#!/usr/bin/env python2.7
import md5
md5s = [0x831daa3c843ba8b087c895f0ed305ce7,
        0x6722f7a07246c6af20662b855846c2c8,
        0x5f04850fec81a27ab5fc98befa4eb40c,
        0xecf8dcac7503e63a6a3667c5fb94f610,
        0xc0fd15ae2c3931bc1e140523ae934722,
        0x569f606fd6da5d612f10cfb95c0bde6d,
        0x068cb5a1cf54c078bf0e7e89584c1a4e,
        0xc11e2cd82d1f9fbd7e4d6ee9581ff3bd,
        0x1df4c637d625313720f45706a48ff20f,
        0x3122ef3a001aaecdb8dd9d843c029e06,
        0xadb778a0f729293e7e0b19b96a4c5a61,
        0x938c747c6a051b3e163eb802a325148e,
        0x38543c5e820dd9403b57beff6020596d]

print 'Can you turn me back to python ? ...'
flag = raw_input('well as you wish.. what is the flag: ')

if len(flag) > 69:
    print 'nice try'
    exit()

if len(flag) % 5 != 0:
    print 'nice try'
    exit()

for i in range(0, len(flag), 5):
    s = flag[i, i+5]
    if int('0x'+md5.new(s).hexdigest(), 16) != md5s[i/5]:
        print 'nice try'
        exit()

print 'Congratz now you have the flag.'
