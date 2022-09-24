#!/usr/bin/python
from sense_hat import SenseHat
import socket

sense = SenseHat()
sense.set_rotation(180)
red = (255, 0, 0)
blue= (0, 0, 255)

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

while True:
    sense.show_message("Hello, my name is "+ hostname + " " + ip + " Tmp: " + str(round(sense.get_temperature(),1))+ " C Hmdty: " + str(round(sense.get_humidity(),0)) + "% ", text_colour=blue)
