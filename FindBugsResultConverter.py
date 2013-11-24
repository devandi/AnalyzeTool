from Issue import Issue
from ResultConverter import ResultConverter
import xml.etree.ElementTree as ET


class FindBugsResultConverter(ResultConverter):
	
	def __init__(self, filePath, tmpDir):
		self.issueMap = dict()
		self.filePath = filePath
		self.baseDir = tmpDir
	
	def getXML(self):
		self.buildIssueList()
		root = ET.Element("results", {'securityScanner' : 'findbugs'})
		for key, value in self.issueMap.items():
			#print(key)
			fileElement = ET.SubElement(root, 'file', {'path' : key})
			for issue in value:
				#print("\t"+issue.lineNumber)
				elem = issue.getXMLElement(fileElement)
		return root
	
	def buildIssueList(self):
		
		eTree = ET.parse(self.baseDir+'findbugsresult.xml')
		root = eTree.getroot()
		for error in root.iter("BugInstance"):
			category = error.get('category')
			
			if(category=="SECURITY"):
				
				type = error.get('type')
				
				sourceLine = error.find("SourceLine")
				filePath = sourceLine.get("sourcepath")
				filePath = filePath[filePath.rindex('/')+1:]
				location = sourceLine.get('start')
				
				print("id="+category+"; file="+filePath+"; line="+str(location))
				issue = Issue(filePath, type, location)
			
				if(issue.filePath in self.issueMap):
					issueList = self.issueMap.get(issue.filePath)
				else:
					issueList = []
					issueList.append(issue)
					self.issueMap[issue.filePath] = issueList