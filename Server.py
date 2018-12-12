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

data=""
    
while True:
	connectionSocket, addr=serverSocket.accept()
	print('Connected by', addr)
	filename='test.txt'
	f = open(filename,'rb')
	l = f.read(1024)
	while (l):
		connectionSocket.send(l)
		print('Sent ',repr(l))
		l = f.read(1024)
	f.close()
	
	print("Done sending")
	
	connectionSocket.close()
