import socket

targetHost = '127.0.0.1'
targetPort = 9995

# generate socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send data to target
client.sendto(b'AAABBBCCC', (targetHost, targetPort))

# receive data from target
data, address = client.recvfrom(4096)

print(data.decode('utf-8'))
print(address)

client.close()
