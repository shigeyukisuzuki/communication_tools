import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("127.0.0.1", 7))
serverSocket.listen(1)
clientSocket, client_address = serverSocket.accept()
print("Connection from:", client_address)

while True:
	data = clientSocket.recv(1024)
	str_data = data.decode()
	if not data:
		break
	print("Received from client:", str_data)
	clientSocket.send(data)

clientSocket.close()