import re
import ToolsFile
import pass1

# We open the instruction table that has the OP code & the symbol table for reading the calculations.
with open("instructions.txt") as textFile:
    opArr = [line.split(' ') for line in textFile]
with open("symbolTable.txt") as textFile:
    symbArr = [line.split(' ') for line in textFile]
# Our assembly code we'll read/trace from.
finalArr = ToolsFile.appendall()
# Where we'll store the result of Object Code.
objectcodeFile = open("ObjectCode.txt", "wt")

# We imported location counter for the HTE Record
LFile = open("locationCounter.txt", "rt")
LArray = LFile.readlines()


def ObjectCode():
    for i in range(len(finalArr)):  # Tracing the first row of our list.

        if "BYTE" in finalArr[i][1]:
            # Byte have two cases: either ASCII of characters or their immediate value.
            if "C'" in finalArr[i][2]:
                pureChars = finalArr[i][2][2:].replace("'", '')
                # ORD function helps convert characters to ASCII values
                # We used it then stored the value on the Object Code table
                addressBits = ''.join(hex(ord(C)).split(
                    'x')[-1].upper() for C in pureChars)
                # We write down the Object Code
                objectcodeFile.write(addressBits+"\n")
            if "X'" in finalArr[i][2]:
                addressBits = finalArr[i][2][2:].replace("'", '')
                # We write down the Object Code
                objectcodeFile.write(addressBits+"\n")

        # We check if we are reading the operations that shouldn't generate Object Code.
        if "RESW" in finalArr[i][1] or "RESB" in finalArr[i][1] or "RESTW" in finalArr[i][1]:
            opBits = "No object code!"
            objectcodeFile.write(opBits+"\n")

        # Starting from here if we have the cases of WORD or BYTE, we do a specific calculation.
        if "WORD" in finalArr[i][1]:
            # We used .split('x')[-1].upper() to neglect the 0X
            # that's in our result then capitalize it.
            addressBits = hex(int(finalArr[i][2])).split('x')[-1].upper()
            objectcodeFile.write(addressBits.zfill(6)+"\n")

        # If we passed by an RSUB
        if "RSUB" in finalArr[i][1]:
            objectcodeFile.write("4C0000"+"\n")

        else:  # If it's not any of the special cases above, we'll do our Object Code normally as below.
            for j in range(len(opArr)):  # We trace through the instruction table
                if finalArr[i][1] in opArr[j][0]:  # Ex: if LDA = LDA
                    opBits = (bin(int(opArr[j][1], 16))[2:].zfill(8))
                    # We take the OP code, convert it to int, then to binary
                    # Fill it to be 8 bits (since OP Code should be 8)
                    # We used [2:] to not read the first two characters of the array because it starts with 0b
                    if ',X' in finalArr[i][2]:  # If we had an xBit
                        xBit = '1'
                    else:
                        xBit = '0'
                    # We trace through the symbol table we generated
                    for m in range(len(symbArr)):
                        # remove the ',X' so we can read the address properly
                        if finalArr[i][2].replace(',X', "") in symbArr[m][0]:
                            addressBits = (  # We convert the value from the Symbol Table
                                bin(int(symbArr[m][1], 16))[2:]).zfill(15)
                    hexObjectCode = hex(  # The final assembly, we add the binary with each other then convert it to hex
                        int((opBits+''+xBit+''+addressBits), 2)).split('x')[-1].upper().zfill(6)

                    # We write down the Object Code we calculated
                    objectcodeFile.write(hexObjectCode+"\n")
    objectcodeFile.close()


def HTE_Record():

    # HTE Record storation
    open('HTE_Record.txt', 'w').close()

    # We assigned lists from the object code for the HTE
    HTE_File = open("HTE_Record.txt", "a")
    ObjectFile = open("ObjectCode.txt", "rt")
    ObjectCodeArray = ObjectFile.readlines()
    print(ObjectCodeArray)

    # To get the header (H.)
    Header = str("H." + ToolsFile.ProgName() + "." +
                 ToolsFile.startingadress().zfill(6) + "." + ToolsFile.ProgLength())
    HTE_File.write(Header+"\n")

    # To get the end (E.)
    End = str("E." + ToolsFile.startingadress().zfill(6))

    # We assigned our initiatives for the loop below
    Count = 0
    TStart = ToolsFile.startingadress()
    Tobj = ""  # A temp that carries T record

    # To get the text (T.)
    for i in range(len(ObjectCodeArray)):  # We loop through the Object Code file
        # The break condition of the Text record
        if ("No object code!" in ObjectCodeArray[i]):
            if Tobj != "":  # As long as Tobj doesn't equal to ""
                HTE_File.write(hex(Count).split(
                    'x')[-1].upper().zfill(2)+""+str(Tobj).replace("\n", "")+"\n")
            Count = 0
            Tobj = ""
        elif (Count == 30):  # The other break condition of the Text record
            if Tobj != "":  # We put it due to a bug not properly executing the lines below
                HTE_File.write(hex(Count).split(
                    'x')[-1].upper().zfill(2)+""+str(Tobj).replace("\n", "")+"\n")
            Count = 3  # RELATED: we put the counter to 3 because we used a word in the T record
            HTE_File.write("T." + LArray[i].zfill(6).replace("\n", "") + ".")
            Tobj = ("."+ObjectCodeArray[i])

        elif i == len(ObjectCodeArray) - 1:  # When the text record reaches the end
            if Tobj != "":
                HTE_File.write(hex(Count).split(
                    'x')[-1].upper().zfill(2) + "" + str(Tobj).replace("\n", "") + "\n")
            HTE_File.write(End)
        else:
            if Count == 0:  # RELATED: the reason why we made the count = 3 above was
                # we wouldn't be able to execute the others below and make a new T-record
                HTE_File.write(
                    "T." + LArray[i].zfill(6).replace("\n", "") + ".")
            Count = Count+3
            Tobj = (Tobj+"."+ObjectCodeArray[i])

    HTE_File.close()
