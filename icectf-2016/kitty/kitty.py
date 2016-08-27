#!/usr/bin/python
# Nullp0inter, Kitty Brute Forcer
import hashlib # for sha256 and hexdigest
import string  # for the string constants

correct_hash = 'c7e83c01ed3ef54812673569b2d79c4e1f6554ffeb27706e98c067de9ab12d1a'

for c1 in string.ascii_uppercase:
    for c2 in string.ascii_lowercase:
        for c3 in string.digits:
            for c4 in string.digits:
                for c5 in string.punctuation:
                    mystring = c1 + c2 + c3 + c4 + c5
                    my_hash = hashlib.sha256(mystring).hexdigest()
                    if my_hash == correct_hash:
                        print mystring
