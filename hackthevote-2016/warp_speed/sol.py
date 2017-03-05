#!/usr/bin/env python3

import math
from PIL import Image

STRIP_WIDTH = 504
STRIP_HEIGHT = 8

def unwrap(im, strip_height=STRIP_HEIGHT):
    out_im = Image.new(im.mode, (int(math.ceil(im.size[0]*im.size[1]/strip_height)), strip_height))

    line = 0
    while line * strip_height < im.size[1]:
        rect = im.crop((0, line * strip_height, im.size[0], (line+1) * strip_height))
        rect.load()
        out_im.paste(rect, (line * im.size[0], 0, (line+1) * im.size[0], strip_height))

        line += 1

    return out_im

def collate(im, strip_width=STRIP_WIDTH, strip_height=STRIP_HEIGHT):
    out_im = Image.new(im.mode, (strip_width, int(math.ceil(im.size[0]/strip_width)) * strip_height))

    line = 0
    while line * strip_width < im.size[0]:
        rect = im.crop((line * strip_width, 0, (line+1) * strip_width, strip_height))
        rect.load()
        out_im.paste(rect, (0, line * strip_height, strip_width, (line+1) * strip_height))

        line += 1

    return out_im

image = Image.open('warp_speed.jpg')
fixed_image = collate(unwrap(image)).rotate(90)
fixed_image.save('warp_speed_fixed.jpg')

