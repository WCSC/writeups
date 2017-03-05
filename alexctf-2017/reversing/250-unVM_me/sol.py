#!/usr/bin/env python2.7

import marshal
import dis

with open('unvm_me.pyc') as f:
    f.read(8)
    dis.dis(marshal.load(f))
