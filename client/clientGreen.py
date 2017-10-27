import RPi.GPIO as GPIO


rood = 3
geel = 5
groen = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(rood, GPIO.OUT)
GPIO.setup(geel, GPIO.OUT)
GPIO.setup(groen, GPIO.OUT)

GPIO.output(rood, GPIO.LOW)
GPIO.output(geel, GPIO.LOW)
GPIO.output(groen, GPIO.HIGH)
