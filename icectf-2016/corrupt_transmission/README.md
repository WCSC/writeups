# IceCTF 2016
# Corrupt Transmission
#### Forensics -- 50 points
# Description
We intercepted this image, but it must have gotten corrupted during the transmission. Can you try and fix it? corrupt.png 

# Solution
As with many CTF challenges, it's a good idea to see what `file` has to say about it. 
~~~
sh$ file corrupt.png
corrupt.png: data
~~~
Since `file` is unable to identify this as a PNG, we know that the [magic numbers](https://en.wikipedia.org/wiki/File_format#Magic_number) are wrong. 

A quick Google search brought me to the [PNG specification](https://www.w3.org/TR/PNG/) which lists the magic numbers in decimal as
~~~
 137 80 78 71 13 10 26 10
~~~

Using bash and `xargs`, we can convert those to hex. 
~~~
sh$ echo "137 80 78 71 13 10 26 10" | xargs printf '%x '
89 50 4e 47 d a 1a a % 
~~~

When we look at the magic numbers in the file, we see that the magic numbers are incorrect.

~~~
sh$ xxd corrupt.png | head -n 3
00000000: 9050 4e47 0e1a 0a1b 0000 000d 4948 4452  .PNG........IHDR
00000010: 0000 01f4 0000 0198 0806 0000 00b4 e010  ................
00000020: ab00 0000 0662 4b47 4400 ff00 ff00 ffa0  .....bKGD.......
~~~

Using Vim as a [simple hex editor](http://vi.stackexchange.com/questions/2232/how-can-i-use-vim-as-a-hex-editor), we can correct the magic numbers:

~~~
sh$ xxd corrupt_fixed.png | head -n 3
00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR
00000010: 0000 01f4 0000 0198 0806 0000 00b4 e010  ................
00000020: ab00 0000 0662 4b47 4400 ff00 ff00 ffa0  .....bKGD.......
~~~

Now when the fixed PNG file is opened in an image viewer, the flag is clearly visible. `IceCTF{t1s_but_4_5cr4tch}`
