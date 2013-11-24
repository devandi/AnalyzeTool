import xml.etree.ElementTree as ET

# simple generic result holder which is used to sum up different 
# results from the files in one class
class ComparisonResultHolder(object):
	def __init__(self):
		self.issueCnt = 0
		self.correctMatchCnt=0
		self.realIssues = 0
		self.differentTypeMatches=0
		self.differentLineMatches=0
		self.rangeMatch=0
		self.noneMatching=0
		self.withoutCWE=0
	
	def addIssue(self,issueComparison, issueHolder):
		self.issueCnt+=len(issueHolder.foundIssues)
		self.correctMatchCnt+=issueHolder.correctMatchCnt
		self.realIssues+=len(issueComparison.existingIssues)
		self.differentLineMatches+=issueHolder.differentLineMatches;
		self.differentTypeMatches+=issueHolder.differentTypeMatches;
		self.rangeMatch+=issueHolder.rangeMatch;
		self.noneMatching+=issueHolder.noneMatching
		self.withoutCWE+=issueHolder.withoutCWE
	
	#TODO
	#def addExistingIssue(self, issue):
	#	self.issueCnt+=
		
	def getXMLSubelement(self, parent, elementName, elementKey):
		return ET.SubElement(parent, elementName, {'name' : elementKey, 'found' : str(self.issueCnt), 'realIssues': str(self.realIssues), 'correctlineMatches' : str(self.correctMatchCnt),'differentLineMatches' : str(self.differentLineMatches), 'differentTypeMatches' : str(self.rangeMatch), 'rangeMatch' : str(self.rangeMatch), 'noneMatching' : str(self.noneMatching)})
	
	def printDetailData(self):
		print("\t"+str(self.correctMatchCnt)+" correct line matches")
		print("\t"+str(self.differentLineMatches)+" different line matches")
		print("\t"+str(self.rangeMatch)+" range matches")
		print("\t"+str(self.differentTypeMatches)+" different type matches")
		print("\t"+str(self.noneMatching)+" none matching")