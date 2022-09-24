#!/usr/bin/python
import time
import sys
import socket
from sense_hat import SenseHat
from evdev import InputDevice, list_devices, ecodes

sense = SenseHat()
sense.set_rotation(180)

# Setting some variables
hostname = socket.gethostname()
ipaddress = socket.gethostbyname(hostname)


found = False;
devices = [InputDevice(fn) for fn in list_devices()]
for dev in devices:
    if dev.name == 'Raspberry Pi Sense HAT Joystick':
        found = True;
        break

if not(found):
    print('Raspberry Pi Sense HAT Joystick not found. Aborting ...')
    sys.exit()


# Defining colours
red   = (255, 0, 0)
blue  = (0, 0, 255)
green = (0, 255, 0)
cyan  = (0, 255, 140)

pixels = [
    [255, 0, 0], [255, 0, 0], [255, 87, 0], [255, 196, 0], [205, 255, 0], [95, 255, 0], [0, 255, 13], [0, 255, 122],
    [255, 0, 0], [255, 96, 0], [255, 205, 0], [196, 255, 0], [87, 255, 0], [0, 255, 22], [0, 255, 131], [0, 255, 240],
    [255, 105, 0], [255, 214, 0], [187, 255, 0], [78, 255, 0], [0, 255, 30], [0, 255, 140], [0, 255, 248], [0, 152, 255],
    [255, 223, 0], [178, 255, 0], [70, 255, 0], [0, 255, 40], [0, 255, 148], [0, 253, 255], [0, 144, 255], [0, 34, 255],
    [170, 255, 0], [61, 255, 0], [0, 255, 48], [0, 255, 157], [0, 243, 255], [0, 134, 255], [0, 26, 255], [83, 0, 255],
    [52, 255, 0], [0, 255, 57], [0, 255, 166], [0, 235, 255], [0, 126, 255], [0, 17, 255], [92, 0, 255], [201, 0, 255],
    [0, 255, 66], [0, 255, 174], [0, 226, 255], [0, 117, 255], [0, 8, 255], [100, 0, 255], [210, 0, 255], [255, 0, 192],
    [0, 255, 183], [0, 217, 255], [0, 109, 255], [0, 0, 255], [110, 0, 255], [218, 0, 255], [255, 0, 183], [255, 0, 74]
]

msleep = lambda x: time.sleep(x / 1000.0)

def get_next_colour(pix):
    r = pix[0]
    g = pix[1]
    b = pix[2]

    if (r == 255 and g < 255 and b == 0):
        g += 1

    if (g == 255 and r > 0 and b == 0):
        r -= 1

    if (g == 255 and b < 255 and r == 0):
        b += 1

    if (b == 255 and g > 0 and r == 0):
        g -= 1

    if (b == 255 and r < 255 and g == 0):
        r += 1

    if (r == 255 and b > 0 and g == 0):
        b -= 1

    pix[0] = r
    pix[1] = g
    pix[2] = b

def get_temp():
    return str(round(sense.get_temperature(),1))

def get_humidity():
    return str(round(sense.get_humidity(),0))

def action_sense_clear():
    sense.clear()

def action_rainbow():
    while True:
        for pix in pixels:
            get_next_colour(pix)

        sense.set_pixels(pixels)
        msleep(2)

def action_show_temp(colour):
     sense.show_message(get_temp() + "C", text_colour=colour)
    
def action_show_humidity(colour):
     sense.show_message(get_humidity() + "%", text_colour=colour)
 
def action_show_hostname(colour):
     sense.show_message("hostame: " + hostname, text_colour=colour)

def action_show_ipaddress(colour):
     sense.show_message("ip address: " + ipaddress, text_colour=colour)

def action_text_scroll(colour):
     #while True:
        sense.show_message("Hello, my name is "+ hostname
                           + " - ip address: " + ipaddress
                           + " - temperature: " + get_temp()
                           + "C - humidity: " + get_humidity()
                           + "% - ", text_colour=colour)


running = True

def handle_code(code):
    if code == ecodes.KEY_UP:
        action_show_hostname(cyan)
        action_show_ipaddress(cyan)
    elif code == ecodes.KEY_DOWN:
        action_show_temp(red)
        action_show_humidity(blue)
    elif code == ecodes.KEY_LEFT:
        action_show_hostname(green)
    elif code == ecodes.KEY_RIGHT:
        action_show_humidity(blue)

sense.clear()
while running:
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            if event.value == 1:  # key down
                handle_code(event.code)
            #if event.value == 0:  # key up
            #    handle_code(event.code)
        if event.type == ecodes.KEY_ENTER:
            action_sense_clear()
            running = False
            sys.exit()


    
