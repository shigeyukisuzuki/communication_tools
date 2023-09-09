import socket
import ssl
import sys

hostname = sys.argv[1]
port = 992
if len(sys.argv) > 2:
	port = sys.argv[2]

# start tls
context = ssl.create_default_context()

with socket.create_connection((hostname, port)) as sock:
	with context.wrap_socket(sock, server_hostname=hostname) as ssock:
		#print(ssock.version())
		while True:
			response = ssock.recv(4096)
			print(response.decode('UTF8'), end='')
