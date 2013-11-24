import os
from shutil import copytree
import shutil
import glob
import sys


def myCp(root_src_dir, root_dst_dir):       
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            shutil.copy(src_file, dst_dir)

def copyDir(cweEntry):
    destPath = "C:\\Users\\user\\Masterarbeit\\SAMATE\\CCPP\\"+cweEntry+"\\"
    srcPath = "C:\\Users\\user\\Downloads\\SAMATE_CCPP_TMP\\"+cweEntry+"\\"
    
    
    for file in os.listdir(srcPath):
        absPath = srcPath+file
        if(os.path.isdir(absPath)):
           #for subFile in os.listdir(absPath):
           #    absSubPath = absPath+"\\"+subFile
           if(os.path.isdir(absPath)):
               myCp(absPath, destPath)

    with open(destPath+"\\manifest.xml", 'w') as f:
        f.write("<?xml version=\"1.0\"?>")
        f.write("<container>") 
        for file in glob.glob(srcPath+"*\\manifest.xml"):
            for line in open(file):
                newLine = line.replace("<?xml version=\"1.0\"?>","")
                newLine = newLine.replace("<container>","")
                newLine = newLine.replace("</container>","")
                f.write(newLine)
        f.write("</container>") 


if __name__ == '__main__':
    cweNumberStr = sys.argv[1]
       
    cweNumberList = cweNumberStr.split(",")
    
    for number in cweNumberList:
        copyDir("CWE"+number)
    
    
    
            

