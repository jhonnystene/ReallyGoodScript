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

assembly = "BITS 16\n"

# We need to include the call vectors or applications won't be able to interface w/ the OS
try:
	with open("rgs/callvectors.asm", 'r') as vectorFile: # TODO: Make callvectors.asm an optional argument
		assembly += vectorFile.read() + "\n"
except:
	print("ERROR! Couldn't read call vectors (rgs/callvectors.asm)")
	exit()

assembly += "main:\n" # Boot process (stack setup, segmenting, etc...) is handled by rgs_boot so we go there first

# Compile to assembly
for line in fileContents:
	assembly += convertLine(line)

# Add all of the strings
for i in range(len(strings)):
	assembly += "string" + str(i) + " db " + strings[i] + ", 13, 10, 0\n"
	
# Finally, include the rest of the ASM needed for the OS
try:
	with open("rgs/functions.asm", 'r') as functionfile: # TODO: Make functions.asm an optional argument
		assembly += functionfile.read() + "\n"
except:
	print("ERROR! Couldn't read function include file (rgs/functions.asm)")
	exit()

try:
	with open(outfile, 'w') as output:
		output.write(assembly)
except:
	print("ERROR! Couldn't write to output file (outfile)")
	exit()
