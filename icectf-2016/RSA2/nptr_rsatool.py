#!/usr/bin/python

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

print('Give me your e value:')
e = input()
print('Input your p value:')
p = input()
print('Input your q value:')
q = input()

print('Solving for the d. Give me a sec, kay ;)')
p -= 1
q -= 1
phi = p * q
d = modinv(e,phi)
print('Found your d, sweetheart:')
print(hex(d))
