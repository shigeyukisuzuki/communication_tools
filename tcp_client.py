import socket

targetHost = 'www.google.com'
targetPort = 80

# generate TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to target host
client.connect((targetHost, targetPort))

# send message
client.send(b'GET / HTTP1.1\r\nHost: google.com\r\n\r\n')

# receive message
response = client.recv(4096)

print(response.decode())
client.close()

