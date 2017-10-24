import RPi.GPIO as GPIO
import time
from sshconnect import sendCommand

rood = 3
geel = 5
groen = 7
button1 = 15
button2 = 23
button3 = 31

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(rood, GPIO.OUT)
GPIO.setup(geel, GPIO.OUT)
GPIO.setup(groen, GPIO.OUT)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Booting up...")
GPIO.output(rood, GPIO.HIGH)
GPIO.output(geel, GPIO.HIGH)
GPIO.output(groen, GPIO.HIGH)
time.sleep(1)
print("System running")
GPIO.output(rood, GPIO.LOW)
GPIO.output(geel, GPIO.LOW)
GPIO.output(groen, GPIO.HIGH)

while True:
    input_state1 = GPIO.input(button1)
    input_state2 = GPIO.input(button2)
    input_state3 = GPIO.input(button3)
    # Update presence time
    # sendCommand("justanothergeek1", "echo Presence > Presence.txt")

    if input_state1 == True:
        
        print('Button 1 Pressed')   # Triggers Alarm
        GPIO.output(rood, GPIO.LOW)
        GPIO.output(geel, GPIO.HIGH)
        GPIO.output(groen, GPIO.LOW)
        time.sleep(5)
        GPIO.output(rood, GPIO.HIGH)
        GPIO.output(geel, GPIO.LOW)
        GPIO.output(groen, GPIO.LOW)
        sendCommand("justanothergeek1", "triggerAlarm.py")
        print("Alarm Triggerd")

    elif input_state2 == True:
        print('Button 2 Pressed')   # Clears from Danger
        GPIO.output(rood, GPIO.LOW)
        GPIO.output(geel, GPIO.LOW)
        GPIO.output(groen, GPIO.HIGH)       #Slaat deze zonder reden over
        time.sleep(5)
        GPIO.output(rood, GPIO.HIGH)
        GPIO.output(geel, GPIO.LOW)
        GPIO.output(groen, GPIO.LOW)
        if sendCommand("justanothergeek1", "clearAlarm.py") == False:
            print("Alarm triggerd")
            GPIO.output(rood, GPIO.HIGH)
            GPIO.output(geel, GPIO.LOW)
            GPIO.output(groen, GPIO.LOW)
        else:
            print("Alarm Disarmed")
            GPIO.output(rood, GPIO.LOW)
            GPIO.output(geel, GPIO.LOW)
            GPIO.output(groen, GPIO.HIGH)

    elif input_state3 == True:
        print("Button 3 Pressed")   # Clears Alarm
        GPIO.output(rood, GPIO.LOW)
        GPIO.output(geel, GPIO.LOW)
        GPIO.output(groen, GPIO.HIGH)
        time.sleep(0.2)
        if sendCommand("justanothergeek1", "clearAlarm.py") == False:
            print("Alarm Triggerd")
            GPIO.output(rood, GPIO.HIGH)
            GPIO.output(geel, GPIO.LOW)
            GPIO.output(groen, GPIO.LOW)
        else:
            print("Alarm Disarmed")
            GPIO.output(rood, GPIO.LOW)
            GPIO.output(geel, GPIO.LOW)
            GPIO.output(groen, GPIO.HIGH)

