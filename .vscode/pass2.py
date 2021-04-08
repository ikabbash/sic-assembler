import re
import ToolsFile
import pass1


def ObjectCode():
    with open("instructions.txt") as textFile:
        opArr = [line.split(' ') for line in textFile]
    with open("symbolTable.txt") as textFile:
        symbArr = [line.split(' ') for line in textFile]
    finalArr = ToolsFile.appendall()  # keda masakna el 7agat elli 3ayzenha lel object code
    objectcodeFile = open("ObjectCode.txt", "wt")
    for i in range(len(finalArr)):  # keda wa2feen 3and awel row fel program
        if "RESW" in finalArr[i][1] or "RESB" in finalArr[i][1] or "RESTW" in finalArr[i][1]:
            opBits= "no object code !"
            objectcodeFile.write(opBits+"\n")
        if "WORD" in finalArr[i][1] :
            addressBits=hex(int(finalArr[i][2])).split('x')[-1].upper()
            objectcodeFile.write(addressBits.zfill(6)+"\n")
        if "BYTE" in finalArr[i][1] :
            if "C'" in finalArr[i][2]:
                pureChars= finalArr[i][2][2:].replace("'",'')
                addressBits=''.join(str(ord(C)) for C in pureChars)
                objectcodeFile.write(addressBits+"\n")
            if "X'" in finalArr[i][2]:
                addressBits=finalArr[i][2][2:].replace("'",'')
                objectcodeFile.write(addressBits+"\n")

        else : #law ana mesh 7ala shazza
            for j in range(len(opArr)):
                if finalArr[i][1] in opArr[j][0]: #law el operation elli m3aya la2etha
                    opBits = (bin(int(opArr[j][1], 16))[2:].zfill(8) )
                    if ',X' in finalArr[i][2]:
                        xBit='1'
                    else :
                        xBit='0'
                    for m in range(len(symbArr)) :
                        if finalArr[i][2].replace(',X',"") in symbArr[m][0] :
                            addressBits=(bin(int(symbArr[m][1], 16))[2:]).zfill(15)
                    hexObjectCode=hex(int((opBits+''+xBit+''+addressBits),2)).split('x')[-1].upper().zfill(6)

                    objectcodeFile.write(hexObjectCode+"\n")
