'''
Created on 28.03.2013

@author: Andreas Wagner
'''
from Issue import Issue
from ResultConverter import ResultConverter
import xml.etree.ElementTree as ET


class PMDResultConverter(ResultConverter):
    
    def __init__(self, filePath, tmpDir):
        self.issueMap = dict()
        self.filePath = filePath
        self.baseDir = tmpDir
    
    def getXML(self):
        self.buildIssueList()
        root = ET.Element("results", {'securityScanner' : 'pmd'})
        for key, value in self.issueMap.items():
            #print(key)
            fileElement = ET.SubElement(root, 'file', {'path' : key})
            for issue in value:
                #print("\t"+issue.lineNumber)
                elem = issue.getXMLElement(fileElement)
        return root
    
    def buildIssueList(self):
        
        eTree = ET.parse(self.baseDir+'pmdresults.xml')
        root = eTree.getroot()
        for error in root.iter("file"):
            fileName = error.get('name')
            fileName = fileName[fileName.rindex('\\')+1:]
            issueList = []
            for violation in error.iter("violation"):
                
                
                
                rule = violation.get('rule')
                
                sourceLine = violation.get("beginline")
               
                
                print("id="+rule+"; file="+fileName+"; line="+str(sourceLine))
                issue = Issue(fileName, rule, sourceLine)
                issueList.append(issue)
               
                    
            self.issueMap[fileName] = issueList
               