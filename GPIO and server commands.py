import RPi.GPIO as GPIO
import time
import paramiko

def sendcommand(hostname,command):
    'Sends a command over SSH to a remote host using SSH key authentication'
    k = paramiko.RSAKey.from_private_key_file("/home/pi/alarmsystem/privatekey.pem")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("connecting")
    c.connect( hostname = hostname, username = "pi", password = "AlarmSystem" )
    print("connected")
    print("Executing {}".format( command ))
    stdin , stdout, stderr = c.exec_command(command)
    print(stdout.read())
    print( "Errors")
    print(stderr.read())
    c.close()

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
    sendcommand("justanothergeek1", "echo Presence > Presence.txt")
    
    if input_state1 == True:
        print('Button 1 Pressed')
        GPIO.output(rood, GPIO.LOW)
        GPIO.output(geel, GPIO.HIGH)
        GPIO.output(groen, GPIO.LOW)
        time.sleep(5)
        GPIO.output(rood, GPIO.HIGH)
        GPIO.output(geel, GPIO.LOW)
        GPIO.output(groen, GPIO.LOW)
        sendcommand("justanothergeek1", "echo Trigger > trigger.txt")

    elif input_state2 == True:
        print('Button 2 Pressed')
        GPIO.output(rood, GPIO.LOW)
        GPIO.output(geel, GPIO.LOW)
        GPIO.output(groen, GPIO.HIGH)       #Slaat deze zonder reden over
        time.sleep(5)
        GPIO.output(rood, GPIO.HIGH)
        GPIO.output(geel, GPIO.LOW)
        GPIO.output(groen, GPIO.LOW)

    elif input_state3 == True:
        print("Button 3 Pressed")
        GPIO.output(rood, GPIO.LOW)
        GPIO.output(geel, GPIO.LOW)
        GPIO.output(groen, GPIO.HIGH)
        time.sleep(0.2)
        sendcommand("justanothergeek1", "echo Disarm > Disarm.txt")

