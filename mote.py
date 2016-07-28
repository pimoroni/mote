import serial
import serial.tools.list_ports
import time
import sys
import numpy


GAMMA_CORRECT = 0x01

VID = 0x16d0
PID = 0x08c4

MAX_PIXELS = 512


buf = numpy.zeros(MAX_PIXELS)	

def find_serial_port(vid, pid):
    check_for = "USB VID:PID={vid:04x}:{pid:04x}".format(vid=vid,pid=pid).upper()
    ports = serial.tools.list_ports.comports()

    for check_port in ports:
        if hasattr(serial.tools,'list_ports_common'):
            if (check_port.vid, check_port.pid) == (VID, PID):
                return check_port.device
            continue

        if check_for in check_port[2].upper():
            return check_port[0]

    return None


port = find_serial_port(VID, PID)

if port is None:
    print("Unable to find Mote device")
    sys.exit(1)

ser = serial.Serial(port, 115200, timeout=1)


def configure_channel(index, num_pixels, gamma_correction=False):
    ser.write(b'mote')
    ser.write(b'c')
    ser.write(bytes([index, num_pixels, 1 if gamma_correction else 0]))

def set_pixel(channel, index, r, g, b):
    

configure_channel(1, 16, False)
configure_channel(2, 16, False)
configure_channel(3, 16, False)
configure_channel(4, 16, False)

i = 0

try:
    while True:
        values = bytearray()
        for v in range(0, 16):
            values.append((i + (v * 4)) % 256)
            values.append(0)
            values.append(0)
        for v in range(0, 16):
            values.append(0)
            values.append((i + (v * 4)) % 256)
            values.append(0)
        for v in range(0, 16):
            values.append(0)
            values.append(0)
            values.append((i + (v * 4)) % 256)
        for v in range(0, 16 * 3):
            values.append((i + (v * 4)) % 256)



        ser.write(b'mote')
        ser.write(b'o')
        ser.write(values)

        i += 1
except KeyboardInterrupt:
    pass

ser.close()
