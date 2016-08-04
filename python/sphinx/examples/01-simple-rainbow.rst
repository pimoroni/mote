Simple Rainbow
==============

This tutorial will guide you through the steps to show a simple rainbow LED pattern on your Mote.

To create a rainbow, we're going to convert from the Hue/Saturation/Value colour space, into the Red/Green/Blue that Mote understands. HSV is represented as a cylinder with Hue around its circumference, saturation along its radius, and value (or brightness) running from bottom to top.

By setting Saturation and Value to 1.0 (max) we always get a bright, fully saturated colour. This leaves us with a circular hue value around the top edge of the cylinder, 360 degrees in length which constitutes the rainbow we want to display.

First we'll import everything we'll need:

.. code-block:: python

    from colorsys import hsv_to_rgb
    
    from mote import Mote


Next we must create an instance of the `Mote` class. Mote is class-based because we might want to set up an instance for every Mote device connected to our computer. The class constructor will take the path to a serial port, to identify which Mote the instance should be responsible for.

If there's only one Mote, we can just initialise like so:

.. code-block:: python

    mote = Mote()


Now we must configure each channel on the Mote, so that it understands how to update the LEDs that are connected. This example assumes you have a single, 16 pixel Mote stick connected to channel one:

.. code-block:: python

    mote.configure_channel(1, 16)


Okay! That's the set-up done. Let's get to the guts of the code.

We want to create a rainbow swatch and display it across the 16 pixels.

We'll start by figuring how much of the hue value from the HSV colour space we need to display on each pixel:

.. code-block:: python

    degrees_per_pixel = 360 / 16.0


Then we'll iterate through our pixels:

.. code-block:: python

    for pixel in range(mote.get_pixel_count(1)):

        this_pixel_hue = (pixel * degrees_per_pixel)

        r, g, b = [int(c * 255) for c in hsv_to_rgb(this_pixel_hue/360.0, 1.0, 1.0)]

        mote.set_pixel(1, pixel, r, g, b)


And finally, send the result to Mote:

.. code-block:: python

    mote.show()


If everything goes according to plan, you should see your Mote light up with a rainbow swatch from red towards the USB connector right up to pink at the other end.

And, finally, here's the complete code for this example:

.. code-block:: python

    from colorsys import hsv_to_rgb
    from mote import Mote


    mote = Mote()

    mote.configure_channel(1, 16)

    degrees_per_pixel = 360 / 16.0

    for pixel in range(mote.get_pixel_count(1)):

        this_pixel_hue = (pixel * degrees_per_pixel)

        r, g, b = [int(c * 255) for c in hsv_to_rgb(this_pixel_hue/360.0, 1.0, 1.0)]

        mote.set_pixel(1, pixel, r, g, b)

    mote.show()
