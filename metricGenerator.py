if __name__ == '__main__':
    file = "data\\number_handling"
    parent="Number%20Handling"
    
    newFile=file+"_metrics"
    
    for line in open(file):
        trimedLine = line.strip();
        if(len(trimedLine)>0):
            parts = trimedLine.split(';')
            print("<metric full=\""+parts[1]+"\" key=\"true\" language=\"Java\" name=\"Juliet-Testsuite$CWE"+parts[0]+"\" subtype=\"Rule\"/>")
    
    for line in open(file):
        trimedLine = line.strip();
        if(len(trimedLine)>0):
            parts = trimedLine.split(';')
            print("<item child=\"Juliet-Testsuite$CWE"+parts[0]+"\" parent=\""+parent+"\"/>")