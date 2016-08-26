#!/usr/bin/env python2

"""
The pcap is a capture of a USB keyboard. 
The proper way to tell is by finding the VID/PID combination during enumeration then looking up the device from that.
The easy way is just to have looked at enough USB stuffs to recognize that it's a keyboard. :)

The keyboard data exists in the USB Leftover section. `tshark` is our friend for extracting this.
tshark -r ./intercept.pcapng -T fields -e usb.capdata -Y usb.capdata 2>/dev/null
This has some trailing data that we don't care about it, so use tail to skip the beginning 6 lines.
tshark -r ./intercept.pcapng -T fields -e usb.capdata -Y usb.capdata 2>/dev/null | tail -n +6

The output looks like:
00:00:00:00:00:00:00:00
20:00:00:00:00:00:00:00
20:00:0a:00:00:00:00:00
20:00:00:00:00:00:00:00
00:00:00:00:00:00:00:00
...

The first byte is a bit field of modifier keys (shift, ctrl, alt, etc.). 0x20 means shift
The third byte is a keycode. More keycodes can be in the later bytes, but this isn't the case this time.
A line of all 00's means that all keys have been released.

The keycodes can be found here: http://download.microsoft.com/download/1/6/1/161ba512-40e2-4cc9-843a-923143f3456c/translate.pdf

Except, it's not actually a QWERTY keyboard. It's (mostly) Dvorak. 
Luckily for me, I actually use Dvorak.
Treating it as pure Dvorak doesn't work either because some of the symbols aren't actually changed as expected.

Truthfully, I didn't save the key, and I did some unswapping by hand, so I don't know if this final script is fully correct. 
It's at least really close. (may need to swap ':' with 'Z')


tshark -r ./intercept.pcapng -T fields -e usb.capdata -Y usb.capdata 2>/dev/null | tail -n +6 | python usbcap_to_ascii.py

"""
import string
import sys


def usb_to_ascii(x, mod=0):
    # This is really nasty

    # Qwerty with unprintables replaced by '?'
    # lower = string.ascii_lowercase + "1234567890" + "\n??\t -=[]\\?;'`,./?"
    # upper = string.ascii_uppercase + "!@#$%^&*()" + "\n??\t _|{}|?:\"~<>??"

    # Dvorak
    # lower = "axje.uidchtnmbrl'poygk,qf;" + "1234567890" + "\n??\t []/=\\?s-`wvz"
    # upper = 'AXJE>UIDCHTNMBRL"POYGK<QF:' + "!@#$%^&*()" + "\n??\t {}?+|?s_~WVZ"

    # Dvorak with some symbols unchanged
    lower = "axje.uidchtnmbrl'poygk,qf;" + "1234567890" + "\n??\t -=[]\\?;'`wvz?"
    upper = 'AXJE>UIDCHTNMBRL"POYGK<QF:' + "!@#$%^&*()" + '\n??\t _|{}|?:"WVZ??'

    chars = lower
    # Todo: better mod detection
    if mod:
        chars = upper

    # Keycodes start at 4
    num = x - 4
    if 0<= num < len(chars):
        # print num, chars[num]
        return chars[num]
    print num, "?"


text = ""
for line in sys.stdin.readlines():
    mod, spam, val = line.split(":")[:3]
    val = int(val, 16)
    mod = int(mod, 16)
    if val:
        char = usb_to_ascii(val, mod=mod)
        if char is not None:
            text += char

print text
