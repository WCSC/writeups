# IceCTF RSA 1
### Solved By: Nullp0inter

# Solution
We are given N, c, and e where `e = 0x1`. In RSA `ed = 1 mod phi`, all you need to know then is that phi is bigger than 1 (WAY bigger usually) and that given
`A mod B` where B is the larger number, the result is A. We then have `ed = 1` so because e is 1, we know d must also be 1. Now that we have d all we need to do
is plug our numbers into this [online RSA calculator](http://nmichaels.org/rsa.py "Online RSA Tool") (because I'm lazy and didn't feel like writing it in python).
That will net you the flag.

# Note:
Due to not having saved the actual numbers (other than e), the challenge description, or the flag itself, this write up will be in extremely rough shape until I get those.
Once I have the information I need, I will edit this to actually include those
