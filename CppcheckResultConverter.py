from Issue import Issue
from ResultConverter import ResultConverter
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import os

class CppcheckResultConverter(ResultConverter):
	
	def __init__(self, filePath, tmpDir):
		self.issueMap = dict()
		self.filePath = filePath
		self.baseDir = tmpDir
	
	def getXML(self):
		self.prepareFile()
		self.buildIssueList()
		root = ET.Element("results", {'securityScanner' : 'cppcheck'})
		for key, value in self.issueMap.items():
			#print(key)
			fileElement = ET.SubElement(root, 'file', {'path' : key})
			for issue in value:
				#print("\t"+issue.lineNumber)
				elem = issue.getXMLElement(fileElement)
		return root
	
	def buildIssueList(self):
		
		eTree = ET.parse(self.baseDir+'\\cppcheck_transformed_file.xml')
		root = eTree.getroot()
		for error in root.iter("error"):
			
			category = error.get('id')
			location = error.find('location')
			filePath = location.get('file')
			lineNumber = location.get('line')
			#print("id="+category+"; file="+filePath+"; line="+str(lineNumber))
			issue = Issue(filePath, category, lineNumber)
			
			if(issue.filePath in self.issueMap):
				issueList = self.issueMap.get(issue.filePath)
			else:
				issueList = []
			issueList.append(issue)
			self.issueMap[issue.filePath] = issueList
			
	def prepareFile(self):
		with open(self.baseDir+'\\cppcheck_transformed_file.xml', 'w') as f:
			f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
			f.write('<results>\n')
			for line in open(self.filePath):
				strippedLine = line.strip()
				if not strippedLine.startswith("<?xml") and not strippedLine.startswith("<results") and not strippedLine.startswith("</results>") and not strippedLine.startswith("<cppcheck"):
					f.write(line)
			f.write('</results>')
	