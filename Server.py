#Server Code
from socket import *

#The port on which to listen
serverPort = 12000

#Create a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

#Bind the socket to the port
serverSocket.bind(('', serverPort))

#Start listening for incoming connections
serverSocket.listen()

print ("The server is ready to receive ")

connectionSocket, addr=serverSocket.accept()

with connectionSocket:
	print('Connected by', addr)
	
	while True:
		data = connctionSocket.recv(1024)
		if not data:
			break
		connectionSocket.sendall(data)
