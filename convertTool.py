#! /usr/bin/env/python 3.1
#
# tool which converts the output of several security checkers to an own format which 
# is needed for further processing
# author: Andreas Wagner
#
from CppcheckResultConverter import CppcheckResultConverter
from MSCompilerResultConverter import MSCompilerResultConverter
from AnalyzeToolConfig import AnalyzeToolConfig
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from FindBugsResultConverter import FindBugsResultConverter
from PMDResultConverter import PMDResultConverter

def convertResult(scanner, tmpDataDir):
	outputFile = config.config.get(scanner, 'outputFile')
	
	if(scanner=='cppcheck'):
		converter = CppcheckResultConverter(outputFile, tmpDataDir)
	elif(scanner=='mscompiler'):
		converter = MSCompilerResultConverter(outputFile, tmpDataDir)
	elif(scanner=="findbugs"):
		converter = FindBugsResultConverter(outputFile, tmpDataDir)
	elif(scanner=="pmd"):
		converter = PMDResultConverter(outputFile, tmpDataDir)
	root = converter.getXML()
	with open(tmpDataDir+scanner+'_converted_file.xml', 'w') as f:
		f.write(parseString(ET.tostring(root)).toxml())

if __name__ == '__main__':
	config = AnalyzeToolConfig('config.cfg')
	
	converterMap = dict()
	
	for scanner in config.getCCppScannerList():
		print("convert file for "+scanner.name)
		convertResult(scanner.name, config.tmpCppDataPath)
	
	for scanner in config.getJavaScannerList():
		convertResult(scanner.name, config.tmpJavaDataPath)	