# CSAW 2016 Quals
# The Rock
##### Brad Daniels -- USF Whitehatter's Computer Security Club
##### reversing -- 100 points
## Description

Never forget the people's champ.

## Solution
We're given a binary 64-bit ELF binary. It seems to take an input from STDIN and produce some output. 

~~~
$ ./rock
asdf
-------------------------------------------
Quote from people's champ
-------------------------------------------
*My goal was never to be the loudest or the craziest. It was to be the most entertaining.
*Wrestling was like stand-up comedy for me.
*I like to use the hard times in the past to motivate me today.
-------------------------------------------
Checking....
Too short or too long
~~~

By trial and error, I figured out what length of characters it wanted. When 30 characters are entered, it produces a different response.

~~~

$ perl -e 'print "a"x30' | ./rock
-------------------------------------------
Quote from people's champ
-------------------------------------------
*My goal was never to be the loudest or the craziest. It was to be the most entertaining.
*Wrestling was like stand-up comedy for me.
*I like to use the hard times in the past to motivate me today.
-------------------------------------------
Checking....
You did not pass 0
~~~ 

I decided to test what happens if the first of the 30 characters was correct. 

~~~
$ for c in {a..z}  {A..Z}; do echo -n "$c$(perl -e "print 'a'x29")"| ./rock | grep pass; done;
...
You did not pass 0
You did not pass 0
You did not pass 1
You did not pass 0
You did not pass 0
You did not pass 0
...
~~~

It looks like that worked. By counting we can tell that the first character is 'I'. Lets write something better to brute force the accepting string for us.

~~~python
from subprocess import Popen, STDOUT, PIPE
import re
import string

charset = []
for c in string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation:
        charset.append(c)

inStr = list('0'*30)
curIndex = 0
charIndex = 0

while 1:
        p = Popen("./rock", stdout=PIPE, stderr=PIPE, stdin=PIPE)
        o = p.communicate(input=''.join(inStr))[0]
        m = re.match(".*You did not pass (\d{1,2}).*", o, re.DOTALL)
        print ''.join(inStr)
        if not m:
                print o
                exit()

        newIndex = int(m.group(1))
        if newIndex > curIndex:
                print charset[charIndex]
                curIndex = newIndex
                charIndex = 0
                continue

        inStr[curIndex] = charset[charIndex]
        charIndex = charIndex + 1
~~~

~~~
...
Pass 27
Pass 28
Pass 29
/////////////////////////////////
Do not be angry. Happy Hacking :)
/////////////////////////////////
Flag{IoDJuvwxy\tuvyxwxvwzx{\z{vwxyz}
~~~

