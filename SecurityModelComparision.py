from ComparisonResultHolder import ComparisonResultHolder
class SecurityModelComparision(object):
    def __init__(self, securityModel, scannerName):
        self.model = securityModel
        self.issueComparisionMap = dict()
        #self.compareResult = dict()
        self.scannerName = scannerName
        
    def addIssueComparision(self, issueComparision):
        if(len(issueComparision.existingIssues)>0):
            cwe = issueComparision.existingIssues[0].category
            
            cwe = cwe.upper()
           
            
            if(cwe in self.issueComparisionMap):
                issueList = self.issueComparisionMap[cwe]
            else:
                issueList = []
            
            issueList.append(issueComparision)
            self.issueComparisionMap[cwe] = issueList
            
    def compare(self):
        compareResult = dict()
        for key, cweList in self.model.hierarchy.items():
            resultHolder = ComparisonResultHolder()
            print(key)
            for cweItem in cweList:
                if(cweItem in self.issueComparisionMap):
                    issueList = self.issueComparisionMap[cweItem]
                    for issue in issueList:
                        foundIssue = issue.foundIssues[self.scannerName]
                        resultHolder.addIssue(issue, foundIssue)
            compareResult[key]=resultHolder
        
        return compareResult
                