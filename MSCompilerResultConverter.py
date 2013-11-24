from Issue import Issue
from ResultConverter import ResultConverter
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import os

class MSCompilerResultConverter(ResultConverter):
	
	def __init__(self, filePath, tmpDir):
		self.issueMap = dict()
		self.filePath = filePath
		self.baseDir = tmpDir
	
	def getXML(self):
		self.buildIssueList()
		root = ET.Element("results", {'securityScanner' : 'mscompiler'})
		for key, value in self.issueMap.items():
			#print(key)
			fileElement = ET.SubElement(root, 'file', {'path' : key})
			for issue in value:
				#print("\t"+issue.lineNumber)
				elem = issue.getXMLElement(fileElement)
		return root
	
	def buildIssueList(self):
		
		eTree = ET.parse(self.baseDir+'\\cl_result.xml')
		root = eTree.getroot()
		for error in root.iter("DEFECT"):
			sfa = error.find('SFA')
			filePath = sfa.find('FILENAME')
			location = sfa.find('LINE')
			category = error.find('DEFECTCODE')
			#print("id="+category+"; file="+filePath+"; line="+str(lineNumber))
			issue = Issue(filePath.text, category.text, location.text)
			
			if(issue.filePath in self.issueMap):
				issueList = self.issueMap.get(issue.filePath)
			else:
				issueList = []
			issueList.append(issue)
			self.issueMap[issue.filePath] = issueList