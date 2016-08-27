# IceCTF 2016
## Solution By: Nullp0inter

# Kitty Web 70pts

They managed to secure their website this time and moved the hashing to the server :(. We managed to leak this hash of the admin's password though! `c7e83c01ed3ef54812673569b2d79c4e1f6554ffeb27706e98c067de9ab12d1a`. Can you get the flag? kitty.vuln.icec.tf

# Solution:
For this challenge we are given a hash that we are told belongs to the admin over at kitty.vuln.icec.tf. Our job is of course to crack the hash and login to the chalenge. We can do this two ways, an easy way
and a not as easy way. Before either of those it is a good idea to go ahead and try to put something into the login form so you can see that it has to match a "specified format." If we inspect the page source:

```html
<!doctype html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Log In</title>
    <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css" />
</head>
<body>
    <div class="container">
        <form method="post" action="login.php">
            <label for="username">Username: </label>
            <input class="u-full-width" type="text" name="username" placeholder="Username" required minlength="5" />
            <label for="password">Password: </label>
            <input id="password" class="u-full-width" type="password" name="password" placeholder="Password" required pattern="[A-Z][a-z][0-9][0-9][\?%$@#\^\*\(\)\[\];:]" />
            <input type="submit" value="Log In" />
        </form>
    </div>
</body>
</html>
```

Notice the line that reads `required pattern="[A-Z][a-z][0-9][0-9][\?%$@#\^\*\(\)\[\];:]`. Awesome, now we know that the format for the password is, in this order, one *captial* letter from A to Z, one *lowercase* letter
from a to z, two *digits* between 0 and 9, then finally one character that falls within `?%$@#^*()[];:`. Put together this means we can only have passwords like `Ab19?`,`Xf526%`, etc. You can also use an
online hash identifier to find out (if you didn't already know) that the given hash is sha256. Now let's get to those two options:

### The Easy Way:
Just jam that hash into this [online cracker](md5hashing.net/hash "Online Hash Cracking Utility, md5hashing.net"), making sure to select sha256 as the hash type.
It will come back in a few seconds and let you know that the result is `Vo83*` which fits our format so we try to login as user `admin` with
password `Vo83*` and PRESTO we are in!

```
Logged in!

Your flag is: IceCTF{i_guess_hashing_isnt_everything_in_this_world}
```

There it is the flag.


### The Not As Easy Way:
So recall that by now we know both the required format, the hash, AND we know the hash is of type sha256. We can write a simple python script
to brute force that pretty quickly:

```python 
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
```

That script will work in about 4 seconds and return the password string `Vo83*` (which matches what the online tool found). We simply take the
password we got and use it to login as user `admin` and receive your prize:

```
Logged in! 

Your flag is: IceCTF{i_guess_hashing_isnt_everything_in_this_world}
```

