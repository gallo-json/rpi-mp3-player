import os

# os.system("mpg123 '../../media/pi/USB STICK/Czerny - Nocturne in E-flat major.mp3'")

import RPi.GPIO as GPIO
import time

button = 2
led    = 3

'''
def setup():
       GPIO.setmode(GPIO.BCM)
       GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
       GPIO.setup(led, GPIO.OUT)

def loop():
        while True:
              button_state = GPIO.input(button)
              if  button_state == False:
                  GPIO.output(led, True)
                  print('Button Pressed...')
                  while GPIO.input(button) == False:
                    time.sleep(0.2)
              else:
                  GPIO.output(led, False)

def endprogram():
         GPIO.output(led, False)
         GPIO.cleanup()


if __name__ == '__main__':

          setup()

          try:
                 loop()

          except KeyboardInterrupt:
                 endprogram()

'''
import RPi.GPIO as GPIO
import time
import threading
import subprocess

GPIO.setmode(GPIO.BCM)

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led, GPIO.OUT)

master, slave = os.openpty()

player = subprocess.Popen(['mpg123', '-C', '../../../../media/pi/USB STICK/Czerny - Nocturne in E-flat major.mp3'], stdin=master)
def stop():
    while True:
        if GPIO.input(button) == False:
                # GPIO.output(led, True)
                os.write(slave, 's')
                while GPIO.input(button) == False:
                    time.sleep(0.2)
try:
        t1 = threading.Thread(target=stop, args=())

        t1.start()

        t1.join()
except KeyboardInterrupt:
        os.write(slave, 'q')
        GPIO.cleanup()
