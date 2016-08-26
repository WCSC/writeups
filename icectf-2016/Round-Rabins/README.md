# IceCTF 2016
# Round Rabins!
# Solved By: bt
###### Crypto Challenge -- 100 points

## Description
"John gave up on RSA and moved to Rabin. ...he still did it wrong though [flag.txt](https://play.icec.tf/problem-static/flag_4541b3f5527778f80ae376bf7234dda6ea9a97b6103284a1f596bcec5e1c312c.txt). What a box!"


## Solution

After downloading the provided text file, we open it up and see what we have:

    N=0x6b612825bd7972986b4c0ccb8ccb2fbcd25fffbadd57350d713f73b1e51ba9fc4a6ae862475efa3c9fe7dfb4c89b4f92e925ce8e8eb8af1c40c15d2d99ca61fcb018ad92656a738c8ecf95413aa63d1262325ae70530b964437a9f9b03efd90fb1effc5bfd60153abc5c5852f437d748d91935d20626e18cbffa24459d786601
    c=0xd9d6345f4f961790abb7830d367bede431f91112d11aabe1ed311c7710f43b9b0d5331f71a1fccbfca71f739ee5be42c16c6b4de2a9cbee1d827878083acc04247c6e678d075520ec727ef047ed55457ba794cf1d650cbed5b12508a65d36e6bf729b2b13feb5ce3409d6116a97abcd3c44f136a5befcb434e934da16808b0b


Hmm... looks like RSA, but without an exponent. The name of the challenge is Rabin, so we read [Wikipedia](https://en.wikipedia.org/wiki/Rabin_cryptosystem) to get the details of the cryptosystem to find out how encryption works. For a message $m$, we get our ciphertext $c$ with the congruence $c = m^2 (mod N)$.

We use [Yafu](https://sourceforge.net/projects/yafu/) to find factors of `N`:

    ***factors found***
    
    P154 = 8683574289808398551680690596312519188712344019929990563696863014403818356652403139359303583094623893591695801854572600022831462919735839793929311522108161
    P154 = 8683574289808398551680690596312519188712344019929990563696863014403818356652403139359303583094623893591695801854572600022831462919735839793929311522108161

So $N$ is a square of a prime $p$.

After reading about decrypting a Rabin cipher, it seems we need our primes $p$ and $q$ to be congruent to $3\pmod{4}$, but $p \equiv q \not\equiv 3 \pmod{4}$, so we can't use the decryption method found in the article easily.

The problem boils down to finding $\sqrt{c} \pmod{p^2}$.
After a few hours of Googling and researching, I came across [Hensel's Lemma](https://en.wikipedia.org/wiki/Hensel%27s_lemma). Hensel's Lemma says we can use the roots found from $\sqrt{c} \pmod{p}$ to "lift" to a higher power of $p$, i.e., $\sqrt{c} \pmod{p^k}$ for any $k \geq 2$.

I found a [post](http://mathforum.org/library/drmath/view/70474.html) which has formulas for finding our roots. Basically we have two main steps:

1. Find the square roots modulo $p$, i.e., $m^2 \pmod{p}$. This is pretty easy to find using a modular square root algorithm.
2. Find roots of increasing powers of $p$ using the equation $r - \frac{(r^2 - p^2)}{2r} \pmod{p^2}$, where $r$ is one of the roots found from step 1. (Do this step again for every root found in step 1).

Since we're interested in the roots $\mod{p^2}$, we can stop here and look at the two new roots found in step 2. One of them is our flag, the other is extraneous. We write a script to do our computations:

~~~python
#!/usr/bin/env python
'''
Rabin cryptosystem challenge:
N=0x6b612825bd7972986b4c0ccb8ccb2fbcd25fffbadd57350d713f73b1e51ba9fc4a6ae862475efa3c9fe7dfb4c89b4f92e925ce8e8eb8af1c40c15d2d99ca61fcb018ad92656a738c8ecf95413aa63d1262325ae70530b964437a9f9b03efd90fb1effc5bfd60153abc5c5852f437d748d91935d20626e18cbffa24459d786601


c=0xd9d6345f4f961790abb7830d367bede431f91112d11aabe1ed311c7710f43b9b0d5331f71a1fccbfca71f739ee5be42c16c6b4de2a9cbee1d827878083acc04247c6e678d075520ec727ef047ed55457ba794cf1d650cbed5b12508a65d36e6bf729b2b13feb5ce3409d6116a97abcd3c44f136a5befcb434e934da16808b0b
'''

def legendre_symbol(a, p):
    """
    Legendre symbol
    Define if a is a quadratic residue modulo odd prime
    http://en.wikipedia.org/wiki/Legendre_symbol
    """
    ls = pow(a, (p - 1)/2, p)
    if ls == p - 1:
        return -1
    return ls

def prime_mod_sqrt(a, p):
    """
    Square root modulo prime number
    Solve the equation
        x^2 = a mod p
    and return list of x solution
    http://en.wikipedia.org/wiki/Tonelli-Shanks_algorithm
    """
    a %= p

    # Simple case
    if a == 0:
        return [0]
    if p == 2:
        return [a]

    # Check solution existence on odd prime
    if legendre_symbol(a, p) != 1:
        return []

    # Simple case
    if p % 4 == 3:
        x = pow(a, (p + 1)/4, p)
        return [x, p-x]

    # Factor p-1 on the form q * 2^s (with Q odd)
    q, s = p - 1, 0
    while q % 2 == 0:
        s += 1
        q //= 2

    # Select a z which is a quadratic non resudue modulo p
    z = 1
    while legendre_symbol(z, p) != -1:
        z += 1
    c = pow(z, q, p)

    # Search for a solution
    x = pow(a, (q + 1)/2, p)
    t = pow(a, q, p)
    m = s
    while t != 1:
        # Find the lowest i such that t^(2^i) = 1
        i, e = 0, 2
        for i in xrange(1, m):
            if pow(t, e, p) == 1:
                break
            e *= 2

        # Update next value to iterate
        b = pow(c, 2**(m - i - 1), p)
        x = (x * b) % p
        t = (t * b * b) % p
        c = (b * b) % p
        m = i

    return [x, p-x]

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


# This finds a solution for c = x^2 (mod p^2)
def find_solution(c, p):
    '''
    Hensel lifting is fairly simple.  In one sense, the idea is to use
    Newton's method to get a better result.  That is, if p is an odd
    prime, and

                            r^2 = n (mod p),

    then you can find the root mod p^2 by changing your first
    "approximation" r to

                        r - (r^2 - n)/(2r) (mod p^2).

    http://mathforum.org/library/drmath/view/70474.html                    
    '''
    n = p ** 2
    # Get square roots for x^2 (mod p)
    r = prime_mod_sqrt(c,p)[0]

    inverse_2_mod_n = modinv(2, n)
    inverse_r_mod_n = modinv(r, n)

    new_r = r - inverse_2_mod_n * (r - c * inverse_r_mod_n)

    return new_r % n

if __name__ == "__main__":
    # These are the given values
    n = 0x6b612825bd7972986b4c0ccb8ccb2fbcd25fffbadd57350d713f73b1e51ba9fc4a6ae862475efa3c9fe7dfb4c89b4f92e925ce8e8eb8af1c40c15d2d99ca61fcb018ad92656a738c8ecf95413aa63d1262325ae70530b964437a9f9b03efd90fb1effc5bfd60153abc5c5852f437d748d91935d20626e18cbffa24459d786601L
    # n is a perfect square: n = p * p
    p = 0xa5cc6d4e9f6a893c148c6993e1956968c93d9609ed70d8366e3bdf300b78d712e79c5425ffd8d480afcefc71b50d85e0914609af240c981c438acd1dcb27b301L
    # encrypted message
    c = 0xd9d6345f4f961790abb7830d367bede431f91112d11aabe1ed311c7710f43b9b0d5331f71a1fccbfca71f739ee5be42c16c6b4de2a9cbee1d827878083acc04247c6e678d075520ec727ef047ed55457ba794cf1d650cbed5b12508a65d36e6bf729b2b13feb5ce3409d6116a97abcd3c44f136a5befcb434e934da16808b0bL

    solution = find_solution(c, p)
    print hex(solution)[2:-1].decode("hex")
~~~

Running this gives us our flag: `IceCTF{john_needs_to_get_his_stuff_together_and_do_things_correctly}`
