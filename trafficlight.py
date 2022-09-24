#!/usr/bin/python
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT) #RED
GPIO.setup(27, GPIO.OUT) #GREEN
GPIO.setup(17, GPIO.OUT) #BLUE

GPIO.output(22,100)
GPIO.output(27,100)
GPIO.output(17,100)

PWMR1=GPIO.PWM(22,100);
PWMG1=GPIO.PWM(27,100);
PWMB1=GPIO.PWM(17,100);
# 
for count in range(10):
    PWMR1.start(1)
    PWMG1.start(1)
    PWMB1.start(1)
    time.sleep(4)

GPIO.cleanup()
