Mote USB Host
=============

The Mote USB host is powered by an ATXmega32a4u. It can drive up to 4 Mote lighting add-ons simultaneously.

* 4 "Mote" ports for driving attached lighting
* 1 data port for USB connection to the host computer
* 1 power port for connecting an AC adaptor (official Pi power supply recommended)
* Firmware upgradable via a USB-bootloader

Mote is equipped with an onboard auto-switching power supply to choose between low-brightness development mode, and unrestricted brightness when powered from an AC adaptor.

A 2A, 5V microUSB power supply is recommended to allow for 500mA per channel. The black or white supplies from our store are a good fit: https://shop.pimoroni.com/products/raspberry-pi-universal-power-supply

Mote Lighting Ports
-------------------

Mote's lighting devices are connected via one of the 4 ports (numbered 1 to 4 on reverse) along the top edge. These correspond to Mote's channels 1 to 4 in software.

While these ports use microUSB for their physical connector, they are *not* USB compatible; the data and clock lines carry an APA-102 compatible signal only.

Mote can drive up to 512 pixels and each channel can be configured to drive up to 128 pixels.

The pinout of each connector is, from left to right:

* GND
* NC
* Clock
* Data
* 5V

Mote Programming Header
-----------------------

Mote includes a PDI (Programming/Debugging Interface) header. This is intended for flashing the firmware in production, but the ability to reflash has not been disabled. If you know how to use this- happy hacking ;)