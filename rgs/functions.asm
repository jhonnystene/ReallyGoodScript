rgs_boot:
	; Setup stack
	cli
	mov ax, 0
	mov ss, ax
	mov sp, 0FFFFh
	sti
	
	; Setup segmenting
	mov ax, 2000h
	mov ds, ax
	mov es, ax
	mov fs, ax
	mov gs, ax
	
	; Figure out boot device stuff
	cmp dl, 0
	je main
	mov [rgs_boot_device], dl
	push es
	mov ah, 8
	int 13h
	pop es
	and cx, 3Fh
	mov [rgs_disk_sectors_per_track], cx
	movzx dx, dh
	add dx, 1
	mov [rgs_disk_sides], dx
	jmp main

rgs_puts:
	; By far the easiest function to write. Just loop over the string and print with int 10h (ah 0Eh, al character)
	pusha ; Save registers
	mov ah, 0Eh ; This tells the BIOS we want to print a character
	
	.loop:
		lodsb ; Read a character from the string
		cmp al, 0 ; Is the character zero? (strings are null terminated)
		je .finish ; Restore regs and return
		
		int 10h ; Print the character in al
		jmp .loop ; Do it again
	
	.finish:
		popa ; Restore registers
		ret ; We're done here

rgs_boot_device db 0
rgs_disk_sectors_per_track dw 18
rgs_disk_sides dw 2
