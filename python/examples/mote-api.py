#!/usr/bin/env python

from colorsys import hsv_to_rgb, rgb_to_hsv
from sys import exit

try:
    from flask import Flask, jsonify, make_response
except ImportError:
    exit("This script requires the flask module\nInstall with: sudo pip install flask")

from mote import Mote


## Create app, Mote instance
app = Flask(__name__)
mote = Mote()

## Configure Mote channels for 4x 16 pixel strips
mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)

# Define baseurl and current API version
baseurl = "/mote/api/"
version = "v1.0"

## Default status to initialise with - all channels off, white, full brightness
status = {'state': {1: 0, 2: 0, 3: 0, 4: 0},
          'colour': {1: [255, 255, 255], 2: [255, 255, 255], 3: [255, 255, 255], 4: [255, 255, 255]},
          'brightness': {1: 255, 2: 255, 3: 255, 4: 255}
         }

## Converts a hex colour like FF0000 to an RGB colour like 255, 0, 0 (red)
def hex_to_rgb(value):
    value = value.lstrip('#')
    length = len(value)
    return tuple(int(value[i:i + length / 3], 16) for i in range(0, length, length / 3))

## Turns Mote on, with the currently set colours and states for each channel
def mote_on(status):
    for chan in range(4):
        r, g, b = status['colour'][chan + 1]
        for pixel in range(16):
            if not status['state'][chan + 1] == 0:
                mote.set_pixel(chan + 1, pixel, r, g, b)
            else:
                mote.set_pixel(chan + 1, pixel, 0, 0, 0)
    mote.show()
    return True

## Turns Mote off
def mote_off(status):
    for chan in range(1, 5):
        if status['state'][chan] == 0:
            for pixel in range(16):
                    mote.set_pixel(chan, pixel, 0, 0, 0)
    mote.show()
    return True

## Returns, in JSON, the state of the given channel, or all channels
@app.route(baseurl + version + '/channel/<string:channel>/state', methods=['GET'])
def get_state(channel):
    global status
    for chan in range(1, 5):
        for pixel in range(16):
            if mote.get_pixel(chan, pixel) != (0, 0, 0):
                status['state'][chan] = 1
            else:
                status['state'][chan] = 0
        col = mote.get_pixel(chan, 0)
        br = rgb_to_hsv(*col)[2]
        status['colour'][chan] = list(col)
        status['brightness'][chan] = br
    if channel == 'all':
        return jsonify(status)
    else:
        channel_status = {}
        for k in status:
            channel_status[k] = {int(channel): status[k][int(channel)]}
        return jsonify(channel_status)

## Sets all channels, or a given channel, "on" or "off"
@app.route(baseurl + version + '/channel/<string:channel>/state/<string:st>', methods=['GET'])
def set_state(channel, st):
    global status
    if st == 'on':
        if channel == 'all':
            for chan in range(1, 5):
                status['state'][chan] = 1
        else:
            status['state'][int(channel)] = 1
        mote_on(status)
    elif st == 'off':
        if channel == 'all':
            for chan in range(1, 5):
                status['state'][chan] = 0
        else:
            status['state'][int(channel)] = 0
        mote_off(status)
    return jsonify(status)

## Returns the currently set colours for a specific channel or all channels
@app.route(baseurl + version + '/channel/<string:channel>/colour', methods=['GET'])
def get_colour(channel):
    global status
    if channel == 'all':
        return jsonify(status['colour'])
    else:
        return jsonify({channel: status['colour'][int(channel)]})

## Sets a colour for a specific channel or all channels
@app.route(baseurl + version + '/channel/<string:channel>/colour/<string:c>', methods=['GET'])
def set_colour(channel, c):
    global status
    if channel == 'all':
        for ch in status['colour']:
            status['colour'][ch] = hex_to_rgb(c)
        if not all(status['state'].values()) == 0:
            mote_on(status)
    else:
        status['colour'][int(channel)] = hex_to_rgb(c)
        if not status['state'][int(channel)] == 0:
            mote_on(status)
    return jsonify(status)

## Sets the brightness for a channel or all channels, by converting to HSV, 
## modifying the V, and then converting back to RGB, and setting that colour
@app.route(baseurl + version + '/channel/<string:channel>/brightness/<string:br>', methods=['GET'])
def set_brightness(channel, br):
    global status
    if channel == 'all':
        for ch in status['colour']:
            c = status['colour'][ch]
            r, g, b = c
            h, s, v = rgb_to_hsv(r, g, b)
            v = int(br) / 100.0
            r, g, b = [int(c * 255) for c in hsv_to_rgb(h, s, v)]
            status['colour'][ch] = [r, g, b]
        if not all(status['state'].values()) == 0:
            mote_on(status)
    else:
        c = status['colour'][int(channel)]
        r, g, b = c
        h, s, v = rgb_to_hsv(r, g, b)
        v = int(br) / 100.0
        r, g, b = [int(c * 255) for c in hsv_to_rgb(h, s, v)]
        status['colour'][int(channel)] = [r, g, b]
        if not status['state'][int(channel)] == 0:
            mote_on(status)
    return jsonify(status)

## Returns the current API version to the requester
@app.route(baseurl, methods=['GET'])
def get_version():
    return jsonify({'mote-api-version': version})

## Catches page not found errors, returns 404
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    mote_off(status)
    app.run(host='0.0.0.0', debug=True)
