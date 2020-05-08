import os
import RPi.GPIO as GPIO
import time
import threading
import subprocess
import glob

pause_play = 14
vol_up = 15

GPIO.setmode(GPIO.BCM)


GPIO.setup(pause_play, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(vol_up, GPIO.IN, pull_up_down=GPIO.PUD_UP)

master, slave = os.openpty()

os.system('mount /dev/sda1 ../../../../media/pi/usb')

def pause():
    while True:
        if GPIO.input(pause_play) == False:
                os.write(slave, 's')
                while GPIO.input(pause_play) == False:
                    time.sleep(0.2)

def volume_up():
    while True:
        if GPIO.input(vol_up) == False:
                os.write(slave, 'f')
                while GPIO.input(vol_up) == False:
                    time.sleep(0.2)

try:
    player = subprocess.Popen(["mpg123", "-Z", "-C"] + glob.glob("../../../../media/pi/usb/*.mp3"), stdin=master)
    t1 = threading.Thread(target=pause, args=())
    t2 = threading.Thread(target=volume_up, args=())

    t1.start()
    t2.start()

    t1.join()
    t2.join()
except KeyboardInterrupt:
    os.write(slave, 'q')
    GPIO.cleanup()
