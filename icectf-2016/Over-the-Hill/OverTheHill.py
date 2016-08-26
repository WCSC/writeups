#!/usr/bin/env python
import numpy as np
import math
from numpy import linalg

def modMatInv(A,p):       # Finds the inverse of matrix A mod p
  n=len(A)
  A=np.matrix(A)
  adj=np.zeros(shape=(n,n))
  for i in range(0,n):
    for j in range(0,n):
      adj[i][j]=((-1)**(i+j)*int(round(linalg.det(minor(A,j,i)))))%p
  return (modInv(int(round(linalg.det(A))),p)*adj)%p

def modInv(a,p):          # Finds the inverse of a mod p, if it exists
  for i in range(1,p):
    if (i*a)%p==1:
      return i
  raise ValueError(str(a)+" has no inverse mod "+str(p))

def minor(A,i,j):    # Return matrix A with the ith row and jth column deleted
  A=np.array(A)
  minor=np.zeros(shape=(len(A)-1,len(A)-1))
  p=0
  for s in range(0,len(minor)):
    if p==i:
      p=p+1
    q=0
    for t in range(0,len(minor)):
      if q==j:
        q=q+1
      minor[s][t]=A[p][q]
      q=q+1
    p=p+1
  return minor


alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789_{}"
mod = len(alphabet)

matrix = [[54, 53, 28, 20, 54, 15, 12, 7],
          [32, 14, 24, 5, 63, 12, 50, 52],
          [63, 59, 40, 18, 55, 33, 17, 3],
          [63, 34, 5, 4, 56, 10, 53, 16],
          [35, 43, 45, 53, 12, 42, 35, 37],
          [20, 59, 42, 10, 46, 56, 12, 61],
          [26, 39, 27, 59, 44, 54, 23, 56],
          [32, 31, 56, 47, 31, 2, 29, 41]]

ciphertext = "7Nv7}dI9" + "hD9qGmP}" + "CR_5wJDd" + "kj4CKxd4" + "5rko1cj5" + "1DpHPnND" + "b__EXDot" + "SRCP8ZCQ"

ct = [ciphertext[i:i+8] for i in range(0, len(ciphertext), 8)]

mm = np.matrix(matrix)
mi = modMatInv(matrix, mod)


c = np.matrix([[alphabet.index(x) for x in c] for c in ct]).tolist()
ctrans = np.matrix(c).transpose().tolist()


def solve(strng):
	msg = np.matrix([alphabet.index(c) for c in strng]).transpose()
	msg = np.remainder(np.dot(mi, msg), mod).tolist()

	flag = ""
	for x in [alphabet[int(c[0])] for c in msg]:
		flag += x
	return flag

flag = ""
for x in ct:
	flag += solve(x)

print flag
