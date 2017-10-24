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

# Trigger Alarm
sendcommand("justanothergeek1","ls")

# Disarm Alarm
sendcommand("justanothergeek1","python3 alarmOff.py")

# Presence
sendcommand("justanothergeek1","python3 presence.py")
