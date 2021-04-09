import re
import ToolsFile


def locationCounter():
    # Starting address from ToolsFile, we put the first value in counter variable
    counter = hex(int(ToolsFile.startingadress())).split('x')[-1].upper()
    fout = open("locationCounter.txt", "wt")  # print the start
    # padding the number to be written in 4 bits
    fout.write(str(counter).zfill(4))
    fout.write('\n')
    finalArray = ToolsFile.appendall()
    for i in range(len(finalArray)):
        temp = int(counter, 16)  # we turn hex to int to be able to count

        # we calculate the odd cases for their specific calculations
        if 'BYTE' in finalArray[i][1]:
            temp = temp + 1
        elif 'RESB' in finalArray[i][1]:
            temp = temp + int(finalArray[i][2])
        elif 'RESW' in finalArray[i][1]:
            temp = temp + (int(finalArray[i][2]))*3
        elif 'RESTW' in finalArray[i][1]:
            temp = temp + ((int(finalArray[i][2]))*3)*3
        else:
            temp = temp + 3
        # If it's none of the cases, it'll increment 3 bytes (a whole word) normally
        counter = hex(temp).split('x')[-1].upper()
        fout.write(str(counter).zfill(4))
        fout.write('\n')
    fout.close()

def SymbolTable():
    fout = open("locationCounter.txt", "rt")
    fout2 = open("symbolTable.txt.", "wt")

    # we initiate a variable with the final array we made before that has the program
    finalArray = ToolsFile.appendall()
    # we put the location counter we made in a variable as well
    locationArray = fout.readlines()
    for i in range(len(finalArray)):
        if finalArray[i][0] != '':  # if we don't have an index in the first column then we skip it
            symbol1 = finalArray[i][0]  # we write the index
            # then put beside it the calculated location of it
            symbol2 = locationArray[i]
            fout2.write(symbol1 + ' ' + symbol2 + '\n')
