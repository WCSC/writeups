# IceCTF 2016
# Intercepted Part One
## Solution By: [duck](https://github.com/duckythescientist)

# Solution (copied from solve.py)

The pcap is a capture of a USB keyboard. 

The proper way to tell is by finding the VID/PID combination during enumeration then looking up the device from that.

The easy way is just to have looked at enough USB stuffs to recognize that it's a keyboard. :)

The keyboard data exists in the USB Leftover section. `tshark` is our friend for extracting this.

```bash
tshark -r ./intercept.pcapng -T fields -e usb.capdata -Y usb.capdata 2>/dev/null
```

This has some trailing data that we don't care about it, so use tail to skip the beginning 6 lines.
```bash
tshark -r ./intercept.pcapng -T fields -e usb.capdata -Y usb.capdata 2>/dev/null | tail -n +6
```

The output looks like:
```
00:00:00:00:00:00:00:00
20:00:00:00:00:00:00:00
20:00:0a:00:00:00:00:00
20:00:00:00:00:00:00:00
00:00:00:00:00:00:00:00
...
```

The first byte is a bit field of modifier keys (shift, ctrl, alt, etc.). 0x20 means shift

The third byte is a keycode. More keycodes can be in the later bytes, but this isn't the case this time.

A line of all 00's means that all keys have been released.

The keycodes can be found [here](http://download.microsoft.com/download/1/6/1/161ba512-40e2-4cc9-843a-923143f3456c/translate.pdf)

Except, it's not actually a QWERTY keyboard. It's (mostly) Dvorak. 
Luckily for me, I actually use Dvorak.

Treating it as pure Dvorak doesn't work either because some of the symbols aren't actually changed as expected.
Truthfully, I didn't save the key, and I did some unswapping by hand, so I don't know if this final script is fully correct. 
It's at least really close. (may need to swap ':' with 'Z')

```bash
tshark -r ./intercept.pcapng -T fields -e usb.capdata -Y usb.capdata 2>/dev/null | tail -n +6 | python usbcap_to_ascii.py
```
