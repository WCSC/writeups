# IceCTF 2016
## Solution By: Nullp0inter

# IRC 2 -Misc- 60pts
Can you trick our IRC bot into giving you his flag? Talk to IceBot on glitch.is:6667. Please only send him private messages, you do this by writing /msg IceBot !command. the "help" command has been removed so here is the output from !help. Please consider that he may be slow to respond or the command you're trying may not work.

# Solution:

So we are told once again to return to the IRC to see if we can trick him into giving us the flag.
They gave us a text file that lists all of the commands (this is due to a sopel bug where too many
requests to the help command can actually "DDoS" the bot). Taking a look at the list we see a command
that should probably stand out to everyone, `!flag`. If we go to IRC and try to just message him this
as we are told to do it, `/msg IceBot !flag`, he will spit back an ugly looking python error:

```
KeyError: Identifier('nullp0inter') (file "/usr/local/lib/python2.7/dist-packages/sopel/module.py", line 321, in guarded)
```

Now I am sure this is where a TON of people got stuck (considering this had under 200 solves) and,
like me initially, ran off to research the bots backend and sopel. If you searched long enough and 
happened to be paying attention, you would find the error is related to you not having permissions,
i.e. not being OP. You could also waited for someone to forget the part about PM'ing the bot and try
to issue !flag in the channel (which happened quite a bit) and you would see:

```
 06:66 nullp0inter !flag
 06:66 +IceBot I'm sorry, you're not a channel operator
```

Not a channel OP? Easy fix, simply join a selfnamed channel, for me that is `/join nullp0inter` then
invite the bot to it, `/invite IceBot`. IceBot should then join your channel where you are an OP.
All thats left to do is issue `!flag` and presto:

```
nullp0inter !flag
IceBot IceCTF{H3Re_y0U_9O_M4s7Er_m4kE_5uR3_yOU_K33P_iT_54F3}
```

There is the flag:
`IceCTF{H3Re_y0U_9O_M4s7Er_m4kE_5uR3_yOU_K33P_iT_54F3}`
_____
**_NOTE_** I have seen a few people quite literally joined my channel on glitch.is and try `!flag`. Please note that if you
*literally* try `/join nullp0inter` you will literally be joining a channel with me that I am the sole op of. Instead as I
mentioned you should do a `/join <name>` where name is **_your_** username. That is to say that if your nick on the IRC is
`xxmlgsniper420yolo` then the command you'll want to use is `/join xxmlgsniper420yolo`. Hopefully this clears up any confusion

**_ALTERNATIVELY_** You can simply join a nonsense channel and hope that you were the first to attempt to join such a channel.
One example that I did, and please don't try this one as I am already the op of it, is `/join #binsoutforharambe`. If you try nonsense
names for the channel, chances are you'll probably have been the first to do it. The idea is that when you join the channel, you
are listed as an `Operator`. If you are not listed as an `Operator` IceBot will tell you so and refuse to give you the flag.
