import re
import socket
import threading

#targetHost = '52.193.48.235'
targetHost = '103.41.63.2'
#targetHost = 'koukoku.shadan.open.ad.jp '
targetPort = 23

# generate TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to target host
client.connect((targetHost, targetPort))

def receive(client):
	# logging
	with open('koukoku.log', 'a', encoding='SJIS') as logFile:
		# receive message
		try:
			while True:
				response = client.recv(4096)
				talk = re.findall("(?<=>> )[^<]*(?=<<)", response.decode('SJIS'))
				if talk:
					message = talk[0]
					print(message)
					logFile.write(message + '\n')
				#print(response,decode())
		except ConnectionAbortedError:
			return

try:
	receiveThread = threading.Thread(target=receive, args=(client, ))
	receiveThread.start()
	while True:
		message = input("")
		if message == 'quit':
			break
		if re.findall("^[a-zA-Z0-9!#$%&'()=~|^@`{:*},./\<>?_\-\[\]" + '"' + "]+$", message):
			message += '。\n'
		else:
			message += '\n'
		# send message
		try:
			client.send(message.encode('SJIS'))
			#print(message.encode('SJIS'))
		except UnicodeEncodeError:
			print("UnicodeEncodeError")
finally:
	receiveThread.join(timeout=0.3)
	client.close()

#print(response.decode())

#receiveThread = threading.Thread(target=receive, args=(client, ))
#sendThread = threading.Thread(target=send, args=(client))
#receiveThread.start()
#sendThread.start()

