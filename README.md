# ReallyGoodScript
I'm sorry.

### Requirements:
- Python 3.7 or later
- NASM (or a compatible assembler)
- A bootloader of your choice
- Basic command line knowledge

### Compiling:
`rgs-compiler [input file] [output file] [optional arguments]`

#### Optional arguments:
- `--windows-newlines` forces the compiler to use the Windows `\r\n` newline format when parsing the file.
- `--unix-newlines` forces the compiler to use the *nix `\n` newline format when parsing the file.
- `--print-output` makes the compiler print the assembly code, in its entirety, to the console.

### Syntax:
Functions and arguments are seperated by the `@` symbol. For example:

`print@"Hello, world!"`

Good luck.

### Functions
#### print
Takes one argument- a string in double quotes.
#### comment
Takes one argument- your comment.
This will also be put on the assembly file.
#### asm
Takes one argument- a line of assembly in Intel syntax.
This will be put directly in the assembly as you write it.

### Todo:
- Make the syntax less GARBAGE
- Add enough functions to be useful for more than "Hello, World!"
- Write a dedicated bootloader
- Direct export to a .img file
