#!/usr/bin/env python
import random
import time
import argparse
from mote import Mote

print("""random-blinky.py - Blink random LEDs in random or specified colour

Press Ctrl+C to exit!
""")

parser = argparse.ArgumentParser()
parser.add_argument('--red', type=int, default=-1, help='Red amount (0-255), -1 for random')
parser.add_argument('--green', type=int, default=-1, help='Green amount (0-255), -1 for random')
parser.add_argument('--blue', type=int, default=-1, help='Blue amount (0-255), -1 for random')
parser.add_argument('--delay', type=float, default=0.05, help='Delay between updates')
parser.add_argument('--max', type=int, default=5, help='Maximum number of pixels to light per channel')

args = parser.parse_args()

mote = Mote()

mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)

args.red = max(-1, min(args.red, 255))
args.green = max(-1, min(args.green, 255))
args.blue = max(-1, min(args.blue, 255))
args.max = max(1, min(args.max, 16))

try:
    while True:
        for channel in range(4):
            pixels = random.sample(range(16), random.randint(1, args.max))
            for i in range(16):
                if i in pixels:
                    mote.set_pixel(channel + 1, i,
                                   random.randint(0, 255) if args.red == -1 else args.red,
                                   random.randint(0, 255) if args.green == -1 else args.green,
                                   random.randint(0, 255) if args.blue == -1 else args.blue)
                else:
                    mote.set_pixel(channel + 1, i, 0, 0, 0)
            mote.show()
        time.sleep(args.delay)

except KeyboardInterrupt:
    mote.clear()
    mote.show()
    quit()
