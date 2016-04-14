Dance 
=====
Exploitation - 55 Points

About
-----
We are given the binary running on a server that we connect to using netcat. Upon connecting you see something similar to this:

```
Welcome to the pro club. you just paid a door fee and have no respect. earn ur cred on the dancefloor!
give us ur sick dance moves like so:
whip,naenae,whip,whip,naenae<ENTER>

whip,naenae,whip,naenae,whip
do the whip!
   (;P)
 8=/||\_
_/¯    ¯\_
do the naenae
(\)
  \(:O)
   /||\_
_/¯    ¯\_
do the whip!
   (;P)
 8=/||\_
_/¯    ¯\_
do the naenae
(\)
  \(:O)
   /||\_
_/¯    ¯\_
do the whip!
   (;P)
 8=/||\_
_/¯    ¯\_

cool dance! come again!
```
You have input here so may as well start looking at the buffer.

Solved By 
----------
nullp0inter

How to solve 
------------
Honestly, when I solved this challenge I was (in the spirit of the ctf) RIGGITY-RIGGITY-REKT SON! (I had all but chugged an entire bottle of wine). Being that I was not of sound mind, I really didn't want to bother exploring the binary to find out how big the buffer was, instead I just used pattern generation with Ragg2 and sent varying lengths. Ultimately I solved this one on accident, when I was wasted, just trying to figure out how big the buffer was using a binary search sort of method. If you send it approximately 80 A's (I sent it a pattern of length 80), it spits out the flag and tells you that you are a gurl who can dance.

Ragg2 is great for analysis as it generates patterns of whatever length you like then can search for them. You can quickly generate a pattern with:
`ragg2 -P <length_you_want_the_pattern_to_be_so_80_in_this_case> -r`

Being that I don't have the binary, didn't write down the flag, and the challenges are all down at this point, you'll just have to settle for

`SUN{this_was_the_flag}` 
