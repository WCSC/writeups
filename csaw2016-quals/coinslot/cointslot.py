import socket
import re

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("misc.chal.csaw.io", 8000))

resp = s.recv(1024)
print resp,

while len(resp) > 0:

	m = re.match(".*\$(\d{1,50})\.(\d\d).*", resp, re.DOTALL)
        if m:
	    change = int(m.group(1)) * 100 + int(m.group(2))
        else:
            resp = s.recv(1024)
            print resp
            quit()

	denoms = [1000000, 500000, 100000, 50000, 10000, 5000, 2000, 
                1000, 500, 100, 50, 25, 10, 5, 1]

	for denom in denoms:
		num = 0
		num = change/denom
                print num
		if num > 0: 
			change = change - (denom * num)
		s.send(str(num) + '\n')
		resp = s.recv(1024)
	        print resp,

