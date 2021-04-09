# Welcome to the SIC project for the Systems Programming course
# Supervised by: Dr. Sherine Nagi & Eng. Esraa Khattab
# Group canditates:
# Mazen Mamdouh - 17100759
# Ibrahim M. Kabbash - 17100399

import re
import ToolsFile
import pass1
import pass2

mainArray = ToolsFile.appendall()
print(mainArray)
pass1.locationCounter()
pass1.SymbolTable()
pass2.ObjectCode()
pass2.HTE_Record()
