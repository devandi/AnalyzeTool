#! /usr/bin/env/python 3.1
#
# tool which compares the output of serveral checkers with the existing issues in the testsuite
# author: Andreas Wagner
#
from IssueComparison import IssueComparison
from ComparisonResultHolder import ComparisonResultHolder
from Issue import Issue
from AnalyzeToolConfig import AnalyzeToolConfig
from collections import OrderedDict
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import os
from pylab import *
from ScannerCWEMapping import ScannerCWEMapping
import csv
from ScannerIssueHolder import ScannerIssueHolder
from SecurityModel import SecurityModel
from SecurityModelComparision import SecurityModelComparision
from HTMLReport import HTMLReport
import shutil

class CompareTool(object):
	def __init__(self, config):
		self.config = config
		self.securityModel = SecurityModel(config.securityModelPath)
		self.securityModel.buildModel()
	
	#read the existing flaw file in the memory for further use
	def readExistingFlawFile(self,root):
		flawMap = dict()
		for file in root.iter("file"):
			fileName = os.path.basename(file.get("path")).lower()
			issueList = []
			for issue in file.iter("issue"):
				newIssue = Issue(fileName, issue.get("type"), issue.get("startLine"))
				if(issue.get("endLine")!=None):
					newIssue.endLine=issue.get("endLine")
					newIssue.startLine=issue.get("startLine")
				issueList.append(newIssue)
				self.securityModel.appendExistingIssue(newIssue)
				
			issueComparision = IssueComparison(fileName)
			issueComparision.addExistingIssues(issueList)
			flawMap[fileName] = issueComparision
		return flawMap
		
	def parseScannerResultFile(self, scanner, file, flawMap, falseFlawMap):
		
		#AW20130614 first parse CWE-Scanner Mapping file. 
		cweMapping = ET.parse(self.config.cweMappingsPath+scanner+"CWEMappings.xml");
		
		cweRoot = cweMapping.getroot();
		
		abbrvCWEMap = dict()
		for scannerCode in cweRoot.iter("scannerCode"):
			origName = scannerCode.get("name")
			
			cweList = []
			for cweEntry in scannerCode.iter("cwe"):
			#cweEntry = scannerCode.find("cwe")
				cweId = cweEntry.get("id")
				cweList.append(cweId)
				
			abbrvCWEMap[origName]= ScannerCWEMapping(origName,cweList)
			
		#foundIssueCnt = 0
		with open(file, "r") as csvFile:
			reader = csv.reader(csvFile, delimiter=';')
			
			lastFileName = ''
			issueList = []
			for row in reader:
				
				if(len(row)>0):
					
					
					
					abbrv = row[1]
					
					fileExtensionPoint = row[2].rfind('.')
					#splitFileName = row[2].split('.')
					
					highestDot = row[2].rfind('.', 0, fileExtensionPoint-1)
					highestBackslash = row[2].rfind('\\')
					startSplit = max(highestDot, highestBackslash)
					scannedFile = row[2][startSplit+1:]
					
					'''if(len(splitFileName)<3):
						splitFileName = row[2].rsplit('\\')
						scannedFile = splitFileName[1]
					else:
						scannedFile = splitFileName[1]+"."+splitFileName[2]'''
					scannedFile = scannedFile.lower()
					
					lineNumber = row[4]
					
					if(abbrv in abbrvCWEMap):
						cweEntry = abbrvCWEMap[abbrv].cweList[0]
						cweList = abbrvCWEMap[abbrv].cweList
					else:
						cweEntry = ''
						cweList = []
					#print('test'+abbrv+"; "+cweEntry+"; "+scannedFile)
					
					if(lastFileName==''):
						lastFileName = scannedFile;
					
					scannerIssue = ScannerIssueHolder(scannedFile,abbrv, cweEntry, cweList, lineNumber)
					issueList.append(scannerIssue)
					if(lastFileName!=scannedFile):
						#print(scannedFile)
						if(scannedFile in flawMap):
							issueComparison = flawMap.get(scannedFile);
						else:
							issueComparison = IssueComparison(scannedFile)
							flawMap[scannedFile] = issueComparison;
						#foundIssueCnt+=len(issueList)
						issueComparison.addFoundScannerIssues(scanner, issueList)
						issueList = []
						lastFileName = scannedFile
					
			#print("ISSUE-CNT: "+str(foundIssueCnt))
		'''eTree = ET.parse(file)
		root = eTree.getroot()
		for file in root.iter("file"):
			fileName = file.get("path").lower()
			issueList = []
			for issue in file.iter("issue"):
				issueList.append(Issue(file, issue.get("type"), issue.get("lineNumber")))
			issueComparison = flawMap.get(fileName);
			issueComparison.addFoundIssues(scanner, issueList)'''
		print("parsed foundIssueFile")
		
		
	def printAndWriteResult(self, flawMap, baseDir, scannerList, title):
		mainResult = ComparisonResultHolder()
		scannerResults = OrderedDict()
		securityModelResultMap = OrderedDict()
		scannerResults['JULIET'] = ComparisonResultHolder()
		securityModelResultMap['JULIET'] = SecurityModelComparision(self.securityModel,'JULIET')
		
		root = ET.Element("analyzereport")
		details = ET.SubElement(root, "details")
		for sc in scannerList:
			scannerResults[sc.name] = ComparisonResultHolder()
			securityModelResultMap[sc.name] = SecurityModelComparision(self.securityModel,sc.name)
		
		for key, issueComparison in flawMap.items():
			issueComparison.compareIssues()
			#print(key)
			
			if(len(issueComparison.existingIssues) >0):
				totalIssues = 1
			else:
				totalIssues = 0
			#print("totalIssues="+str(totalIssues))
			mainResult.issueCnt+=totalIssues
			
			fileIssue = ET.SubElement(details, 'file', {'totalIssues' : str(totalIssues), 'name' : issueComparison.fileName})
			
			for scanner, issueHolder in issueComparison.foundIssues.items():
				#print("\tSecurity-Scanner: "+scanner)
				#print("\t\tfound issues="+str(len(issueHolder.foundIssues)))
				#print("\t\tcorrectMath="+str(issueHolder.correctMatchCnt))
				
				secModelResult = securityModelResultMap[scanner]
				comparisonResult = scannerResults.get(scanner)
				comparisonResult.addIssue(issueComparison,issueHolder)
				
				secModelResult.addIssueComparision(issueComparison)
				
				if(scanner!='JULIET'):
					scannerXMLResult = ET.SubElement(fileIssue, 'scanner', {'name' : scanner, 'foundIssues': str(len(issueHolder.foundIssues)),'realIssues': str(len(issueComparison.existingIssues)), 'correctLineMatches' : str(issueHolder.correctMatchCnt), 'differentLineMatches' : str(issueHolder.differentLineMatches), 'differentTypeMatches' : str(issueHolder.rangeMatch), 'differentTypeMatches' : str(issueHolder.rangeMatch), 'noneMatching' : str(issueComparison.noneMatching)})
				
		print("=============================")
		print("========"+title+" SUMMARY========")
		print("=============================")
		print("Total Issues: "+str(mainResult.issueCnt))
		print("Scanners: ")
		
		summary = ET.SubElement(root, 'summary', {'totalIssues' : str(mainResult.issueCnt)})
		chartData = OrderedDict()
		chartData['Total Issues'] = mainResult.issueCnt
		for key, value in scannerResults.items():
			
			if(scanner!='JULIET'):
				summaryDetail = value.getXMLSubelement(summary, 'scanner', key)
				print(key+" found "+str(value.issueCnt)+" of "+str(value.realIssues))
				value.printDetailData()
				#print("\t"+str(value.withoutCWE)+" CWE")
				chartData[key] = value.issueCnt
				self.printPieChart(key, value, baseDir)
		
		secModelXML = ET.SubElement(root, 'securityModel')
		for key, value in securityModelResultMap.items():
			compareResultMap = value.compare()
			if(scanner!='JULIET'):
				scannerXML = ET.SubElement(secModelXML, 'scanner', {'name' : key})
				print(key)
				for weaknessClass, resultHolder in compareResultMap.items():
					resultHolder.getXMLSubelement(scannerXML, 'weaknessClass', weaknessClass)
					print(weaknessClass)
					resultHolder.printDetailData()
		#write xml
		with open(baseDir+'report.xml', 'w') as f:
			f.write(parseString(ET.tostring(root)).toprettyxml())
		
		self.printChart(chartData, baseDir, title)
		
		htmlReport = HTMLReport(mainResult, scannerResults, securityModelResultMap, baseDir+"report.html")
		htmlReport.buildReport()
		
	#source http://www.goldb.org/goldblog/2007/03/23/PythonCreatingBarGraphsWithMatplotlib.aspx
	def printChart(self, name_value_dict, baseDir, heading):
		figure(figsize=(4, 2)) # image dimensions  
		title(heading+" Analyze-Report", size='x-small')	
		# add bars
		for i, key in zip(range(len(name_value_dict)), name_value_dict.keys()):
			if(i==0):
				mycolor = 'red'
			else:
				mycolor = 'green'
			bar(i + 0.25 , name_value_dict[key], color=mycolor)
		# axis setup
		xticks(arange(0.65, len(name_value_dict)),
			[('%s: %d' % (name, value)) for name, value in
			zip(name_value_dict.keys(), name_value_dict.values())],
			size='xx-small')
		max_value = max(name_value_dict.values())
		
		tick_range = arange(0, max_value, 1000)
		yticks(tick_range, size='xx-small')
		formatter = FixedFormatter([str(x) for x in tick_range])
		gca().yaxis.set_major_formatter(formatter)
		gca().yaxis.grid(which='major')
		
		savefig(baseDir+"reportchart.png")
		
	def printPieChart(self, scannerName, scannerResult, baseDir):
		# make a square figure and axes
		figure(figsize=(12, 12))
		ax = axes([0.1, 0.1, 0.8, 0.8])
	
		# The slices will be ordered and plotted counter-clockwise.
		labels = 'correct line matches', 'different line matches', 'range matches', 'different type matches', 'none matching'
		fracs = [scannerResult.correctMatchCnt, scannerResult.differentLineMatches, scannerResult.rangeMatch, scannerResult.differentTypeMatches, scannerResult.noneMatching]
		explode = (0, 0, 0, 0,0)
	
		pie(fracs, explode=explode, labels=labels,
	    	autopct='%1.1f%%', shadow=True, startangle=90)
	                # The default startangle is 0, which would start
	                # the Frogs slice on the x-axis.  With startangle=90,
	                # everything is rotated counter-clockwise by 90 degrees,
	                # so the plotting starts on the positive y-axis.
	
		title(scannerName+' detail data', fontsize=32)
	
		savefig(baseDir+"report"+scannerName+"piechart.png")
		
	def compareResults(self, tmpDataDir, scannerList, title):
		reportDir = tmpDataDir+"report\\"
		existingIssuesFile = tmpDataDir+'existingIssues.xml'
		
		if(not os.path.isfile(existingIssuesFile)):
			print("File: "+existingIssuesFile+" not found returning...")
			return
		
		eTree = ET.parse(existingIssuesFile)
		root = eTree.getroot()
		
		
		
		flawMap = self.readExistingFlawFile(root)
		falseFlawMap = dict()
		print("parsed existingIssueFile")
			
		for scanner in scannerList:
			self.parseScannerResultFile(scanner.name, tmpDataDir+scanner.name+".csv", flawMap, falseFlawMap)
		
		if (not os.path.exists(reportDir)):
			os.mkdir(reportDir)
		
		cssSrcFile = self.config.cweMappingsPath+"reportStyle.css"
		cssDestFile = reportDir+"reportStyle.css"
		if(not os.path.isfile(cssDestFile)):
			shutil.copy(cssSrcFile, cssDestFile)
		self.printAndWriteResult(flawMap, reportDir, scannerList, title)
if __name__ == '__main__':
	cfg = AnalyzeToolConfig('config.cfg')
	
	tool = CompareTool(cfg)
	if(len(cfg.getCCppScannerList())>0):
		tool.compareResults(cfg.tmpCppDataPath, cfg.getCCppScannerList(), "C/C++")
	if(len(cfg.getJavaScannerList())>0):
		tool.compareResults(cfg.tmpJavaDataPath, cfg.getJavaScannerList(), "Java")
