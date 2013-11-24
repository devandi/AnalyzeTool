#! /usr/bin/env/python 3.1
#
# handle the transformation of the scanner results files. 
# use MOT as transformattor
# author: Andreas Wagner
#
from AnalyzeToolConfig import AnalyzeToolConfig
import os.path
import py_common

class TransformTool(object):
    def __init__(self, config):
        self.config = config
        
    def transformResultForScanner(self, scanner, tmpDataDir):
        outputFolder = os.path.dirname(scanner.outputFile)
        
        execCMD = "java -jar "+self.config.motJar+" -input:"+outputFolder+" -meta:"+self.config.motMeta+"\\"+scanner.motMetaFile+" -output:"+tmpDataDir+scanner.name+".csv"
        py_common.run_commands([execCMD], True)
        
    def transformResults(self):
        cfg = self.config
        ccppScannerList = cfg.getCCppScannerList()
        javaScannerList = cfg.getJavaScannerList()
                
        if(len(ccppScannerList)>0):
            for scanner in ccppScannerList:
                self.transformResultForScanner(scanner, cfg.tmpCppDataPath)
        
        if(len(javaScannerList) >0):
           for scanner in javaScannerList:
                self.transformResultForScanner(scanner, cfg.tmpJavaDataPath)
        
if __name__ == '__main__':
    cfg = AnalyzeToolConfig('config.cfg')
    
    tool = TransformTool(cfg)
    tool.transformResults()
