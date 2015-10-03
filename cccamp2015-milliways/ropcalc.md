# ROPcalc writeup

ropcalc was fun. You're given the binary and a python server to wrap it. The server calls the binary, you provide stdin, and it simply returns to whatever address you supply. The server then checks the return value and verifies whether or not it matches the expected number.

From the server code:

```python
EXPRESSIONS = ( 
    "$rax + $rbx",
    "$rax + $rbx + 1337",
    "$rax * $rbx",
    "$rax * (31337 + $rbx)",
    "$rcx + 23 * $rax + $rbx - 42 * ($rcx - 5 * $rdx - $rdi * $rsi) - $r8 + 2015",
)
```

So you need to create a ROP chain that evaluates those expressions, then return the value in RAX. It's not difficult, but it's an exercise in x64 ROP. And gadget searching, of course. The server goes through each individual expression and checks it, so we want a rop chain to implement each expression. Also, the server takes a hex encoding of the payload (rop chain).

The first expression is `$rax + $rbx`. I do a `grep "add rax, rbx" calc.rop` and find a gadget:


```
0x0000000000400b30 : add rax, rbx ; ret
```

This looks like a nice gadget. And it'll return with `RAX` being the result, so we're golden.

```python
rop = ''
rop += p64(0x0000000000400b30)
r.sendline(rop.encode('hex'))
```

The next one was to do `$rax + $rbx + 1337`. For this, I decided to just pop the value into a register and add it that way. `RBX` is fine as a temporary register... A couple greps later, and here's a chain:

```
0x0000000000400b30 : add rax, rbx ; ret
0x00000000004008d0 : pop rbx ; ret
1337
0x0000000000400b30 : add rax, rbx ; ret
```

Notice that I'm simply popping 1337 from the stack (into `RBX`) and then adding that. 

```python
rop += p64(0x0000000000400b30)
rop += p64(0x00000000004008d0)
rop += p64(1337)
rop += p64(0x0000000000400b30)
r.sendline(rop.encode('hex'))
```

Next one you needed to multiply (`$rax * $rbx`)! That's crazy stuff, so I had to change my grep up a little. `grep "mul rax, rbx" calc.rop` gave me:

```
0x0000000000400b50 : imul rax, rbx ; ret
```

So...

```python
rop += p64(0x0000000000400b50)
r.sendline(rop.encode('hex'))
```

Now for the next one (`$rax * (31337 + $rbx)`) we need proper order of operations. So I need a temporary register. It can't be `RAX` or `RBX`, so I `egrep "add r.x, rbx" calc.rop`. And I decided to use:

'''
0x00000000004013a0 : add rcx, rbx ; ret
'''

Now everything is as easy as before - put 31337 into `RCX`, add it to `RBX`, then `imul` that with `RAX`. 

```
0x0000000000400900 : pop rcx ; ret
31337
0x00000000004013a0 : add rcx, rbx ; ret
0x0000000000400ba0 : imul rax, rcx ; ret
```

Python:

```python
rop += p64(0x0000000000400900)
rop += p64(31337)
rop += p64(0x00000000004013a0)
rop += p64(0x0000000000400ba0)
r.sendline(rop.encode('hex'))
```

Now this last one was a pain... This:

```
$rcx + 23 * $rax + $rbx - 42 * ($rcx - 5 * $rdx - $rdi * $rsi) - $r8 + 2015
```

had lots of order-of-operations problems. I decided to just do stuff in semi-random order - it's nice that x64 has lots of registers to allow for temp storage <3. After lots of grepping and soul searching (comments and all from my notes):

```
0x0000000000400a20 : pop r10 ; ret          stage 23
23
0x0000000000400d80 : imul rax, r10 ; ret    23 * rax
0x0000000000400b80 : add rax, rcx ; ret     ^this + rcx
0x0000000000400b30 : add rax, rbx ; ret     ^this + rbx

stuffs:
0x0000000000400a20 : pop r10 ; ret
5
0x00000000004019b0 : imul rdx, r10 ; ret
0x0000000000401400 : sub rcx, rdx ; ret

0x00000000004020e0 : imul rdi, rsi ; ret
0x00000000004014a0 : sub rcx, rdi ; ret

0x0000000000400a20 : pop r10 ; ret
42
0x00000000004015a0 : imul rcx, r10 ; ret

0x0000000000400b90 : sub rax, rcx ; ret
0x0000000000400cd0 : sub rax, r8 ; ret
0x0000000000400a20 : pop r10 ; ret
2015
0x0000000000400d60 : add rax, r10 ; ret
```

Yay python:

```python
rop += p64(0x0000000000400a20)
rop += p64(23)
rop += p64(0x0000000000400d80)
rop += p64(0x0000000000400b80)
rop += p64(0x0000000000400b30)

rop += p64(0x0000000000400a20)
rop += p64(5)
rop += p64(0x00000000004019b0)
rop += p64(0x0000000000401400)

rop += p64(0x00000000004020e0)
rop += p64(0x00000000004014a0)

rop += p64(0x0000000000400a20)
rop += p64(42)
rop += p64(0x00000000004015a0)

rop += p64(0x0000000000400b90)
rop += p64(0x0000000000400cd0)
rop += p64(0x0000000000400a20)
rop += p64(2015)
rop += p64(0x0000000000400d60)
r.sendline(rop.encode('hex'))

r.interactive()
```

A bit tedious, but fun nonetheless. Could be a good one to teach basic x64 ROP.
