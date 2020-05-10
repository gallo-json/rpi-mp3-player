import os
import RPi.GPIO as GPIO
import time
import threading
import subprocess
import glob

pause_play = 14
next_track = 15
vol_up = 18
vol_d = 23

GPIO.setmode(GPIO.BCM)

GPIO.setup(pause_play, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(next_track, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(vol_up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(vol_d, GPIO.IN, pull_up_down=GPIO.PUD_UP)

master, slave = os.openpty()

os.system('mount /dev/sda1 ../../../../media/pi/usb')

def button(pin, c):
    while True:
        if GPIO.input(pin) == False:
                os.write(slave, c)
                while GPIO.input(pin) == False:
                    time.sleep(0.2)

def volume(pin, c):
    while True:
        if GPIO.input(pin) == False:
            # subprocess.call(["/bin/bash", "-i", "-c", c])
            os.system(c)
            while GPIO.input(pin) == False:
                time.sleep(0.2)


try:
    player = subprocess.Popen(["mpg123", "-Z", "-C"] + glob.glob("../../../../media/pi/usb/*.mp3"), stdin=master)
    threads = [threading.Thread(target=button, args=(pause_play, 's')),    
                threading.Thread(target=button, args=(next_track, 'f')),
                threading.Thread(target=volume, args=(vol_up, "amixer -M set PCM 5%+")),
                threading.Thread(target=volume, args=(vol_d, "amixer -M set PCM 5%-"))]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

except KeyboardInterrupt:
    GPIO.cleanup()
