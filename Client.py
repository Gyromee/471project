#Client code
from socket import *

#Name and port number of the server to
# which want to connect
serverName = "192.168.1.133"
serverPort = 12000

#Create a socket
clientSocket = socket(AF_INET, SOCK_STREAM)

#Connect to the server
clientSocket.connect((serverName, serverPort))

clientSocket.sendall(b'KILL MEVIN CHEN')
data = clientSocket.recv(1024)

print('Received', repr(data))

#Close the socket
clientSocket.close()