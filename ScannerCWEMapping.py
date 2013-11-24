#
# Simple class which encapsulates the scanner result cwe mapping 
# author Andreas Wagner
#
class ScannerCWEMapping(object):
    def __init__(self, origType,cweList):
        self.origType = origType
        self.cweList = cweList