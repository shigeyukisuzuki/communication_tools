#!/usr/bin/python3

import re
import socket
import sys
import threading

codec = 'cp932'
#codec = 'SJIS'

targetDomainNameOrIpAddr = sys.argv[1]
#print("sys.argv : " + str(sys.argv))
#targetDomainName = 'koukoku.shadan.open.ad.jp'
targetPort = 23
if len(sys.argv) > 2 and sys.argv[2]:
	targetPort = sys.argv[2]

ipv4regex = r"((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])"
if not re.match(ipv4regex, targetDomainNameOrIpAddr):
	addrs = socket.getaddrinfo(targetDomainNameOrIpAddr, None)
	for family, kind, proto, canonname, sockaddr in addrs:
		if proto == 6:
			targetHost = sockaddr[0]
			break
else:
	targetHost = targetDomainNameOrIpAddr

# generate TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(targetHost, targetPort, socket.getservbyport(targetPort, 'tcp'))
# connect to target host
client.connect((targetHost, targetPort))

def receive(client):
	# logging
	with open('koukoku2.log', 'a', encoding='UTF8') as logFile:
		# receive message
		while True:
			try:
				response = client.recv(4096)
				#print(response.decode(codec), end='')
				talk = re.findall("(?<=>> )[^<]*(?=<<)", response.decode(codec))
				if talk:
					message = talk[0]
					print(message)
					logFile.write(message + '\n')
			except ConnectionAbortedError:
				return
			except UnicodeDecodeError:
				print("UnicodeDecodeError", response.decode(codec))

try:
	receiveThread = threading.Thread(target=receive, args=(client, ))
	receiveThread.start()
	while True:
		message = input("")
		if message == 'quit':
			break
		if re.findall(r"^[a-zA-Z0-9!#$%&'()=~|^@`{:*},./\<>?_\-\[\]" + '"' + "]+$", message):
			message += '。\n'
		else:
			message += '\n'
		# send message
		try:
			#client.send(message)
			client.send(message.encode(codec))
			#print(message.encode(codec))
		except UnicodeEncodeError:
			print("UnicodeEncodeError")
finally:
	receiveThread.join(timeout=0.3)
	client.close()
