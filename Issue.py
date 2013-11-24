#
# Simple class which encapsulates an Issue in the Testsuite
# author Andreas Wagner
#
from xml.etree.ElementTree import SubElement
class Issue(object):
	def __init__(self, filePath, category, lineNumber):
		self.filePath = filePath
		self.category = category
		self.lineNumber = lineNumber
		self.startLine = -1
		self.endLine = -1
		self.errorLine = ""
		
	#return a XML-SubElement for the parent element
	def getXMLElement(self, parentElement):
		
		#depending if startline and endline are set generate different xml representations
		if(self.startLine!=-1 and self.endLine!=-1 and self.lineNumber==-1):
			elem = SubElement(parentElement, 'issue', {'type' : self.category, 'startLine' : str(self.startLine), 'endLine' : str(self.endLine)})
		else:
			#AW20130529 use startLine here. Otherwise the spqr tool couldn't transfer the file correctly
			elem = SubElement(parentElement, 'issue', {'type' : self.category, 'startLine' : str(self.lineNumber)})
		
		return elem