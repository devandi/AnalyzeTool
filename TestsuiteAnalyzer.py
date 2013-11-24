#! /usr/bin/env/python 3.1
#
# analyze tool inspired from juliet-test-suite 'run_analysis_example_tool
# author: Andreas Wagner
#

from AnalyzeToolConfig import AnalyzeToolConfig
import glob
import os
import py_common
import sys
import time
# add parent directory to search path so we can use py_common
sys.path.append("..")

class TestsuiteAnalyzer(object):
	def __init__(self, config):
		self.config = config
		
	#run each security scanner for the file
	def run_example_tool(self, bat_file, scannerList):
			
		for sc in scannerList:
			#AW20130309 set use shell to true here, otherwise pipes don't work
			py_common.run_commands([sc.getCmdString(bat_file)], True)
			#print(sc.getCmdString(bat_file))
			
	# copied from pycommons and modified slightly to fit the needs
	def run_analysis(self,glob_needle, run_analysis_fx, scannerList):
		"""
		Helper method to run an analysis using a tool.  Takes a glob string to search
		for and a function pointer.
		"""
		#AW20130730 some modifications to speed up the mscompiler. can only be used if no other scanner runs
		#msCompilerCMD='C:\\Program Files\\Microsoft Visual Studio 10.0\\VC\\bin\\vcvars32.bat'
		#py_common.run_commands([msCompilerCMD], True)
		time_started = time.time()
	
		# find all the files
		files = glob.glob(glob_needle)
	
		lastDir = 'none'
		# run all the files using the function pointer
		for file in files:
			#AW20130717 ensure only defined file extensions are processed
			if(any(file.endswith(x) for x in self.config.allowedFileTypes)):	
				# change into directory with the file
				dir = os.path.dirname(file)
				os.chdir(dir)
		
				# run the the file
				file = os.path.basename(file)
				dirName = os.path.basename(dir)
				#run_analysis_fx(file, scannerList)
				for sc in scannerList:
					if(not sc.scanFolder):
						#AW20130309 set use shell to true here, otherwise pipes don't work
						py_common.run_commands([sc.getCmdString(file,file)], True)
						print(sc.getCmdString(file,file))
					elif(sc.scanFolder and lastDir!=dir):
						print(sc.getCmdString(dir,dirName))
						py_common.run_commands([sc.getCmdString(dir,dirName)], True)
						lastDir=dir
		
				# return to original working directory
				os.chdir(sys.path[0])
		
		time_ended = time.time()
	
		#print("Started: " + time.ctime(time_started))
		#print("Ended: " + time.ctime(time_ended))
	
		elapsed_seconds = time_ended-time_started
		#print("Elapsed time (in seconds): " + str(elapsed_seconds))
	
	def runAnalyze(self):
		cfg = self.config
		ccppScannerList = cfg.getCCppScannerList()
		javaScannerList = cfg.getJavaScannerList()
		
		searchPathCCpp = cfg.ccpptestsuitePath #+ "\\testcases\\*\\CWE126_Buffer_Overread__CWE129_large_01.c"
		searchPathJava = cfg.javatestsuitePath
		#searchPath = testsuitePath + "\\testcases\\CWE15_External_Control_of_System_or_Configuration_Setting\\*.c*"
		startAnalysis = time.time()
		
		if(len(ccppScannerList)>0):
			print("start C/Cpp testcases")
			ccppStartAnalysis = time.time()
			self.run_analysis(searchPathCCpp, self.run_example_tool, ccppScannerList)
			ccppEndAnalysis = time.time()
			ccppOverallTime = (ccppEndAnalysis - ccppStartAnalysis)
		
		if(len(javaScannerList) >0):
			print("start java testcases")
			javaStartAnalysis = time.time()
			self.run_analysis(searchPathJava, self.run_example_tool, cfg.javaSrcScanners)
			self.run_analysis(cfg.javaClasstestsuitePath, self.run_example_tool, cfg.javaClassScanners)
			javaEndAnalysis = time.time()
			javaOverallTime = (javaEndAnalysis - javaStartAnalysis)
		
		endAnalysis = time.time()
		overallTime = (endAnalysis - startAnalysis)
		print("Overall analysis took " + str(overallTime)+" seconds;") 
		
		if(len(ccppScannerList)>0):
			print("\t C/C++="+str(ccppOverallTime)+" seconds")
			
		if(len(javaScannerList) > 0):
			print("\t Java="+str(javaOverallTime)+" seconds")
if __name__ == '__main__':
	cfg = AnalyzeToolConfig('config.cfg')
	
	tool = TestsuiteAnalyzer(cfg)
	tool.runAnalyze()



