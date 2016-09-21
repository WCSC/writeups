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
