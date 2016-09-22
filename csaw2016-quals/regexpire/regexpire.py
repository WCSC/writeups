# Chal: Regexpire
import sys
import rstr # First run: sudo pip install rstr
import re
import socket

# RUN WITH PYTHON 2


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
