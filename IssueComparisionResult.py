#simple hold class which encapsulates the result of the compared result            
class IssueComparisonResult(object):
    def __init__(self, securityScanner, foundIssues):
        self.securityScanner = securityScanner
        self.foundIssues = foundIssues
        self.correctMatchCnt = 0
        self.differentTypeMatches=0
        self.differentLineMatches=0
        self.rangeMatch = 0
        self.issueCnt = 0
        self.noneMatching = 0
        self.withoutCWE = 0
        self.noneMatchingWithoutOthers = 0