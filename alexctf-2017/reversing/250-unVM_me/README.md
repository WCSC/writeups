# Reversing 250 - UnVM me

### Description

> If I tell you what version of python I used .. where is the fun in that?

### Solution

[This blog post](http://nedbatchelder.com/blog/200804/the_structure_of_pyc_files.html)
explained that the first 4 bytes of a .pyc file are a magic number indicating
what version of `marshal` (which changes every python major version) was used for serialization.
The next 4 bytes are a modification timestamp, and the rest of the file is a
marshalled code object.

The first four bytes of the .pyc file are `03 f3 0d 0a` (`'\x03\xf3\r\n'`).
[This SO answer](http://stackoverflow.com/a/7807661/1529586) enumerates the known
.pyc version numbers. According to the list, this .pyc file was compiled with
python 2.7a0. We will use that version to demarshal it.

After seeking past the 8th byte, we should be able to call `marshal.load()` and pass the
resulting code object into `dis.dis`. After some trial and error, we arrive at the
original source (located in `original.py`).

It contains a list of md5 digests that must be reversed. The input strings that correspond
to the hashes are 5 characters long each (according to `for i in range(0, len(flag), 5):`)
and there are 13 of them in total. Passing these hashes into any hash cracking software
should get the 13 original strings. Concatenating these results in the flag.

### Flag

    ALEXCTF{dv5d4s2vj8nk43s8d8l6m1n5l67ds9v41n52nv37j481h3d28n4b6v3k}
