import os
import RPi.GPIO as GPIO
import time
import threading
import subprocess

button = 2

GPIO.setmode(GPIO.BCM)

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

stdin, stdout = os.openpty()

def pause():
    while True:
        if GPIO.input(button) == False:
                os.write(stdout, 's')
                while GPIO.input(button) == False:
                    time.sleep(0.2)
try:

    player = subprocess.Popen(['mpg123', '-Z', '-C', '../../../../media/pi/usb/*.mp3'], stdin=stdin)
    t1 = threading.Thread(target=pause, args=())

    t1.start()        
    t1.join()
except KeyboardInterrupt:
    os.write(slave, 'q')
    GPIO.cleanup()
