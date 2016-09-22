# CSAW 2016 Quals
# Regexpire
##### Patricia Wilthew -- USF Whitehatter's Computer Security Club
##### misc -- 100 points
## Description

I thought I found a perfect match but she ended up being my regEx girlfriend.

Note: You can't use newlines inside your match.

`nc misc.chal.csaw.io 8001`

## Solution
The server prints
~~~
Can you match these regexes?
5lfb*(clementine|chair)+[1-9]{8}[eHf]*eK{2}K{2}
~~~
And it gives us some seconds to create a phrase that belongs to that regular expression *

\* Read about regular expressions -> https://msdn.microsoft.com/en-us/library/ae5bf541(v=vs.100).aspx
A possible phrase (or matching phrase) that belongs to that regular expression would be: 5lfbbbclementinechairclementine11111111eHfeKKKK

The problem is that it gives us 10 seconds to come up with a phrase, and as soon as we enter it (which is nearly impossible as we have only 10 seconds), it's gonna ask us to match another regular expression... 

Therefore, we have to write a code that given a regular expression, would generate any phrase that matches it.

I found a pip library called 'rstr' that has a method called 'xeger' that would do what we need it to do.
The only problem was that sometimes it was creating phrases with tabs and newlines, so brad_d added some replacements:
~~~python       
strToMatch = rstr.xeger(pattern)
strToMatch = strToMatch.replace('\n', ' ')
strToMatch = strToMatch.replace('\t', ' ')
~~~

And this is the whole code:
~~~python
# Chal: Regexpire
import sys
import rstr # First run: sudo pip install rstr
import re
import socket

# Connect to server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("misc.chal.csaw.io", 8001))

while 1:
    # Receive 1024 bytes from their server
    resp = s.recv(1024)

	# Print the first message from the server, which is "Can you match ...."
    if resp == 'Can you match these regexes?\n':
        
        print (resp)

    # If their server sends Time Out, exit the program
    elif resp == 'Timeout':

        print (resp)
        sys.exit()

	# If their server sends Irregular, means the last phrase sent was not a match. 
	# Exit program
    elif resp == 'Irregular\n':

        print ('FYI: Last phrase did not match.')
        sys.exit()
    
    # If the server sends a different message from all of the above,
    # let's assume it's the Regular Expression we need
    else:

        # Resp contains the given R.E. 
        print (resp)

        # Pattern contains the R.E. in Python's Syntax
        pattern = re.compile(resp[0:len(resp)-1])

        # If pattern is empty, exit
        if len(list(pattern.pattern)) == 0:
            sys.exit()
        
        # Making sure the phrase doesn't have tabs or newlines
        strToMatch = rstr.xeger(pattern)
        strToMatch = strToMatch.replace('\n', ' ')
        strToMatch = strToMatch.replace('\t', ' ')

        # Send the matching phrase to the server and print it   
        s.send(strToMatch + '\n')
        print (strToMatch + '\n')
~~~
The program will run for a while (1 to 2 minutes), then it will print the flag:
~~~
.....

6{8}z(potato|cat){7}[mjZdcq]*e*[P4n0\DruOD.]{5}9*[i-r]*E[VzF0qQ7\Wl]

66666666zpotatopotatopotatocatcatpotatopotatoqjcqZccjqcdqcZdjdjjZqjqjqZmZeeeeeeeeeeeeee4uD!r9999999999999999999999999999999999999999999999999999999999999999999999999999999jpmlimnqpqiqqkllnmkmpjipprkkrmrpolnlklnmlronrqlmjronkirpqmEq

flag{^regularly_express_yourself$}

flag{regularly_express_yourself}

~~~
