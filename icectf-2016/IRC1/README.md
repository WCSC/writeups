# IceCTF 2016
## Solution By: Nullp0inter

# IRC 1 Misc 35pts
There is someone sharing flags on our IRC server, can you find him and stop him? glitch.is:6667 

# Solution: 
We are told someone is sharing flags on the IRC server and we are asked to find him. All you need to
do is log into the IRC (easily done via their web client) and run a whois query on Glitch,
the creator of the challenge:

```
Glitch (~Glitch@localhost): Hlynur
Glitch is on the following channels: @#78a99bb_flagshare @#IceCTF @#Glitch
Glitch is connected to irc.glitch.is
Glitch is away (Auto away at Sat Aug 27 00:27:01 2016)
```

Hmm, he is an op over at `#78a99bb_flagshare`. Odd, let's join that with `/join #78a99bb_flagshare`.
Once you join look at the channel topic:

```
The topic is: Want flags? We got 'em! IceCTF{pL3AsE_D0n7_5h4re_fL495_JUsT_doNT}
```

Flag: `IceCTF{pL3AsE_D0n7_5h4re_fL495_JUsT_doNT}`
