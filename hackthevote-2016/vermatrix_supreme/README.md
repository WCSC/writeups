# Vermatrix Supreme - [100] Crypto

**Kevin Orr** - [USF Whitehatters Computer Security Club (WCSC)](https://ctftime.org/team/315)


### Description

> Working in IT for a campaign is rough; especially when your candidate uses his password as
> the IV for your campaign's proprietary encryption scheme, then subsequently forgets it.
> See if you can get it back for him. The only hard part is, he changes it whenever he feels
> like it.
>
> `nc vermatrix.pwn.democrat 4201`
>
> [handout](https://s3.amazonaws.com/hackthevote/handout.4838bbdb8619b3a581352c628c6b0b86475b94c9519347a520c90cf1822351ae.py)
>
> author's irc nick: negasora


### Examination

The flag given on line 3 of `handout.py`:  `flag{1_sw34r_1F_p30Pl3_4cTu4lLy_TrY_Th1s}`.
No it's not. I wasted my time.

When the script is run, it outputs the current seed and a 3x3 matrix of integers.
After reading a few times through the script, it becomes apparent that it implements
a [block cipher](https://en.wikipedia.org/wiki/Block_cipher) of sorts.
Since the plaintext and true IV are completely null, the
[mode of operation](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation) could be 
classified as a CBC, PCBC, CFB, or OFB (and possibly others). In addition, every block of
ciphertext except the last is ignored. Regardless, examining the function `chall()`,
it is characterized by the following relationship:

	C[0] := zeros()
	C[i] := E(C[i-1], key[i])

where `E(C, k)` is the block cipher, `key[0] := IV`, and `key[1:] := seed`.

Examining the block cipher in the function `fixmatrix(matrixa, matrixb)`, specifically line 33:

	out[cn][rn] = (int(matrixa[rn][cn])|int(matrixb[cn][rn]))&~(int(matrixa[rn][cn])&int(matrixb[cn][rn]))

If we extend the bitwise operations `|`, `&`, and `~` so that they can operate elementwise
on a matrix, we can rewrite the assignment above in the psuedocode:

	out = (transpose(matrixa) | matrixb) & ~(transpose(matrixa) & matrixb)

It's immediately apparent that this "encryption cipher" is a simple `xor`, i.e.

	out = transpose(matrixa) ^ matrixb


### Solution

We can rewrite the relationships before with this new knowledge:

	C[0] := zeros()
	C[i] := xor(C[i-1], key[i])

This means that

	C[i-1] := xor(C[i], key[i])

Also:

	C[i-1] := xor(C[i], key[i])
	key[i] := xor(C[i], C[i-1])
	key[0] (=IV) := xor(C[1], C[0]) = xor(C[1], zeros()) = C[1]


So our solution is simple: `xor` the end of the key to the result matrix, use that result
as the new end of the key, and recurse, until reaching C[1], which should equal the IV!
Running [`sol.py`](sol.py) reverses the encryption and obtains the IV. It then sends this
IV (encoded as a string of comma-delimited integers) and outputs the flag that the server
sends back.

### Flag

`flag{IV_wh4t_y0u_DiD_Th3r3}`
