#!/usr/bin/python3

import getopt
import re
import socket
import ssl
import sys
import threading

def printHelp():
	print("""telnetClient [-c codec] [-r regex] [-s] [-v] [-h] <host> [<port>]
-c <codec>: use connecting with specified codec
-r <regex>: print text specified by regex
-s: telnets mode
-v: verbose print
-h: print this help
""")
	exit(1)

optlist, args = getopt.gnu_getopt(sys.argv[1:], 'c:r:svh')

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
textRegex = ""
telnetsMode = False
def printVerbose(*message, file=sys.stderr):
	pass

for opt, arg in optlist:
	if opt == '-c':
		codec = arg
	elif opt == '-r':
		textRegex = arg
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

printVerbose(targetHost, targetPort, socket.getservbyport(targetPort, 'tcp'), file=sys.stderr)
# connect to target host
#client.connect((targetHost, targetPort))
client = socket.create_connection((targetHost, targetPort))
printVerbose("connect {} port {} from {} port {}, timeout = {}".format(*client.getpeername(), *client.getsockname(), client.gettimeout()), file=sys.stderr)

# thread function definition
def receive(client):
	# logging
	with open('koukoku2.log', 'a', encoding='UTF8') as logFile:
		# receive message
		while True:
			try:
				response = client.recv(4096).decode(codec)
				#print(response.decode(codec), end='')
				if textRegex:
					#talk = re.findall("(?<=>> )[^<]*(?=<<)", response.decode(codec))
					talk = re.findall(textRegex, response)
					if talk:
						message = talk[0]
					else:
						continue
				else:
					message = response
				print(message, flush=True, end='')
				logFile.write(message + '\n')
			except ConnectionAbortedError:
				return
			except UnicodeDecodeError:
				print("UnicodeDecodeError", response)

# main routine
if __name__ == '__main__':
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
