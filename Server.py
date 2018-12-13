#Server Code
from socket import *
import os
import sys

#The port on which to listen
serverPort = 12000

#Create a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

#Bind the socket to the port
serverSocket.bind(('', serverPort))

#Start listening for incoming connections
serverSocket.listen()

#Send a file to the client
def uploadToClient(filename):
	print("succkerrrrq")	
	
	#Open the file
	fileObj = open(filename.decode(),'r')
	
	# Read 65536 bytes of data
	fileData = fileObj.read(65536)
	
	

	# Make sure we did not hit EOF
	if fileData:

		# Get the size of the data read
		# and convert it to string
		
		dataSizeStr = str(len(fileData))

		# Prepend 0's to the size string
		# until the size is 10 bytes
		while len(dataSizeStr) < 10:
			dataSizeStr = "0" + dataSizeStr

		# Prepend the size of the data to the
		# file data.
		fileData = dataSizeStr + str(fileData)

		# The number of bytes sent
		numSent = 0

		# Send the data!
		while len(fileData) > numSent:
			print(numSent)
			numSent = numSent + connectionSocket.send(fileData[numSent:].encode())
			print(numSent)
		print("Done sending")
		fileObj.close()
		
	# The file has been read. We are done
	else:
		print("hey")
	
	#Return to the main function for reading client input commands
	clientInput()
	

	
	

#Receive a file from the client
def downloadFromClient(filename):
	print("succkerrrrq")
	# The buffer
	recvBuff = ""
	
	# The temporary buffer
	tmpBuff = ""
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	
	print(recvBuff)
	clientInput()
	

#List all files in the directory
def ls():
	path = '.'
	print("succker")
	# Run ls command, get output, and print it
	files = os.listdir(path)
	
	clientInput()
		
	
#Close the connection 
def quit():
	print("Closing connection with ", addr)
	connectionSocket.close()
	





def clientInput():
	print("hyyy")
	with connectionSocket:
		while True:
			#Receive a command from the client
			command = connectionSocket.recv(1024)
			print(command)
			#If using get or put, split the command to obtain the filename
			string = command.split(b'_')
			stringCount = len(string)
			if(stringCount > 1 and stringCount < 3):
				command, filename = string
				
				print("hey")
				
				print(filename)				
			
			
			command = b'_' + command
			if not command:
				break;
			if command == b'_get':
				uploadToClient(filename)
			elif command == b'_put':
				print("hi")
				downloadFromClient()
			elif command ==b'_ls':
				ls()
			elif command ==b'_quit':
				quit()
			if command == b'commandTest':
				uploadToClient()
		
	

print ("The server is ready to receive ")
connectionSocket, addr=serverSocket.accept()
print('Connected by', addr)
clientInput()


	#connectionsMade = connectionsMade + 1
	
	#print ("The server is ready to receive. Connections made: ")
	#print (connectionsMade)
