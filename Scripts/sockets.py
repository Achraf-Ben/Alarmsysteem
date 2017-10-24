import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server to communicate with
server = 'pythonprogramming.net'
port = 80

#Get server ip by hostname
server_ip = socket.gethostbyname(server)

print(server,server_ip)

#Get request
request = "GET / HTTP/1.1\nHost: "+server+"\n\n"

s.connect((server, port))  #Makes a connection to server and port
s.send(request.encode())  #
result = s.recv(4096)  #Buffer, how large the datachunks will be

while (len(result) > 0):
    print(result)
    result = s.recv(4096)
