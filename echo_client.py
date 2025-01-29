import socket

clientSocket = socket.socket()
clientSocket.connect(("127.0.0.1", 7))
while True:
	data = input("$ ")
	clientSocket.send(data.encode())
	if not data:
		break
	newData = clientSocket.recv(1024)
	print("Received from server:", str(newData.decode()))

clientSocket.close()