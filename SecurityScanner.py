#
#
# Simple class for encapsulating different kinds of security scanners
# author Andreas Wagner
#
import time
class SecurityScanner(object):
	def __init__(self, name, cfg):
		self.name = name
		self.cfg = cfg
		
		if(cfg.config.has_option(name, 'options')):
			self.options = cfg.config.get(name, 'options')
		
		if(cfg.config.has_option(name, 'executable')):
			self.executable = cfg.config.get(name, 'executable')
			
		if(cfg.config.has_option(name, 'afterFileOptions')):
			self.afterFileOptions = cfg.config.get(name, 'afterFileOptions')
		
		if(cfg.config.has_option(name, 'wrapper')):
			self.wrapper = cfg.config.get(name, 'wrapper')
		
		if(cfg.config.has_option(name, 'type')):
			self.type = cfg.config.get(name, 'type')
			
		if(cfg.config.has_option(name, 'singleClassPathOption')):
			self.singleClassPathOption = cfg.config.get(name, 'singleClassPathOption')
			
		if(cfg.config.has_option(name, 'scanFolder')):
			self.scanFolder = cfg.config.get(name, 'scanFolder')
		else:
			self.scanFolder = False
			
		if(cfg.config.has_option(name, 'useClassFiles')):
			self.useClassFiles = cfg.config.get(name, 'useClassFiles')
		else:
			self.useClassFiles = False
		
		if(cfg.config.has_option(name, 'motMetaFile')):
			self.motMetaFile = cfg.config.get(name, 'motMetaFile')
			
		if(cfg.config.has_option(name, 'outputFile')):
			self.outputFile = cfg.config.get(name, 'outputFile')
		
	
	# return the cmd String which can be run from the commandline
	def getCmdString(self, file, fileName):
		commandList = []
		commandList.append("\"" + self.executable)
		commandList.append("\"")
		
		
		
		
		if(self.type=='java'):
			if(hasattr(self, 'singleClassPathOption')):
				classesPath = file[:file.index('\\antbuild')]+"\\antbuild\\testcasesupport\\"
				for compiledClass in self.cfg.javaClassNames:
					entry = self.singleClassPathOption+" "+classesPath+"\\"+compiledClass+".class"
					entry = entry.replace("\\\\","\\")
					commandList.append(entry)
					
				for javaLib in self.cfg.javaLibs:
					commandList.append(self.singleClassPathOption+" "+javaLib)
				
					
		
		if(hasattr(self, 'options')):
			commandList.append(self.options)
			
		
		commandList.append(file)
		
		if(hasattr(self, 'afterFileOptions')):
			commandList.append(self.afterFileOptions)
		
		cmd = " ".join(commandList)
		cmd = cmd.replace("#filename", fileName)
		return cmd