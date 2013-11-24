#! /usr/bin/env/python 3.1
#
# run through files and parse errors from the files which are indicated by comments
# author: Andreas Wagner
#

from AnalyzeToolConfig import AnalyzeToolConfig
from Issue import Issue
from xml.dom.minidom import parseString
from xml.etree.ElementTree import Element, SubElement, tostring, parse
import glob
import os.path
import re
import linecache
import sys

class FlawCollector(object):
	def __init__(self, config):
		self.config = config
		
		#defines an area in which the issues should be between
		self.CONST_ERROR_AREA = 10
		
	# build category list which represents different kinds of flaws
	# AW20130705 this is deprecated and only used for some testing purpose
	# but has no effect for the analyzing
	#
	def buildCategoryList(self):
		categoryList = ['FLAW', 'POTENTIAL FLAW', 'INCIDENTAL']
		
		return categoryList

	#collect flaws from the file
	def collectFlaws(self,filePath, samateIssueMap, categoryList):
		foundCategory = []
		lineNumber = 1
		
		badFunctionFound = False
			
		shouldSearchForIssues = False
		
		#defining the bad functions as defined in the docu, slightly adopted
		primaryBadFunction = "(CWE.*_)?bad\(.*\).*$"
		if(".java" in filePath):
			badFunctionPattern = "((.*bad\(.*\))|((bad_.*)\(.*\))|((helper_bad.*)\(.*\))|((_bad.*)\(.*\))).*$"
		else:
			#(((CWE.*_)?bad\(\).*$)|((CWE.+_)bad_source(_[a-z])?.*$)|(
			#badFunctionPattern = "(((CWE.*_)?bad\(\).*)|(bad_([a-z])*))$"
			badFunctionPattern = "(((CWE.*_)?bad\(\).*)|((bad_.*)\(.*\))|((helper_bad.*)\(.*\))).*$"
		
		#inlineBadFunctionPattern = ".*/\*("+badFunctionPattern+")";
		startLine = -1;
		endLine = -1;
		if("_bad" in filePath):
			badClassFile = True
			startLine = 1;
		else:
			badClassFile = False
		
		cweEntry = os.path.basename(filePath).split("_")[0]
		
		issueList = []
		hasPrimaryBadFunction = False;
		isInComment = False;
		isBlank = False;
		fileName = os.path.basename(filePath)
		
		#if we found an entry in the samateissuemap use this one because there we have definied line numbers
		if(fileName in samateIssueMap):
			samateIssue = samateIssueMap.get(fileName)
		else:
			samateIssue = None;
		
		samateIssueList = list()
		samateGeneratedIssue = None
		alreadyProcessedErrorLines = list()
		#print(filePath)
		for line in open(filePath):
			trimedLine = line.strip()
			#print("isComment="+str(line.find('/*')))
			
			#try to find comment lines
			commentStart = trimedLine.find('/*')
			commentEnd = trimedLine.find('*/')
			if(not badClassFile and commentStart >=0):
				isInComment = True;
			if(not badClassFile and commentEnd>=0):
				isInComment = False
			
			#use search regex to find the line match
			match = re.search(badFunctionPattern, trimedLine)
			if(match != None and ((commentStart==-1 and commentEnd==-1) or not (match.start() >=commentStart and match.start()<=commentEnd))):
				correctMatch = True
			else:
				correctMatch = False
				
			#print("trimedLine="+trimedLine+"; isComment="+str(isInComment)+"; isBlank="+str(isBlank)+"; badClassFile="+str(badClassFile))
			if (not badClassFile and correctMatch and not ";" in trimedLine and not isInComment):
				badFunctionFound = True
				#print("hello"+trimedLine)
				openBracketCount = 0
				if(re.search(primaryBadFunction, trimedLine) !=None):
					hasPrimaryBadFunction = True
					
				startLine = lineNumber;
				
				if(not isBlank):
					#print("create issue")
					
					issue = Issue(filePath, cweEntry, -1)
					issue.startLine = lineNumber
			
			if(isBlank and (len(trimedLine)==0 or trimedLine.startswith('/*')) ):
				isBlank = True
			else:
				isBlank = False
				
			if(badFunctionFound):
				
				if('{' in trimedLine and not trimedLine.startswith('/*') and not trimedLine.startswith('*')):
					openBracketCount = openBracketCount + 1
				if('}' in trimedLine and not trimedLine.startswith('/*') and not trimedLine.startswith('*')):
					openBracketCount = openBracketCount - 1		
					
					if(openBracketCount==0):
						badFunctionFound = False
						endLine = lineNumber;
						issue.endLine = lineNumber
						issueList.append(issue)
						isBlank = True
						
					
			#AW20130412 for now only use the full function as possible errors	
			if(badFunctionFound or badClassFile):
				shouldSearchForIssues = True
			else:
				shouldSearchForIssues = False
			
			
				
			if(shouldSearchForIssues):
				#search for FLAW-Comments in the current line and add them to the category list if found
				#this category logic is deprecated and only used for some testing purpose
				if any(cat in line for cat in categoryList):
					startIdx = line.find('/*')
					endIdx = line.find(':')
					foundCategory.append(line[startIdx+2:endIdx].strip())
					
				
				#AW20130525 use documented flaw line number if possible
				#sadly the files do not match 100% therefore we need to compare the error lines manually
				#and check in which linenumber we are
				if(samateIssue!=None and len(samateIssue)>0):
					#print(filePath+"; match=")
					#print("trimedLine="+trimedLine)
					for sIssue in samateIssue:
						
						sIssueLineNumber = int(sIssue.lineNumber)
						
						#AW20130529 the errorLine should be near the defined lineNumber in the SRD-Files (use CONST_ERROR_AREA as space)
						if(trimedLine == sIssue.errorLine and sIssue.errorLine not in alreadyProcessedErrorLines and lineNumber>= sIssueLineNumber-self.CONST_ERROR_AREA and lineNumber <= sIssueLineNumber+self.CONST_ERROR_AREA):
							#print("trimedLine="+trimedLine+"; "+sIssue.errorLine)
							samateGeneratedIssue = Issue(filePath, cweEntry, lineNumber)
							samateIssueList.append(samateGeneratedIssue)
							alreadyProcessedErrorLines.append(sIssue.errorLine)	
			lineNumber+=1
			
		if(badClassFile):
			endLine = lineNumber;
			issue = Issue(filePath, cweEntry, -1)
			issue.startLine=startLine
			issue.endLine = endLine
			issueList.append(issue)
		
		#if('issue' in locals() and not issue in issueList):
		#	issueList.append(issue)
		if(len(samateIssueList)>0):
			#print("use samate Issue List "+str(len(samateIssueList)))
			issueList = samateIssueList
		#AW20130412 only return issues which occur in files with primary bad function
		if(len(issueList)==0 or (not badClassFile and not hasPrimaryBadFunction)):
			return None
		else:
			if(len(foundCategory)<=0):
				print(filePath)
			return issueList
	
	#write the Issue
	def writeXML(self, flawMap, fileXML):
		for key, value in flawMap.items():
			for issue in value:
				elem = issue.getXMLElement(fileXML)
	
	def readSAMATEErrorFiles(self, samateFilePath):
		#mainPath = 'C:\\Users\\user\\Masterarbeit\\SAMATE\\Java\\*\\manifest.xml'
		mainPath = samateFilePath
		samateIssueMap = dict()
		for file in glob.glob(mainPath):
			dirName = os.path.dirname(file)
			eTree = parse(file)
			root = eTree.getroot()
		
			for error in root.iter("file"): 
				flawList =error.findall("flaw")        
				if(flawList!=None):
					filePath = error.get("path")
					fileName = os.path.basename(filePath)
					samateIssueMap[fileName] = list()
					for flaw in flawList:
						
						flawLineNumer = flaw.get("line")
						if(flawLineNumer!=None):
							errorLine = linecache.getline(dirName+"\\"+filePath, int(flawLineNumer))
							errorLine = errorLine.strip();
							issue = Issue(fileName, "", flawLineNumer)
							issue.errorLine = errorLine;
							#print(fileName+"; "+filePath+"; "+flawLineNumer+"; "+errorLine)
							samateIssueMap[fileName].append(issue);
						#else:
							#print(fileName)
				
						
		return samateIssueMap
	
	def collect(self, testsuiteLanguage):
		#startTime = time.time();
		print("start collecting flaws")
		categoryList = self.buildCategoryList()
	
		
		#searchPath = 'C:\\Users\\user\\Masterarbeit\\Juliet_Test_Suite_v1.1_for_C_Cpp\\testcases\\CWE401_Memory_Leak\\*'
		#searchPath ="C:\\Users\\user\Masterarbeit\\Juliet_Test_Suite_v1.1_for_C_Cpp\\testcases\\CWE126_Buffer_Overread\\*"
		#searchPath ="C:\\Users\\user\Masterarbeit\\Juliet_Test_Suite_v1.1_for_C_Cpp\\testcases\\*\\*"
		searchPath ="C:\\Users\\user\Masterarbeit\\Juliet_Test_Suite_v1.1.1_for_Java\\src\\testcases\\*\\*.java"
		
		if(testsuiteLanguage=='java'):
			searchPath = self.config.javatestsuitePath
			samateFilePath = self.config.samateJavaFilePath
			outputPath = self.config.tmpJavaDataPath
		elif(testsuiteLanguage=='ccpp'):
			searchPath = self.config.ccpptestsuitePath
			samateFilePath = self.config.samateCCPPFilePath
			outputPath = self.config.tmpCppDataPath
		else:
			print("unknown testsuiteLanguage was set. defaulting to java")
			searchPath = self.config.javatestsuitePath
			samateFilePath = self.config.samateJavaFilePath
			outputPath = self.config.tmpJavaDataPath
		
		if (os.path.exists(outputPath+"existingIssues.xml")):
			print("existingIssue file already exists. aborting...");
			return
			
		print("searchPath="+searchPath+"; samateFilePath="+samateFilePath)
		
		
		
		files = glob.glob(searchPath)
	
		root = Element('files')
		
		samateIssueMap = self.readSAMATEErrorFiles(samateFilePath)
		
		for file in files:	
			#AW20130717 ensure only defined file extensions are processed
			if(any(file.endswith(x) for x in self.config.allowedFileTypes)):		
				issueList = self.collectFlaws(file, samateIssueMap, categoryList)
				
				#AW20130427 only write output if there are issues
				if(issueList!=None):
					lastStartLine = -1;
					lastEndLine = -1;
					writeIssueCnt = 0;
					#print(fileName+"; issueCnt="+str(len(issueList)))
					for issue in issueList:
						
						if(lastStartLine!=issue.startLine and lastEndLine!=issue.endLine or issue.lineNumber!=-1):
							fileXML = SubElement(root, 'file', {'path' : file})
							issue.getXMLElement(fileXML)
							lastStartLine = issue.startLine;
							lastEndLine = issue.endLine;
							writeIssueCnt+=1
		
		#write the result as xml
		with open(outputPath+'existingIssues.xml', 'w') as f:
			f.write(parseString(tostring(root)).toprettyxml())
		
		#endTime = time.time()
		#print("flaws collected in "+str((endTime-startTime))+" seconds")

if __name__ == '__main__':
	testsuiteLanguage = 'java'
	if(len(sys.argv)>1):
		testsuiteLanguage = sys.argv[1]
	config = AnalyzeToolConfig('config.cfg')
	
	collector = FlawCollector(config)
	collector.collect(testsuiteLanguage)

