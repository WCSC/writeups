#!/usr/bin/env python

from pwn import *

s = remote('195.154.53.62', 1337)

s.recvuntil('are a bot\n')
while True:
    line = s.recvline(keepends=False)
    if line.startswith('Question'):
        expr = s.recvline(keepends=False)
        print line, expr,

        a, op, b = expr.rstrip('=').strip().split()
        a, b = int(a), int(b)

        if op == '-':
            res = str(a - b)
        elif op == '+':
            res = str(a + b)
        elif op == '*':
            res = str(a * b)
        elif op == '%':
            res = str(a % b)
        elif op == '/':
            res = str(a / b)
        else:
            print 'Unknown operation \'%s\'' % op
            break

        print res
        s.send(res + '\n')

    else:
        print line
        print s.recvall()
        break
