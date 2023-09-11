#!/usr/bin/python3

import getopt
import re
import socket
import ssl
import sys
import threading

def printHelp():
	print("""telnetClient [-v] [-s] [-c codec] [-h] <host> [<port>]
-s: telnets mode
-c <codec>: use connecting with specified codec
-v: verbose print
-h: print this help
""")
	exit(1)

optlist, args = getopt.gnu_getopt(sys.argv[1:], 'c:svh')

if len(args) == 0:
	printHelp()

targetHost = args[0]

#targetDomainNameOrIpAddr = args[0]
#targetDomainNameOrIpAddr = sys.argv[1]
#print("sys.argv : " + str(sys.argv))
#targetDomainName = 'koukoku.shadan.open.ad.jp'

# default value
codec = 'cp932'
#codec = 'SJIS'
targetPort = 23
if len(args) > 2 and args[1]:
	targetPort = args[1]
#if len(sys.argv) > 2 and sys.argv[2]:
#	targetPort = sys.argv[2]
telnetsMode = False
def printVerbose(*message, file=sys.stderr):
	pass

for opt, arg in optlist:
	if opt == '-c':
		codec = arg
	elif opt == '-s':
		telnetsMode = True
		targetPort = 992
		codec = 'UTF8'
	elif opt == '-v':
		printVerbose = print
	elif opt == '-h':
		printHelp()
		
#ipv4regex = r"((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])"
#if not re.match(ipv4regex, targetDomainNameOrIpAddr):
#	addrs = socket.getaddrinfo(targetDomainNameOrIpAddr, None)
#	for family, kind, proto, canonname, sockaddr in addrs:
#		if proto == 6:
#			targetHost = sockaddr[0]
#			break
#else:
#	targetHost = targetDomainNameOrIpAddr

# generate TCP socket
#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

printVerbose(targetHost, targetPort, socket.getservbyport(targetPort, 'tcp'))
# connect to target host
#client.connect((targetHost, targetPort))
client = socket.create_connection((targetHost, targetPort))

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
	telnetClient = None
	if telnetsMode == True:
		# start tls
		context = ssl.create_default_context()
		telnetClient = client
		client = context.wrap_socket(client, server_hostname=targetHost)
	receiveThread = threading.Thread(target=receive, args=(client, ), daemon=True)
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
	if telnetClient:
		telnetClient.close()
