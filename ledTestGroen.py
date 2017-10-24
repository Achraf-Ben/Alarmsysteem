import RPi.GPIO as GPIO
import time

groen = 4


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(groen,GPIO.OUT)

print("LED on")

GPIO.output(groen,GPIO.HIGH)
time.sleep(2)
print("LED off")
GPIO.output(groen,GPIO.LOW)
