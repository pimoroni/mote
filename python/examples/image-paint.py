#!/usr/bin/env python
# Adapted from Adafruit's dotstar python example
# https://github.com/adafruit/Adafruit_DotStar_Pi

from PIL import Image
from mote import Mote
mote = Mote()


NUMPIXELS = 16          # Number of LEDs in strip
FILENAME = "hello.png"  # Image file to load

mote.configure_channel(1, NUMPIXELS, False)
mote.configure_channel(2, 0, False)
mote.configure_channel(3, 0, False)
mote.configure_channel(4, 0, False)

# Load image in RGB format and get dimensions:
print("Loading...")
img = Image.open(FILENAME).convert("RGB")
pixels = img.load()
width, height = img.size
ratio = width / height
print("Image is {}x{}".format(width, height))

if height > NUMPIXELS:
    height = NUMPIXELS
    width = int(height * ratio)
    img.resize((width, height))
    print("Resized to {}x{}".format(width, height))

# Calculate gamma correction table, makes mid-range colors look 'right':
gamma = bytearray(256)
for i in range(256):
    gamma[i] = int(pow(float(i) / 255.0, 2.7) * 255.0 + 0.5)

print("Displaying...")

try:
    while True:
        for x in range(width):                   # For each column of image...
            for y in range(height):              # For each pixel in column...
                value = pixels[x, y]             # Read pixel in image
                mote.set_pixel(1,
                               y,                # Set pixel in strip
                               gamma[value[0]],  # Gamma-corrected red
                               gamma[value[1]],  # Gamma-corrected green
                               gamma[value[2]])  # Gamma-corrected blue
            mote.show()                          # Refresh LED strip

except KeyboardInterrupt:
    mote.clear()
    mote.show()
    quit()
