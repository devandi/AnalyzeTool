import xml.etree.cElementTree as ET
DESCCOL=1
CWECOL=3
CODECOL=7    
TOOLNAME='FindBugs'
with open('findbugsmappedfile.csv') as mappedFile:
    mappingContent = mappedFile.readlines()


    
generatedMetrics = list()
findbugsmapping = list()
   
root = ET.Element("mappings")
root.set("scanner", TOOLNAME)
    
for line in mappingContent:
    lineAr = line.split("\t")
    cweEntry = lineAr[CWECOL].replace("\n","").replace("#","").strip()
    codeEntry = lineAr[CODECOL].replace("\n","").replace("#","").strip()
    descEntry = lineAr[DESCCOL].replace("\n","").replace("#","").strip()
    
    if(len(cweEntry)>0):    
        scannerCode = ET.SubElement(root, "scannerCode")
        scannerCode.set("name", codeEntry)
        scannerCode.set("desc", descEntry)
        
        cweXML = ET.SubElement(scannerCode, "cwe")
        cweXML.set("id",cweEntry)

tree = ET.ElementTree(root)
tree.write("findBugsCWEMappings.xml")



