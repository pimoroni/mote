#!/usr/bin/env python

import sys
import time

from mote import Mote


mote = Mote()

mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)


def usage():
    print("Usage: {} <r> <g> <b>".format(sys.argv[0]))
    sys.exit(1)

if len(sys.argv) != 4:
    usage()

# Exit if non integer value. int() will raise a ValueError
try:
    r, g, b = [int(x) for x in sys.argv[1:]]
except ValueError:
    usage()

# Exit if any of r, g, b are greater than 255
if max(r,g,b) > 255:
    usage()

print("Setting Mote to {r},{g},{b}".format(r=r,g=g,b=b))

for channel in range(4):
    for pixel in range(16):
        mote.set_pixel(channel + 1, pixel, r, g, b)
    time.sleep(0.01)

mote.show()
