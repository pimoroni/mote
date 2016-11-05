#!/usr/bin/env python
#Based on original cheerlights.py from Pimoroni

import time
from colorsys import hsv_to_rgb
from colorsys import rgb_to_hsv
from copy import copy
from sys import exit

try:
    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

from mote import Mote


mote = Mote()

num_pixels = 16

transition_time = 1 # seconds
transition_step = 100

mote.configure_channel(1, num_pixels, False)
mote.configure_channel(2, num_pixels, False)
mote.configure_channel(3, num_pixels, False)
mote.configure_channel(4, num_pixels, False)

try:
    channels_colour_rgb = [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]
    channels_colour = [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]
    channels_colour_delta = [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]
    old_channels_colour = [[0,1,0], [0,1,0], [0,1,0], [0,1,0]]
    while True:
        r = requests.get('http://api.thingspeak.com/channels/1417/feed.json')
        j = r.json()
        f = j['feeds'][-8:]

        f = [element for index, element in enumerate(f) if index%2==0]
        
        # get the new colours
        channel = 1
        for col in f:
            col = col['field2']
            r, g, b = tuple(ord(c) for c in col[1:].lower().decode('hex'))
            h,s,v = rgb_to_hsv(r,g,b)
            channels_colour_rgb[channel - 1][0] = r
            channels_colour_rgb[channel - 1][1] = g
            channels_colour_rgb[channel - 1][2] = b
            channels_colour[channel - 1][0] = h
            channels_colour[channel - 1][1] = s
            channels_colour[channel - 1][2] = v
            #calculate the count for each
            for idx in range(0,3):
                channels_colour_delta[channel - 1][idx] = (channels_colour[channel - 1][idx] - old_channels_colour[channel - 1][idx]) / float(transition_step)
            channel += 1     

        print(channels_colour_rgb)

        if old_channels_colour != channels_colour:
            # Do the transition
            for step in range(0, transition_step):
                for channel in range(1, 5):
                    for idx in range(0,3):
                        old_channels_colour[channel - 1][idx] += channels_colour_delta[channel - 1][idx]
                        r,g,b = hsv_to_rgb(old_channels_colour[channel - 1][0],
                                           old_channels_colour[channel - 1][1],
                                           old_channels_colour[channel - 1][2]);
                        for pixel in range(mote.get_pixel_count(channel)):
                            mote.set_pixel(channel, pixel, int(r), int(g), int(b))
                        mote.show()
                time.sleep(transition_time / transition_step)

        for channel in range(0, 4):
            for idx in range(0,3):
                old_channels_colour[channel][idx] = channels_colour[channel][idx]
        time.sleep(5)

except KeyboardInterrupt:
    mote.clear()
    mote.show()
    time.sleep(0.1)
