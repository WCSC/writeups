# IceCTF Toke
### Solution By: Nullp0inter

# Description:
I have a feeling they were pretty high when they made this [website](toke.vuln.icec.tf)...

# Solution

When you visit the webpage you are able to do basically two things, register and login. I, along with what I assume is a significant portion of people, thought that
this challenge was a SQLi or XSS challenge at first. I initially made an account trying XSS but it was handled properly so that got nowhere, except I did see the post
was made by a "Toke" who I then attempted to SQLi may way into for a while which was also fruitless. After logging in if you examine the cookies you will see one that
is `jwt_token` which looks to be base64 encoded. If we just throw copy the whole thing `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmbGFnIjoiSWNlQ1RGe2pXN190MEszbnNfNFJlX25PX3AxNENFX2ZPUl81M0NyRTdTfSIsInVzZXIiOiJucHRyIn0.ItKxsZx5YLny17hrz2WTmWALcBzwxB75pjwkxrNONd8` and just base64decode it:

```python
#!/usr/bin/python

import Base64

cookie = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmbGFnIjoiSWNlQ1RGe2pXN190MEszbnNfNFJlX25PX3AxNENFX2ZPUl81M0NyRTdTfSIsInVzZXIiOiJucHRyIn0.ItKxsZx5YLny17hrz2WTmWALcBzwxB75pjwkxrNONd8'

print (base64.b64decode(cookie))
```

we get back the flag:
`IceCTF{jW7_t0K3ns_4Re_nO_p14CE_fOR_53CrE7S}`
