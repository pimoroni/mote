Welcome
-------

Mote is an ecosystem of lighting control products developed by Pimoroni. It's designed to be simple and easy to connect and use.

Mote adopts the wildely available microUSB connector to provide a custom protocol that supports 4 plug-and-play lighting control channels.

* More information - https://shop.pimoroni.com/products/mote
* Get the code - https://github.com/pimoroni/mote
* Get started - https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-mote
* Get help - http://forums.pimoroni.com/c/support

At A Glance
-----------

.. automoduleoutline:: mote
   :members:

Create A Class Instance
-----------------------

.. autoclass:: mote::Mote
   :noindex:

Configure A Channel
-------------------

.. automethod:: mote::Mote.configure_channel
   :noindex:

Set A Pixel
-----------

.. automethod:: mote::Mote.set_pixel
   :noindex:

Get Pixel Count
---------------

.. automethod:: mote::Mote.get_pixel_count
   :noindex:

Show
----

.. automethod:: mote::Mote.show
   :noindex:

.. _section-hardware:

Clear Mote
----------

.. automethod:: mote::Mote.clear
   :noindex:

Mote USB Host
-------------

The Mote USB host is powered by an ATXmega32a4u. It can drive up to 4 Mote lighting devices simultaneously.

* 4 "Mote" ports for driving attached lighting
* 1 data port for USB connection to the host computer
* 1 power port for connecting an AC adaptor (official Pi power supply recommended)
* Firmware upgradable via a USB-bootloader

Mote is equipped with an onboard auto-switching power supply to choose between low-brightness development mode, and unrestricted brightness when powered from an AC adaptor.

A 2A, 5V microUSB power supply is recommended to allow for 500mA per channel. The black or white supplies from our store are a good fit: https://shop.pimoroni.com/products/raspberry-pi-universal-power-supply

The Mote USB Host includes four 3mm mounting holes.

* The top two holes are spaced 41mm center to center,
* The bottom two holes are spaced 17mm center to center,
* The top and bottom sets of holes are spaced 15mm apart
* The right-most holes are aligned

The most USB host has an irregular shape, but broadly it's:

* 48mm wide and,
* 30mm long.
* The first set of holes are 12mm from the ports edge (to center),
* The second set of holes are 3mm from the opposite edge (to center),
* All holes are 3mm from their respective edges (to center)

A gap of 40mm from the ports edge and power edge is recommended inside any enclosure, to allow cables to flex without straining the ports. This can be squished down to 30mm.

The left-hand side of the bottom is inset by 8mm.

.. code-block:: text

     <-- Holes 41mm -->
          width 48mm
     _________________
    |  1   2   3   4  | 
    |O               O| ^
    |                 | | Holes 15mm
    |_5V_USB_         | | length 30mm
             |O______O| v
    <------->
     w 24mm   <------>
             Holes 17mm
             width 24mm

Lighting Ports
--------------

Mote's lighting devices are connected via one of the 4 ports (numbered 1 to 4 on reverse) along the top edge. These correspond to Mote's channels 1 to 4 in software.

While these ports use microUSB for their physical connector, they are *not* USB compatible; the data and clock lines carry an APA-102 compatible signal only.

Mote can drive up to 512 pixels and each channel can be configured to drive up to 128 pixels.

The pinout of each connector is, from left to right:

* GND
* NC
* Clock
* Data
* 5V

Programming Header
------------------

Mote includes a PDI (Programming/Debugging Interface) header. This is intended for flashing the firmware in production, but the ability to reflash has not been disabled. If you know how to use this- happy hacking ;)

16 Pixel APA-102 Mote Stick
---------------------------

The 16 Pixel APA-102 Mote Stick includes two 3mm mounting holes.

They are spaced 167mm center to center.

* The stick is 180mm long,
* and 10mm wide.
* The hole at the tip is 3mm from the edge (to center)
* The hole at the port is 10mm from the edge (to center)

.. code-block:: text

                   <-- Holes 167mm, length 180mm -->
     ________________________________________________________________
    |                                                                |  ^
   CON O                                                           O |  | width 10mm
    |________________________________________________________________|  v

    <--> 10mm from edge                             3mm from edge <->
