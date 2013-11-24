#
# Simple class which encapsulates a ScannerIssue 
# Ligther than the full Issue-class. Needed for comparision withing the IssueComparison
# author Andreas Wagner
#
from xml.etree.ElementTree import SubElement
class ScannerIssueHolder(object):
    def __init__(self, filePath, origType,cwe, cweList, lineNumber):
        self.filePath = filePath
        self.origType = origType
        self.lineNumber = lineNumber
        self.cwe = cwe
        self.cweList = cweList
    def getXMLElement(self, parentElement):
        elem = SubElement(parentElement, 'issue', {'origType' : self.origType, 'line' : str(self.lineNumber), 'cwe' : str(self.cwe)})
                
        return elem