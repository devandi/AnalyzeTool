#
# Class which represents the config of the tool
# author: Andreas Wagner
#

from SecurityScanner import SecurityScanner
import configparser
import glob
import os.path
class AnalyzeToolConfig(object):
	def __init__(self, configFile):
		self.config = configparser.ConfigParser()
		self.config.read('config.cfg')
		self.ccpptestsuitePath = self.config.get('General', 'ccpptestsuitepath')
		self.javatestsuitePath = self.config.get('General', 'javatestsuitepath')
		self.javaClasstestsuitePath = self.config.get('General', 'javaclassestestsuitepath')
		self.scanners = self.config.get('General', 'scanners')
		self.tmpCppDataPath = self.config.get('General', 'tmpCCppData')
		self.tmpJavaDataPath = self.config.get('General', 'tmpJavaData')
		self.javaLibsPath = self.config.get('General', 'javalibs')
		self.javaClassesPath = self.config.get('General', 'javaclasses')
		self.ccppScanners = set()
		self.javaScanners = set()
		self.javaSrcScanners = set()
		self.javaClassScanners = set()
		self.javaClassNames = set()
		self.javaLibs = set()
		self.samateJavaFilePath = self.config.get('General', 'samateJavaFilePath')
		self.samateCCPPFilePath = self.config.get('General', 'samateCCPPFilePath')
		self.securityModelPath = self.config.get('General', 'securityModelPath')
		self.cweMappingsPath = self.config.get('General', 'cweMappingsPath')
		self.motJar = self.config.get('General', 'motJar')
		self.motMeta = self.config.get('General', 'motMeta')
		self.buildJavaRessources()
		self.buildScannerList()
		self.allowedFileTypes = self.config.get('General', 'allowedFileTypes').split(',')
		
	#build scannerList for the scanners which are defined in the config
	def buildScannerList(self):
		if(len(self.scanners)<=0):
			print("no scanners defined. returning...")
			return;
		scannerNames = self.scanners.split(',')
		for sc in scannerNames:
			securityScanner = SecurityScanner(sc, self)
			
			if(securityScanner.type == 'ccpp'):
				self.ccppScanners.add(securityScanner)
			elif(securityScanner.type == 'java'):
				self.javaScanners.add(securityScanner)
				if(securityScanner.useClassFiles):
					self.javaClassScanners.add(securityScanner)
				else:
					self.javaSrcScanners.add(securityScanner)
	
	def buildJavaRessources(self):
		for fileName in glob.glob(self.javaClassesPath):
			self.javaClassNames.add(os.path.basename(fileName).replace(".java",""))
		
		for fileName in glob.glob(self.javaLibsPath):
			self.javaLibs.add(fileName)
			
	def getCCppScannerList(self):
		return self.ccppScanners;
	
	def getJavaScannerList(self):
		return self.javaScanners;