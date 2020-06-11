# ReallyGoodScript Compiler
# Convert RGS v2 to Assembly
# TODO: Make it easier to port to different architectures (like anyone's going to use this lol)
# TODO: Write a help function
# TODO: Add file importing
# TODO: Finish variable support

import sys

# Variable types
varTypeInt = 0
varTypeLong = 1
varTypeString = 2

global variables
variables = []

class Variable:
	def __init__(self, name, value, varType):
		self.name = name
		self.value = value
		self.varType = varType
		
	def generateASMString(self):
		string = self.name + " "
		
		# Figure out what data type to use (byte, word, etc...)
		if(self.varType == varTypeInt or self.varType == varTypeString):
			string += "db "
		
		elif(self.varType == varTypeLong):
			string += "dw "
		
		# Write the variable data.
		if(self.varType == varTypeString):
			# In the case of a string, write quotes and null-terminate.
			string += str(self.value) + ", 0"
			
		else:
			# Otherwise just write the data.
			string += str(self.value)
		
		return string

# For strings that aren't meant to be modified.
global strings
strings = []

def stringIndex(string):
	if(string in strings):
		# Return string position
		return strings.index(string) 
	else:
		# Add string and return position
		strings.append(string)
		return len(strings) - 1 # Minus one because it returns the "human" count rather than the good count.

# WHOOOO BOYYYY
# This parses a line out to an array of arguments. Think split() if split() respected strings and comments.
# This is the only useful thing in the entire codebase. For some reason I thought this would be *much*
# more difficult, this is why v1 had the Syntax of the Masochist(tm)
def parseLine(line):
	if(line.startswith(";")):
		return line
		
	line = line.split(" ")
	command = []
	
	# We're gonna jump around a bit so a for loop won't work here.
	# Or maybe it is and I just never learned C-style for loops in Python.
	i = 0
	while(i != len(line)):
		currentArg = ""
		
		# Check if we're starting a string
		if(line[i].startswith("\"")):
			if(line[i].endswith("\"")):
				currentArg = line[i]
				i += 1
				
			else:
				currentArg += line[i]
				i += 1
				while(not line[i].endswith("\"")):
					currentArg += " " + line[i]
					i += 1
				
				# The above while loop isn't gonna add the last bit.
				currentArg += " " + line[i]
				i += 1
		
		else:
			currentArg = line[i]
			i += 1
		
		command.append(currentArg)
	
	return command

# Compilation function
def compileLine(line, lineIndex):
	line = parseLine(line)
	assembly = ""
	
	# Variables
	if(line[0] == "int"):
		var = Variable(line[1], int(line[3]), varTypeInt)
		variables.append(var)
		
	elif(line[0] == "long"):
		var = Variable(line[1], int(line[3]), varTypeLong)
		variables.append(var)
	
	elif(line[0] == "string"):
		var = Variable(line[1], str(line[3]), varTypeString)
		variables.append(var)
		
	# Print string
	elif(line[0] == "print"):
		# Are we making a new string constant? Spoiler: Yes. This function doesn't check for variables (yet)
		if(line[1].startswith("\"")):
			assembly += "mov si, string" + str(stringIndex(line[1])) + "\n"
			assembly += "call rgs_print"
		else:
			# TODO: Check for variables before erroring
			print("ERROR on line " + str(lineIndex) + ": Passed a non-string to print")
			exit()
	
	# Clear screen
	elif(line[0] == "clear"):
		assembly += "call rgs_clear"
	
	# Comment
	elif(line[0].startswith(";")):
		assembly += line
	
	# Empty line
	elif(line[0] == ""):
		assembly = ""
	
	else:
		print("ERROR on line " + str(lineIndex) + ": Invalid command: " + line[0])
	
	return assembly

# +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
#
# Load and compile a file
#
# +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=

# Check to make sure we have an input file
try:
	infilename = sys.argv[1]
	outfilename = sys.argv[2]
	
except:
	print("Usage: rgs-compiler <input filename> <output filename>")
	exit()

try:
	with open(infilename, 'r') as infile:
		code = infile.read()
except:
	print("ERROR! Couldn't read input file!")
	exit()

# Setup header with disk buffer and call vectors
print("Loading call vectors...")
assembly = "BITS 16\ndisk_buffer equ 24576\n"
try:
	with open("rgs/callvectors.asm", 'r') as vectorFile: # TODO: Make callvectors.asm an optional argument
		assembly += vectorFile.read() + "\n"
		
except:
	print("ERROR! Couldn't read call vectors (rgs/callvectors.asm)")
	exit()

assembly += "main:\n"
code = code.split("\n")
for line in range(len(code)):
	assembly += compileLine(code[line], line) + "\n"
	
# Finally, include all of the code for the rest of the functions
print("Importing functions...")
try:
	with open("rgs/functions.asm", 'r') as functionfile: # TODO: Make functions.asm an optional argument
		assembly += functionfile.read() + "\n"
except:
	print("ERROR! Couldn't read function include file (rgs/functions.asm)")
	exit()

for var in variables:
	assembly += var.generateASMString() + "\n"
	
for i in range(len(strings)):
	assembly += "string" + str(i) + " db " + strings[i] + ", 0\n"

try:
	with open(outfilename, 'w') as outfile:
		outfile.write(assembly)
except:
	print("ERROR! Couldn't write assembly file!")
	exit()

