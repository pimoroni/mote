#!/usr/bin/env python

import time

from mote import Mote

rgb = (128, 0, 0)

mote = Mote()

mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)

while True:
    r, g, b = rgb
    mote.set_all(r, g, b)
    mote.show()
    time.sleep(1)
    rgb = (g, b, r)
