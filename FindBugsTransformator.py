import glob
if __name__ == '__main__':
    
    srcPath = 'C:\\Users\\user\\Masterarbeit\\tmpData\\Java\\findbugs\\'
    srcPath2 = 'C:\\Users\\user\\Masterarbeit\\tmpData\\Java\\findbugs\\*'
    
    fileList = glob.glob(srcPath2)
   

    print("start reading files")

    with open(srcPath+'findbugs_complete_result.xml', 'w') as f:
        f.write(" <?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
        f.write("<BugCollection>\n");
        for file in fileList:
            print("read file="+file)
            for line in open(file):
                strippedLine = line.strip()
                if not strippedLine.startswith("<?xml") and not strippedLine.startswith("<BugCollection>") and not strippedLine.startswith("</BugCollection>"):
                    line = line.replace("testcases.","")
                    f.write(line)
        f.write("</BugCollection>\n");
                