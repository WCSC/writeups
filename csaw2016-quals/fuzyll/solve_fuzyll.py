#!/usr/bin/python

chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "B", "C", "D",
		 "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T",
		 "V", "W", "X", "Y", "Z", "b", "c", "d", "f", "g", "h", "j", "k",
		 "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]

message = "JQSX2NBDykrDZ1ZHjb0BJt5RWFkcjHnsXvCQ4LL9H7zhRrvVZgLbm2gnXZq71Yr6T14tXNZwR1Dld2Y7M0nJsjgvhWdnhBll5B8w0VP3DFDjd3ZQBlcV4nkcFXBNzdPCSGMXQnQ7FTwcwbkG6RHX7kFHkpvgGDDGJvSDSTx7J6MFhRmTS2pJxZCtys4yw54RtK7nhyW6tnGmMs1f4pW6HzbCS1rSYNBk3PxzW9R1kJK54R2b7syLXd7x1Mr8GkMsg4bs3SGmj3rddVqDf4mTYq1G3yX1Rk9gJbj919Jw42zDtT2Jzz4gN0ZBmXPsBY9ktCLPdFrCPZ33NKJy5m37PK0GLXBxZz9k0cjzyt8x199jMsq7xrvNNgDNvgTbZ0xjZzHhkmrWrCmD7t4q4rWYFSJd4MZBxvnqc0VgGzdkq8jSJjnwcynq9VfH22WCQSdPKw48NkZL7QKGCT94pSb7ZSl2G6W37vBlW38q0hYDVcXTTDwr0l808nDPF6Ct1fPwKdNGKbRZ3Q3lHKMCYBC3w8l9VRjcHwMb1s5sMXM0xBvF8WnWn7JVZgPcXcwM2mDdfVkZsFzkrvVQmPfVNNdk9L5WtwDD8Wp9SDKLZBXY67QkVgW1HQ7PxnbkRdbnQJ4h7KFM2YnGksPvH4PgW2qcvmWcBz62xDT5R6FXJf49LPCKL8MQJLrxJpQb7jfDw0fTd00dX1KNvZsWmfYSTl1GxPlz1PvPSqMTQ036FxSmGb6k42vrzz2X90610Z"

def decode(i):
	if i == 0:
		return chars.index(message[i])
	else: 
		return 52*decode(i-1) + chars.index(message[i])

inpt = decode(len(message) -1)

flag = []
i = len(message)
while i >= 0: 
	for c in range(32,126):
		n = (inpt - c)*1000000l/256
		if int(str(n)[-6:]) == 0 or n == 0:
			flag.append(chr(c))
			inpt = (inpt - c)/256
			break
	i -= 1

print ''.join(flag)[::-1]

