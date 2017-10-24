import paramiko


def sendCommand(hostname,command):
    """Sends a command over SSH to a remote host using SSH key authentication"""
    try:
        key = paramiko.RSAKey.from_private_key_file("/home/pi/privatekey.pem")
        sshClient = paramiko.SSHClient()
        sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshClient.connect(hostname=hostname, username="pi", pkey=key)  # Connect to host
        stdin,stdout,stderr = sshClient.exec_command(command)  # Runs command
        print(stdout.read())  # Print shell read out
        print(stderr.read())  # Print shell errors
        sshClient.close()
        executed = "Executed: {}".format(command)
        return executed
    except paramiko.ssh_exception.NoValidConnectionsError:
        print("Connection to the Alarm Server got disrupted, triggering Alarm...")
        return False
    except:
        print("Another error occured please contact support.")
