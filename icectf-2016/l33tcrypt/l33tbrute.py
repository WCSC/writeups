#!/usr/bin/env python
from pwn import *
from base64 import b64decode as dec
from base64 import b64encode as enc

context.log_level = 'error'

host = "localhost"
# host = "l33tcrypt.vuln.icec.tf"
port = 6001

guess_bytes = [chr(x) for x in range(256)]
block1_plaintext = 'l33tserver pleas'

flag = ''

def recv_line(c):
    c.recvline()
    c.recvline()
    c.recvline()
    d = c.recvline()
    return dec(d)

def send_line(c, data):
    c.sendline(enc(data))

def check_guess(i, goal):
    for x in guess_bytes:
        c = remote(host, port)
        send = block1_plaintext + 'e' * (63 - i) + flag + x
        send_line(c, send)
        guess = recv_line(c)[0x40:0x50]
        c.close()
        if  guess == goal:
            return x

for i in range(64):
    c = remote(host, port)
    send = block1_plaintext + 'e' * (63 - i)
    send_line(c, send)
    goal = recv_line(c)[0x40:0x50]
    c.close()
    b = check_guess(i, goal)
    try:
        flag += b
        print "flag so far:", flag
    except:
        print flag
        sys.exit()
