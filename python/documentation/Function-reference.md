<!--
---
title: Mote Python Function Reference
handle: mote-python-function-reference
type: tutorial
summary: A reference for Mote's Python library
author: Phil Howard
products: [mote]
tags: [Mote, Raspberry Pi, Python, Programming]
images: [images/tba.png]
difficulty: Beginner
-->
# Mote Function Reference

###configure_channel

Configures a channel using the following parameters:

channel: channel, either 1, 2, 3 or 4, corresponding to numbers on Mote  
num_pixels: number of pixels to configure for this channel  
gamma_correction: whether to enable gamma correction (default False)  

```
from mote import Mote

mote = Mote()
mote.configure_channel(1, 16, False)
```

This will create an instance of the Mote class to drive a 16 pixels APA102 stick on channel 1.

###set_pixel

Sets the RGB colour of a single pixel on a single channel, using the following parameters:

channel: channel, either 1, 2, 3 or 4, corresponding to numbers on Mote  
index: index of the pixel to set, starting at 0 (0-15 for 16 pixels sticks)  
r,g,b: amount of red/green/blue, from 0-255  

```
mote.set_pixel(1, 0, 255, 255, 255)
mote.show()
```

Note the show() method required to update all pixels after calling set_pixel.

###get_pixel

Gets the RGB colour of a single pixel on a single channel, using the following parameters:

channel: channel, either 1, 2, 3 or 4, corresponding to numbers on Mote  
index: index of the pixel to set, starting at 0 (0-15 for 16 pixels sticks)  

```
mote.get_pixel(1, 0)
```

###get_pixel_count

Gets the number of pixels a channel is configured to using a single parameter corresponding to the channel to probe:

channel: channel, either 1, 2, 3 or 4, corresponding to numbers on Mote  

```
mote.get_pixel_count(1)
```

###clear

The clear() method clears the buffer of a specific, or all channels:

```
mote.clear()
```

or, to only clear the pixels attached to channel 1:

```
mote.clear(1)
```

##Examples

There are a number of examples in the Examples folder that illustrate the above concepts.
