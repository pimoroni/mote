import sys
import time

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    exit("This library requires the serial module\nInstall with: sudo pip install pyserial")


VID = 0x16d0
PID = 0x08c4
NAME = 'Mote USB Dock'

MAX_PIXELS = 512
MAX_PIXELS_PER_CHANNEL = int(MAX_PIXELS / 4)

class Mote:
    """Represents a connected Mote device, communicating over USB serial.

    The Mote class allows you to configure the 4 channels and set individual pixels.

    It will attach to the first available Mote device unless `port_name` is specified at init.

    :param port_name: Override auto-detect and specify an explicit port to use. Must be a complete path ie: /dev/tty.usbmodem1234 (default None)
    """

    def __init__(self, port_name=None):
        self.port_name = port_name
        self._channels = [None] * 4
        self._channel_flags = [0] * 4

        if self.port_name is None:
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

        buf = bytearray()
        buf.append(channel)
        buf.append(num_pixels)
        buf.append(self._channel_flags[channel -1])

        self.port.write(b'mote')
        self.port.write(b'c')
        self.port.write(buf)

    def get_pixel_count(self, channel):
        """Get the number of pixels a channel is configured to use

        :param channel: Channel, either 1, 2 3 or 4 corresponding to numbers on Mote

        """

        if channel > 4 or channel < 1:
            raise ValueError("Channel index must be between 1 and 4")
        if self._channels[channel-1] is None:
            raise ValueError("Channel {channel} has not been set up".format(channel=channel))

        return len(self._channels[channel-1])

    def get_pixel(self, channel, index):
        """Get the RGB colour of a single pixel, on a single channel

        :param channel: Channel, either 1, 2, 3 or 4 corresponding to numbers on Mote
        :param index: Index of pixel to set, from 0 up

        """

        if channel > 4 or channel < 1:
            raise ValueError("Channel index must be between 1 and 4")
        if self._channels[channel-1] is None:
            raise ValueError("Please set up channel {channel} before using it".format(channel=channel))
        if index >= len(self._channels[channel-1]):
            raise ValueError("Pixel index must be < {length}".format(length=len(self._channels[channel-1])))

        return self._channels[channel-1][index]

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

    def clear(self, channel=None):
        """Clear the buffer of a specific or all channels

        :param channel: If set, clear a specific channel, otherwise all (default None)

        """

        if channel is None:
            for index, data in enumerate(self._channels):
                if data is not None:
                    self.clear(index+1)
            return

        if channel > 4 or channel < 1:
            raise ValueError("Channel index must be between 1 and 4")
        if self._channels[channel-1] is None:
            raise ValueError("Please set up channel {channel} before using it!".format(channel=channel))

        self._channels[channel-1] = [(0,0,0)] * len(self._channels[channel-1])

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

    num_pixels = 16

    mote.configure_channel(1, num_pixels, False)
    mote.configure_channel(2, num_pixels, False)
    mote.configure_channel(3, num_pixels, False)
    mote.configure_channel(4, num_pixels, False)

    colors = [
        (255,   0,   0),
        (0,   255,   0),
        (0,     0, 255),
        (255, 255, 255)
    ]

    try:
        for step in range(4):
            for channel in range(4):
                for pixel in range(num_pixels):
                    r, g, b = colors[channel]
                    mote.set_pixel(channel + 1, pixel, r, g, b)
                    mote.show()
                    time.sleep(0.01)

            colors.append(colors.pop(0))

        for step in range(170):
            for channel in range(4):
                for pixel in range(num_pixels):
                    r, g, b = [int(c * 0.99) for c in mote.get_pixel(channel + 1, pixel)]
                    mote.set_pixel(channel + 1, pixel, r, g, b)

            time.sleep(0.001)
            mote.show()

        brightness = 0
        for h in range(10000):
            for channel in range(4):
                for pixel in range(num_pixels):
                    hue = (h + (channel * num_pixels * 4) + (pixel * 4)) % 360
                    r, g, b = [int(c * brightness) for c in hsv_to_rgb(hue/360.0, 1.0, 1.0)]
                    mote.set_pixel(channel + 1, pixel, r, g, b)
            mote.show()
            time.sleep(0.01)
            if brightness < 255: brightness += 1

    except KeyboardInterrupt:
        mote.clear()
        mote.show()
        time.sleep(0.1)
