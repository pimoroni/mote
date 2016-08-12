# Mote Demo Mac

This directory contains a script to build a self-contained demo for Mote using PyInstaller.

* mote-demo.py is the python script used to build against (and the code that will be executed by the demo)

* mote-demo is the binary resulting from the build process, and includes a self-contained Python environment including mote and pyserial modules pre-loaded.

* mote-demo.dmg contains an app bundle that can be used to test Mote on Mac OS X without any user-performed install