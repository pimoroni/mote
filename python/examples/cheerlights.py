#!/usr/bin/env python

import time
from colorsys import hsv_to_rgb
from sys import exit

try:
    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

from mote import Mote


mote = Mote()

num_pixels = 16

mote.configure_channel(1, num_pixels, False)
mote.configure_channel(2, num_pixels, False)
mote.configure_channel(3, num_pixels, False)
mote.configure_channel(4, num_pixels, False)


try:
    while True:
        r = requests.get('http://api.thingspeak.com/channels/1417/feed.json')
        j = r.json()
        f = j['feeds'][-8:]

        f = [element for index, element in enumerate(f) if index%2==0]

        print(f)

        channel = 1
        for col in f:
            col = col['field2']
            r, g, b = tuple(ord(c) for c in col[1:].lower().decode('hex'))
            for pixel in range(mote.get_pixel_count(channel)):
                mote.set_pixel(channel, pixel, r, g, b)
            channel += 1        

        mote.show()

        time.sleep(5)

except KeyboardInterrupt:
    mote.clear()
    mote.show()
    time.sleep(0.1)
