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

# First, we need to make sure we have all of the arguments we need.
try:
	filename = sys.argv[1]
	outfile = sys.argv[2]
except:
	print("USAGE: " + sys.argv[0] + " <input filename> <output filename>")
	exit()

# We do. Load in the input file:
print("Loading input file...")
try:
	with open(filename, 'r') as infile:
		fileContents = infile.read()
except:
	print("ERROR! Couldn't read input file (" + filename + ")")
	exit()

# Detect what kind of newlines we have.
print("Detecting newlines...")
if("\r\n" in fileContents): # With carriage return?
	print("Detected Windows newlines.")
	fileContents = fileContents.split("\r\n")
else: # Or without carriage return?
	print("Detected *nix newlines.")
	fileContents = fileContents.split("\n")

# Basic header
assembly = "BITS 16\ndisk_buffer equ 24576\n"

# We need to include the call vectors or applications won't be able to interface w/ the OS
print("Loading call vectors...")
try:
	with open("rgs/callvectors.asm", 'r') as vectorFile: # TODO: Make callvectors.asm an optional argument
		assembly += vectorFile.read() + "\n"
except:
	print("ERROR! Couldn't read call vectors (rgs/callvectors.asm)")
	exit()

# Main function. This gets called by rgs_boot after everything has been set up.
assembly += "main:\n"

# Run through each line and convert it to assembly
print("Compiling to Assembly...")
for line in fileContents:
	assembly += convertLine(line)

# Add all of the strings to the ASM file
print("Adding strings...")
for i in range(len(strings)):
	assembly += "string" + str(i) + " db " + strings[i] + ", 13, 10, 0\n"
	
# Finally, include all of the code for the rest of the functions
print("Importing functions...")
try:
	with open("rgs/functions.asm", 'r') as functionfile: # TODO: Make functions.asm an optional argument
		assembly += functionfile.read() + "\n"
except:
	print("ERROR! Couldn't read function include file (rgs/functions.asm)")
	exit()

# Write out all of the code to assembly.
print("Saving...")
try:
	with open(outfile, 'w') as output:
		output.write(assembly)
except:
	print("ERROR! Couldn't write to output file (outfile)")
	exit()

print("Success! Outputted assembly code to " + outfile + ".")
