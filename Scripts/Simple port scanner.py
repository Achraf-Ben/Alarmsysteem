import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

target = "pythonprogramming.net"

def pscan(port):
    try:
        con = s.connect((target,port))
        return True
    except:
        return False


for x in range(79,100):
    if pscan(x):
        print('Port',x,'is open')
    else:
        print('Port',x,'is closed')
