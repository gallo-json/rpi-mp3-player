import os
import RPi.GPIO as GPIO
import time
import threading
import subprocess
import glob

f = open("password.txt", "r")
p = f.read()
f.close()

button = 14

GPIO.setmode(GPIO.BCM)

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

master, slave = os.openpty()

def pause():
    while True:
        if GPIO.input(button) == False:
                os.write(slave, 's')
                while GPIO.input(button) == False:
                    time.sleep(0.2)
try:
    player = subprocess.Popen(["mpg123", "-Z", "-C"] + glob.glob("../../../../media/pi/usb/*.mp3"), stdin=master)
    t1 = threading.Thread(target=pause, args=())

    t1.start()        
    t1.join()
except KeyboardInterrupt:
    os.system('echo %s|sudo -S %s' % (p, 'whoami'))
    os.write(slave, 'q')
    GPIO.cleanup()
