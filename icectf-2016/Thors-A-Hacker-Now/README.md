# IceCTF Thor
## Solution By: Nullp0inter

# Thor's A Hacker Now -Misc- 55pts
Thor has been staring at this for hours and he can't make any sense out of it, can you help him figure out what it is? thor.txt

# Solution:
The challenge gives us a text file that is quite obviously a hex dump of something. The file
is pretty large so I won't post it directly here but its hosted in the same directory here on github
just in case they ever take it down from IceCTFs site. In any case...

If you pay attention to the first 4 letters on the right, you see it says "LZIP".  That happens to 
be the file type, it is simply the hexdump of an lzipped archive. So first you have to go and
download lzip. If you are using ubuntu, then simply do `sudo apt-get install lzip`. Once you have
lzip installed, copy thor.txt to a directory then do `xxd -r thor.txt | lzip -d > thor.out`. This
produces a JPEG image called thor.out. Simply open that image and there is your flag:

`IceCTF{h3xduMp1N9_l1K3_A_r341_B14Clh47}`
