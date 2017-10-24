import paramiko


def sendCommand(hostname,command):
    'Sends a command over SSH to a remote host using SSH key authentication'
    k = paramiko.RSAKey.from_private_key_file("/home/pi/privatekey.pem")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #print("connecting")
    c.connect( hostname = hostname, username = "pi", password = "AlarmSystem" )
    #print("connected")
    execute = "Execute: {}".format(command)
    stdin,stdout,stderr = c.exec_command(command)
    print(stdout.read())
    #print()
    #print( "Errors")
    print(stderr.read())
    c.close()
    return execute
