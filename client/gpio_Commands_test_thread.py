import RPi.GPIO as GPIO
import time
from sshConnect import sendCommand
import threading

# geeft de gpio-pins nummer een naam
rood = 3
geel = 5
groen = 7
button1 = 15
button2 = 23
button3 = 31

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# initialiseren van de hardware
GPIO.setup(rood, GPIO.OUT)
GPIO.setup(geel, GPIO.OUT)
GPIO.setup(groen, GPIO.OUT)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#bij het opstarten gaan eerst alle lampjes aan
print("Booting up...")
GPIO.output(rood, GPIO.HIGH)
GPIO.output(geel, GPIO.HIGH)
GPIO.output(groen, GPIO.HIGH)
time.sleep(1)
#alarm staat aan, dit is te zien door de groene led
print("System running")
GPIO.output(rood, GPIO.LOW)
GPIO.output(geel, GPIO.LOW)
GPIO.output(groen, GPIO.HIGH)


def updateTimeDatabase():
    print('updateTimeDatabase call!')
    while True:
        print('updateTimeDatabase, loop')
        try:
            sendCommand("server.pi", "cd Alarmsysteem && python3 /home/pi/Alarmsysteem/updateTime.py")
        except:
            GPIO.output(rood, GPIO.HIGH)
            GPIO.output(geel, GPIO.LOW)
            GPIO.output(groen, GPIO.LOW)
        time.sleep(20)



def alarmOn():
    if sendCommand("server.pi", "cd Alarmsysteem && python3 /home/pi/Alarmsysteem/alarmOn.py") == False:
        print("Cant connect to server alarm triggerd")
    else:
        print("Alarm Triggerd")
    GPIO.output(rood, GPIO.HIGH)
    GPIO.output(geel, GPIO.LOW)
    GPIO.output(groen, GPIO.LOW)

def alarmOff(escape):
    GPIO.output(rood, GPIO.LOW)
    GPIO.output(geel, GPIO.LOW)
    GPIO.output(groen, GPIO.HIGH)
    if escape == False:
        if sendCommand("server.pi", "cd Alarmsysteem && python3 /home/pi/Alarmsysteem/alarmOff.py") == False:
            print("Alarm Triggerd Server error")
            GPIO.output(rood, GPIO.HIGH)
            GPIO.output(geel, GPIO.LOW)
            GPIO.output(groen, GPIO.LOW)
        else:
            print("Alarm Disarmed")

# Maakt nieuwe thread aan om de tijd weg te schrijven in de database
threadUpdateTime = threading.Thread(target=updateTimeDatabase)
threadUpdateTime.start()

while True:

    input_state1 = GPIO.input(button1)
    input_state2 = GPIO.input(button2)
    input_state3 = GPIO.input(button3)

    #kijkt of button 1/button 2 wordt ingedrukt
    if input_state1 == True or input_state2 == True:
        print('Button 1 or 2 is Pressed')  # Triggers Alarm
        GPIO.output(rood, GPIO.LOW)
        GPIO.output(geel, GPIO.HIGH)
        GPIO.output(groen, GPIO.LOW)

        timeout = 5  # [seconds]

        timeout_start = time.time()

        alarmEscaped = False
        # geeft voor 5 seconden de tijd om het alarm te disablen
        while time.time() < timeout_start + timeout:
            input_state3 = GPIO.input(button3)
            if input_state3 == True:
                print("escape button is pressed!")
                print("Alarm Disarmed")
                alarmEscaped = True
                alarmOff(True)
                time.sleep(1)
                break

        if alarmEscaped == False:
            alarmOn()

    elif input_state3 == True:
        alarmOff(False)

