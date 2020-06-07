import os, sys
global strings

strings = []

# Adds the string to the string list if it doesn't exist and returns its index in the list.
def stringIndex(string): # TODO: Newlines
	if(string in strings):
		# Return string position
		return strings.index(string) 
	else:
		# Add string and return position
		strings.append(string)
		return len(strings) - 1 # Minus one because it returns the "human" count rather than the good count.

# Convert one line of RGS into assembly.
def convertLine(line):
	# The instructions and their arguments are seperated by the @ symbol
	command = line.split("@")
	
	# There's almost certainly a better way to compile to ASM, but I'm tired.
	assembly = ""
	
	# TODO: Validate that all arguments are present.
	if(command[0] == "print"):
		assembly += "mov si, string" + str(stringIndex(command[1])) + "\n"
		assembly += "call rgs_puts\n"
		
	elif(command[0] == "comment"):
		assembly += "; " + command[1] + "\n"
	
	elif(command[0] == "asm"):
		assembly += command[1] + "\n"
	
	elif(command[0] == ""):
		assembly = ""
	
	else:
		print("ERROR! Bad instruction: \"" + command[0] + "\"")
		exit()
	
	return assembly
		

print("ReallyGoodScript Compiler")
try:
	filename = sys.argv[1]
	outfile = sys.argv[2]
except:
	print("USAGE: " + sys.argv[0] + " <input filename> <output filename>")
	exit()
	
with open(filename, 'r') as infile:
	fileContents = infile.read()

if("\r\n" in fileContents):
	print("Detected Windows newlines.")
	fileContents = fileContents.split("\r\n")
else:
	print("Detected *nix newlines.")
	fileContents = fileContents.split("\n")

assembly = "BITS 16\njmp rgs_boot\nmain:\n" # Boot process (stack setup, segmenting, etc...) is handled by rgs_boot so we go there first

# Compile to assembly
for line in fileContents:
	assembly += convertLine(line)

# Add all of the strings
for i in range(len(strings)):
	assembly += "string" + str(i) + " db " + strings[i] + ", 13, 10, 0\n"

with open(outfile, 'w') as output:
	output.write(assembly)
