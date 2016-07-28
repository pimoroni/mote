import serial
import serial.tools.list_ports
import time
import sys

VID = 0x16d0
PID = 0x08c4
NAME = 'Mote USB Dock'

MAX_PIXELS = 512
MAX_PIXELS_PER_CHANNEL = int(MAX_PIXELS / 4)

class Mote:

    def __init__(self):
        """Initialize a new instance of Mote"""

        self._channels = [None] * 4
        self._channel_flags = [0] * 4

        self.port_name = self._find_serial_port(VID, PID, NAME)

        if self.port_name is None:
            raise IOError("Unable to find Mote device")

        self.port = serial.Serial(self.port_name, 115200, timeout=1)

    def _find_serial_port(self, vid, pid, name):
        """Find a serial port by VID, PID and text name

        :param vid: USB vendor ID to locate
        :param pid: USB product ID to locate
        :param name: USB device name to find where VID/PID match fails

        """

        check_for = "USB VID:PID={vid:04x}:{pid:04x}".format(vid=vid,pid=pid).upper()
        ports = serial.tools.list_ports.comports()

        for check_port in ports:
            if hasattr(serial.tools,'list_ports_common'):
                if (check_port.vid, check_port.pid) == (VID, PID):
                    return check_port.device
                continue

            if check_for in check_port[2].upper() or name == check_port[1]:
                return check_port[0]

        return None

    def configure_channel(self, channel, num_pixels, gamma_correction=False):
        """Configure a channel

        :param channel: Channel, either 1, 2, 3 or 4 corresponding to numbers on Mote
        :param num_pixels: Number of pixels to configure for this channel
        :param gamma_correction: Whether to enable gamma correction (default False)

        """

        if channel > 4 or channel < 1:
            raise ValueError("Channel index must be between 1 and 4")
        if num_pixels > MAX_PIXELS_PER_CHANNEL:
            raise ValueError("Number of pixels can not be more than {max}".format(max=MAX_PIXELS_PER_CHANNEL))

        self._channels[channel - 1] = [(0,0,0)] * num_pixels
        self._channel_flags[channel -1] = 1 if gamma_correction else 0

        self.port.write(b'mote')
        self.port.write(b'c')
        self.port.write(bytes([channel, num_pixels, self._channel_flags[channel -1]]))

    def set_pixel(self, channel, index, r, g, b):
        """Set the RGB colour of a single pixel, on a single channel

        :param channel: Channel, either 1, 2, 3 or 4 corresponding to numbers on Mote
        :param index: Index of pixel to set, from 0 up
        :param r: Amount of red: 0-255
        :param g: Amount of green: 0-255
        :param b: Amount of blue: 0-255

        """

        if channel > 4 or channel < 1:
            raise ValueError("Channel index must be between 1 and 4")
        if self._channels[channel-1] is None:
            raise ValueError("Please set up channel {channel} before using it!".format(channel=channel))
        if index >= len(self._channels[channel-1]):
            raise ValueError("Pixel index must be < {length}".format(length=len(self._channels[channel-1])))

        self._channels[channel-1][index] = (r & 0xff, g & 0xff, b & 0xff)

    def show(self):
        """Send the pixel buffer to the hardware"""

        buf = bytearray()
        for index, data in enumerate(self._channels):
            if data is None: continue
            for pixel in data:
                buf.append(pixel[2])
                buf.append(pixel[1])
                buf.append(pixel[0]) 

        self.port.write(b'mote')
        self.port.write(b'o')
        self.port.write(buf)

    def __exit__(self):
        self.port.close()


if __name__ == "__main__":
    from colorsys import hsv_to_rgb
    mote = Mote()

    mote.configure_channel(1, 16, False)
    mote.configure_channel(2, 16, False)
    mote.configure_channel(3, 16, False)
    mote.configure_channel(4, 16, False)

    for channel in range(4):
        for pixel in range(16):
           mote.set_pixel(channel + 1, pixel, 255, 0, 0)
           mote.show()
           time.sleep(0.01)

    for channel in range(4):
        for pixel in range(16):
           mote.set_pixel(channel + 1, pixel, 0, 255, 0)
           mote.show()
           time.sleep(0.01)

    for channel in range(4):
        for pixel in range(16):
           mote.set_pixel(channel + 1, pixel, 0, 0, 255)
           mote.show()
           time.sleep(0.01)

    for h in range(10000):
        for channel in range(4):
            for pixel in range(16):
                hue = (h + (channel * 64) + (pixel * 4)) % 360
                r, g, b = [int(c * 255) for c in hsv_to_rgb(hue/360.0, 1.0, 1.0)]
                mote.set_pixel(channel + 1, pixel, r, g, b)
        mote.show()
        time.sleep(0.01)


