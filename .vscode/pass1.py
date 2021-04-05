import re
import ToolsFile

def locationCounter() :
    counter=hex(int(ToolsFile.startingadress())).split('x')[-1]
    fout = open("locationCounter.txt", "wt") # print the start
    fout.write(str(counter).zfill(4))
    fout.write('\n')
    for i in ToolsFile.appendall():
        temp = int(counter,16)
        temp = temp + 3
        counter = hex(temp).split('x')[-1]
        fout.write(str(counter).zfill(4))
        fout.write('\n')