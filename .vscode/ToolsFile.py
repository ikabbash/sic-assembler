import re
# Below are a bunch of methods for cleaning the code from comments
# before exectuion.


fin = open("testprogram.txt", "rt")
fout = open("program.txt", "wt")
for line in fin:
    fout.write(re.sub('\s+', ',', line))
    fout.write('\n')

fin.close()
fout.close()

with open("program.txt") as textFile:
    progArr = [line.split(',') for line in textFile]
with open("instructions.txt") as textFile:
    instructions = [line.split(' ') for line in textFile]

# To check the instructions for the unique. #
# ones and the one in the instruction text. #

def checkinstructions(teststring):
    i = 0
    found = False
    if teststring in "RESB":
        found = True
    if teststring in "BYTE":
        found = True
    if teststring in "WORD":
        found = True
    if teststring in "RESW":
        found = True
    while i in range(len(instructions)):
        if teststring in instructions[i][0]:
            found = True
        i = i + 1
    return found


# This function will check if there's a comment
# in the OPERATIONS, and if there is we created a new
# array to store the instructions that don't
# start with a comment
def operations():
    opArray = []
    for i in range(1,len(progArr)-1):  # keda wa2feen 3and el row
        if not '.' in progArr[i][1]:
            if not '.' in progArr[i][0]:
                if checkinstructions(progArr[i][1]) == True:
                    opArray.append(progArr[i][1])
                elif checkinstructions(progArr[i][1]) == False:
                    print("ERROOOOOOOOOOOOOR WRONG INSTRUCTIOOOOOOOOOON!!!!")
                    break
    return opArray


# This function will check if there's a comment
# in the VARIABLES, and if there is we created a new
# array to store the instructions that don't
# start with a comment


def variables():
    varArray = []
    for i in range(1,len(progArr)-1):  # keda wa2feen 3and el row
        if not '.' in progArr[i][2]:
            if not '.' in progArr[i][1]:
                if not '.' in progArr[i][0]:
                    varArray.append(progArr[i][2])
    return varArray


# This function will check if there's a comment
# in the INDEXES, and if there is we created a new
# array to store the instructions that don't
# start with a comment


def indexs():
    indexsArray = []
    for i in range(1,len(progArr)-1):  # keda wa2feen 3and el row
        if not '.' in progArr[i][0]:
            indexsArray.append(progArr[i][0])
    return indexsArray


# We take all the lists of indexes, operations and
# variables and store them in the array the program
# will execute on.
def appendall():
    finalArray = []
    finalArray = list(zip(indexs(),operations(), variables()))
    return finalArray
