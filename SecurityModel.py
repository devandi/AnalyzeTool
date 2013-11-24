import xml.etree.ElementTree as ET
from collections import OrderedDict
class SecurityModel(object):
    
    def __init__(self, structureFile):
        self.structureFile = structureFile
        self.hierarchy = OrderedDict()
        self.cweParentMapping = dict()
        self.existingIssueList = []
        
    def appendExistingIssue(self, issue):
        self.existingIssueList.append(issue)
    
    def buildModel(self):
        f = ET.parse(self.structureFile);
        
        root = f.getroot()
        hierarchy = f.find("qualityhierarchy")
        
        
        for item in hierarchy.iter("item"):
            childId = item.get("child")
            
            if("Juliet-Testsuite$" in childId):
                childId = childId.replace("Juliet-Testsuite$","")
                childId = childId.replace("%20"," ")
                if(item.get("parent")!=None):
                    parentName = item.get("parent")
                    parentName = parentName.replace("%20"," ")
                    
                    
                    if(parentName in self.hierarchy):
                        cweList = self.hierarchy[parentName]
                    else:
                        cweList = []
                    
                    cweList.append(childId)
                    self.hierarchy[parentName]=cweList
                    self.cweParentMapping[childId] = parentName
    
    def printHierarchy(self):
        for key, cweEntry in self.hierarchy.items():
           print(key)
           
           for item in cweEntry:
               print("\t"+item)
                
    