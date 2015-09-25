# Forensics 100 - transfer

In this challenge, we are given a pcap file and told that within it contains the flag.

Let's go ahead and load the pcap in WireShark and then do a search to see if the term `flag` is found in any of the packets.

![](http://i.imgur.com/EGaAkLj.png)

Well look at that, the organizers made it easy on use to find what we were looking for.  Let's follow the TCP stream to get a better idea of what we're working with.

![](http://i.imgur.com/MB5ZwhL.png)

Ok now things are starting to fit together.  This instantly jumps out as being a Python script (right? ;-).  But the formatting is off, so we'll need to fix it.  Let's grab the text and paste it into our favorite code editor and clean things up.
```
#!/usr/bin/env python2

import string
import random
from base64 import b64encode, b64decode

FLAG = 'flag{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}'

enc_ciphers = ['rot13', 'b64e', 'caesar']
# dec_ciphers = ['rot13', 'b64d', 'caesard']

def rot13(s):
	_rot13 = string.maketrans( 
	"ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", 
	"NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
	return string.translate(s, _rot13)

def b64e(s):
	return b64encode(s)

def caesar(plaintext, shift=3):
	alphabet = string.ascii_lowercase
	shifted_alphabet = alphabet[shift:] + alphabet[:shift]
	table = string.maketrans(alphabet, shifted_alphabet)
	return plaintext.translate(table)

def encode(pt, cnt=50):
	tmp = '2{}'.format(b64encode(pt))
	for cnt in xrange(cnt):
		c = random.choice(enc_ciphers)
		i = enc_ciphers.index(c) + 1
		_tmp = globals()[c](tmp)
		tmp = '{}{}'.format(i, _tmp)
	return tmp

if __name__ == '__main__':
	print encode(FLAG, cnt=?)
```
Whew, that's better!  Each period that preceeded a line represented a tab (or four spaces).  Also, I added the shebang line so that the script can be interpreted through the command line and removed the text at the end of the stream.  We'll need this later though...

Now we need to figure out what the script is doing and we'll start by examing how the encoding works.  There is an array of names of ciphers created that allows the script to call the functions that they represent.  To make things easier, I'll comment the code to explain:

```
def encode(pt, cnt=50):                 #sets cnt to 50 if no value is passed to cnt
	tmp = '2{}'.format(b64encode(pt))   #the original data is base64 encoded and a 2 is placed at the 
	                                    #beginning of the string. The 2 matches the position+1 in the
	                                    #enc_ciphers array of b64enc
	for cnt in xrange(cnt):             
		c = random.choice(enc_ciphers)  #randomly select which cipher to encode for this loop
		i = enc_ciphers.index(c) + 1    #the index+1 of the random cipher in enc_ciphers
		_tmp = globals()[c](tmp)        #calls the corresponding encoding function from the random selection
		tmp = '{}{}'.format(i, _tmp)    #prepend the encoded data with the cipher number used
	return tmp
```
Pretty straightforward, so decoding should be pretty easy.  What we'll need to do is grab the number at the beginning of our encoded string to find the cipher used during that iteration, and then decode the rest of the string.  This can be scripted to loop until `flag` is found since we don't know how many times the data was encoded.  But first we'll need to have the neccessary functions to do the decoding.

Quickly  
rot13 uses rot13 to decode itself  
base64 can use the builtin python base64decode function  
ceaser is just a shift by a specific number of letters (in this case 3), so we can define the `ceaserd` function to call the `ceaser` function with a shift of -3.  Crafty, huh?  

Now that the decoders are out of the way, it's time to tackle writing the `decode` function.  Again, for simplicities sake, I've commented the code below.

```
def decode(pt):
	while "flag" not in pt:                     #we want to keep looping until 'flag' is in our 
	                                           #decoded string
		cipher = dec_ciphers[int(pt[:1]) - 1]   #This takes the beginning char of our string to
		                                        #determine the cipher used
		text = pt[1:]                           #Our encoded data
		pt = globals()[cipher](text)            #Decodes the data
	return pt
```
Eazy peezy.  Now we just need to add our encoded string to our script and modify main to call our decode function instead of the encode one.  Once that's done we can run our script and get `flag{li0ns_and_tig3rs_4nd_b34rs_0h_mi}`
	
