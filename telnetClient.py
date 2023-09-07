import re
import socket
import sys
import threading

targetDomainName = sys.argv[1]
#targetDomainName = 'koukoku.shadan.open.ad.jp'
targetPort = 23
if len(sys.argv) > 2 and sys.argv[2]:
	targetPort = sys.argv[2]

addrs = socket.getaddrinfo(targetDomainName, None)
for family, kind, proto, canonname, sockaddr in addrs:
	if proto == 6:
		targetHost = sockaddr[0]
		break

# generate TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to target host
#targetHost = '52.193.48.235'
#targetHost = '103.41.63.2'
client.connect((targetHost, targetPort))

def receive(client):
	# logging
	with open('koukoku2.log', 'a', encoding='UTF8') as logFile:
		# receive message
		while True:
			try:
				response = client.recv(4096)
				talk = re.findall("(?<=>> )[^<]*(?=<<)", response.decode('SJIS'))
				if talk:
					message = talk[0]
					print(message)
					logFile.write(message + '\n')
				#print(response,decode())
			except ConnectionAbortedError:
				return
			except UnicodeDecodeError:
				print("UnicodeDecodeError")

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

