#!/usr/bin/env python3

import socket
import re
import itertools
import sys

# From https://docs.python.org/3/library/itertools.html#itertools-recipes
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

def xor(mat_a, mat_b):
    res = [[0]*3 for i in range(3)]
    for col in range(3):
        for row in range(3):
            res[row][col] = mat_a[row][col] ^ mat_b[row][col]

    return res;

# matrix transpose
def t(mat):
    return [list(row) for row in zip(*mat)]

# Connect
s = socket.socket()
s.connect(('vermatrix.pwn.democrat', 4201))

# Get challenge text
text = s.recv(4096).decode('utf-8')
print(text, end='\n')

# Get seed
seed = re.match('SEED: (.+)', text.split('\n')[0]).groups()[0]
print('seed: {}'.format(seed))
seed_mats = [[[0]*3 for i in range(3)] for j in range(len(seed)//9)]
for mat in range(len(seed)//9):
    for row in range(3):
        for col in range(3):
            seed_mats[mat][row][col] = ord(seed[mat*9 + row*3 + col])
print('seed matrices: {}'.format(seed_mats))

# Get encoded result into block
encoded = [[int(i) for i in line.split()] for line in text.rstrip('\n').split('\n')[1:]]
print('encoded result given to us: {}'.format(encoded))


# Get IV
current_block = encoded
for seed_block in reversed(seed_mats):
    current_block = t(xor(current_block, seed_block))
print('\nhopefully the IV: {}'.format(current_block))

# Encode IV
encoded_iv = ','.join(str(i) for i in list(itertools.chain(*current_block)))
print('encoded IV: {}'.format(repr(encoded_iv)))

s.send((encoded_iv + '\n').encode('utf-8'))
print(s.recv(4096).decode('utf-8'))
