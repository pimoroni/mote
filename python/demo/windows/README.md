# Mote Demo Windows

This directory contains a script to build a self-contained demo for Mote using PyInstaller.

* mote-demo.py is the python script used to build against (and the code that will be executed by the demo)

* mote-demo.exe is the binary resulting from the build process, and includes a self-contained Python environment including mote and pyserial modules pre-loaded.

* motecdc.inf is a driver for Windows 7 and 8 to allow the Mote host to be recognised as a CDC device. It is unsigned therefore you will need to install it when Windows is booted in safe mode on Windows 8 and 8.1
