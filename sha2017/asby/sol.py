import pwn
import string
import time

p = pwn.process("WINEDEBUG=fixme-all /usr/bin/wine asby.exe", shell=True)

charset = []
for c in string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation:
    charset.append(c)

i = 0
flag = charset[i]
while(True):
    time.sleep(.1)
    print(p.recv(timeout=0.3))
    print(flag)
    p.send(flag + '\n')
    time.sleep(.1)
    out = p.recv()
    print(out)
    if 'WRONG' in out:
        i+=1
        flag = flag[:-1] + charset[i]
        continue
    else:
        i=0
        flag = flag + charset[0]
        continue

