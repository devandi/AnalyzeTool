#! /usr/bin/env/python 3.1
#
# main file (or entry point) for the analysis. Handles all different stuff like, collection flaws, 
# start the security scanners and generate result-reports
# author: Andreas Wagner
#
import time
from FlawCollector import FlawCollector
import sys
from AnalyzeToolConfig import AnalyzeToolConfig
from TestsuiteAnalyzer import TestsuiteAnalyzer
from CompareTool import CompareTool
from TransformTool import TransformTool
import os


if __name__ == '__main__':
    type = 'java'
    if(len(sys.argv)>1):
        type = sys.argv[1]
    config = AnalyzeToolConfig('config.cfg')
    
    startTime = time.time()
    print("Start a complete analysis run")
    print("collection flaws in testsuite")
    
    flawCollector = FlawCollector(config)
    if(len(config.getCCppScannerList())>0):
        startFlawCollection=time.time()
        flawCollector.collect('ccpp')
        endFlawCollection=time.time()
        print("collected ccpp flaws in "+str((endFlawCollection-startFlawCollection))+" seconds")
        for scanner in config.getCCppScannerList():
            tmpDir = config.tmpCppDataPath+scanner.name
            if (not os.path.exists(tmpDir)):
                os.mkdir(tmpDir)
    if(len(config.getJavaScannerList())>0):
        startFlawCollection=time.time()
        flawCollector.collect('java')
        endFlawCollection=time.time()
        print("collected java flaws in "+str((endFlawCollection-startFlawCollection))+" seconds")
        for scanner in config.getJavaScannerList():
            tmpDir = config.tmpJavaDataPath+scanner.name
            if (not os.path.exists(tmpDir)):
                os.mkdir(tmpDir)
   
    
    
    print("start analyzing testsuite");
    startAnalyzeTime = time.time()
    analyzeTool = TestsuiteAnalyzer(config)
    analyzeTool.runAnalyze()
    endAnalyzeTime = time.time()
    print("run static analyzers in "+str((endAnalyzeTime-startAnalyzeTime))+" seconds")
    
    print("transforming scanner results");
    startTransformTime = time.time();
    transformTool = TransformTool(config)
    transformTool.transformResults()
    endTransformTime = time.time();
    print("transformed scanner results in "+str((endTransformTime-startTransformTime))+" seconds")
    
    compareTool = CompareTool(config)
    if(len(config.getCCppScannerList())>0):
        startCompareTime = time.time()
        compareTool.compareResults(config.tmpCppDataPath, config.getCCppScannerList(), "C/C++")
        endCompareTime = time.time()
        print("compared CCPP analyzers in "+str((endCompareTime-startCompareTime))+" seconds")
    if(len(config.getJavaScannerList())>0):
        startCompareTime = time.time()
        compareTool.compareResults(config.tmpJavaDataPath, config.getJavaScannerList(), "Java")
        endCompareTime = time.time()
        print("compared Java analyzers in "+str((endCompareTime-startCompareTime))+" seconds")
    
    endTime = time.time()
    print("completed full run in "+str((endTime-startTime))+" seconds")
    