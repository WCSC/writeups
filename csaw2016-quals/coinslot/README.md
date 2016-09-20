# CSAW 2016 Quals
# coinslot
##### Brad Daniels -- USF Whitehatter's Computer Security Club
##### misc -- 25 points
## Description

\#Hope \#Change \#Obama2008

`nc misc.chal.csaw.io 8000`

## Solution
The server gives us the following. 
~~~
sh$ nc misc.chal.csaw.io 8000
$0.03
$10,000 bills: 0
$5,000 bills: 0
$1,000 bills: 0
$500 bills: 0
$100 bills: 0
0$50 bills: 0
$20 bills: 0
$10 bills: 0
$5 bills: 0
$1 bills: 0
half-dollars (50c): 0
quarters (25c): 0
dimes (10c): 0
nickels (5c): 0
pennies (1c): 3
correct!
$0.01
$10,000 bills: 1
...
~~~
It's a classic [change-making problem](https://en.wikipedia.org/wiki/Change-making_problem)!

This was relatively straightforward to code a solution to, however I did run into some issues with Python occasionally casting the change string to an incorrect float, so I opted to convert everything to  integers (# of pennies). 

~~~python
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
~~~
15 minutes later, we get the flag: 
~~~
...
$81667.36
$10,000 bills:  8
$5,000 bills:  0
$1,000 bills:  1
$500 bills:  1
$100 bills:  1
$50 bills:  1
$20 bills:  0
$10 bills:  1
$5 bills:  1
$1 bills:  2
half-dollars (50c):  0
quarters (25c):  1
dimes (10c):  1
nickels (5c):  0
pennies (1c):  1
correct!
flag{started-from-the-bottom-now-my-whole-team-fucking-here}
~~~
