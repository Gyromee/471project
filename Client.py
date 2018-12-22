#Client code
from socket import *
import os
import sys
import base64

#Create a socket
clientSocket = socket(AF_INET, SOCK_STREAM)


def downloadFile(filename):
	dataSocket = socket(AF_INET, SOCK_STREAM)
	numSent = 0
	dataSocket.settimeout(20)
	ephemeralPortString = clientSocket.recv(1024).decode()
	ephemeralPortInt = int(ephemeralPortString)
	print(ephemeralPortInt)
	
	dataSocket.connect((serverName, ephemeralPortInt))

	with open(filename, "w") as f:
		print("Downloading file ", filename)
		# The buffer to all data received from the
		# the client.
		fileData = ""
		
		# The temporary buffer to store the received
		# data.
		
		
		# The size of the incoming file
		fileSize = 0	
		
		# The buffer containing the file size
		fileSizeBuff = ""
		
		# Receive the first 10 bytes indicating the
		# size of the file
		dataSocket.settimeout(20)
		fileSizeBuff = dataSocket.recv(10)
		

			
			
		# Get the file size
		fileSize = int(fileSizeBuff)
		if(fileSize > 65536):
			print("File size exceeds maximum capacity")
			dataSocket.settimeout(20)
			tmp = dataSocket.recv(fileSize)
			f.close()
			dataSocket.close()
			print("ftp>", end="")
			
			inputChoice = input()
			choiceInput(inputChoice)
			
		
		
		# Get the file data
		dataSocket.settimeout(20)
		fileData = dataSocket.recv(fileSize)
		#times out after 20 seconds 
		
		bytesDecoded = fileData.decode()
		#print('data=%s', (data))
	
		# write data to a file
		f.write(fileData.decode())
		f.close()
		
				
		
		print('Successfully got the file ' + filename  )
		print('The file size is ' + str(fileSize) + ' bytes')
		print("ftp>", end="")
		
		inputChoice = input()
		choiceInput(inputChoice)

def uploadFile(filename):
	dataSocket = socket(AF_INET, SOCK_STREAM)
	numSent = 0
	dataSocket.settimeout(20)
	ephemeralPortString = clientSocket.recv(1024).decode()
	ephemeralPortInt = int(ephemeralPortString)
	
	dataSocket.connect((serverName, ephemeralPortInt))
	# The name of the file
	

	# Open the file
	fileObj = open(filename, "r")
	# The number of bytes sentE`

	# The file data
	fileData = None

	# Keep sending until all is sent
		
	# Read 65536 bytes of data
	fileData = fileObj.read()
	
	# Make sure we did not hit EOF
		
			
	# Get the size of the data read
	# and convert it to string
	dataSizeStr = str(len(fileData))
	
	# Prepend 0's to the size string
	# until the size is 10 bytes
	while len(dataSizeStr) < 10:
		dataSizeStr = "0" + dataSizeStr


	# Prepend the size of the data to the
	# file data.
	fileData = dataSizeStr + fileData	
	
	# The number of bytes sent
	numSent = 0
	
	# Send the data!
	while len(fileData) > numSent:
		numSent = numSent + dataSocket.send(fileData[numSent:].encode())
	


	print ("Sent ", numSent, " bytes.")
	
	
		
	# Close the socket and the file

	fileObj.close()
	dataSocket.close()
	print("ftp>", end="")
	
	inputChoice = input()
	choiceInput(inputChoice)
	

def listFile():
	clientSocket.sendall(b'ls')
	data = ""
	
# The buffer to all data received from the
	# the client.
	fileData = ""
	
	# The temporary buffer to store the received
	# data.
	recvBuff = ""
	
	# The size of the incoming file
	fileSize = 0	
	
	# The buffer containing the file size
	fileSizeBuff = ""
	
	# Receive the first 10 bytes indicating the
	# size of the file
	clientSocket.settimeout(20)
	fileSizeBuff = clientSocket.recv(10)
		
	# Get the file size
	fileSize = int(fileSizeBuff)
	
	# Get the file data
	
	clientSocket.settimeout(20)
	fileData = clientSocket.recv(fileSize)
	bytesDecoded = fileData.decode()
	string = fileData.split(b'?')
	for name in string:
		print(name.decode())
	
	print("ftp>", end="")
	
	inputChoice = input()
	choiceInput(inputChoice)
	
def quitProgram():
	print("Quitting program")
	
	clientSocket.sendall(b'quit')
	clientSocket.close()
	sys.exit(0)
	

	
def choiceInput(inputChoice):
	while True:
	
		string = inputChoice.split()
		stringCount = len(string)
		if(stringCount > 1):
			command, filename = string
		else:
			command = inputChoice
		if command == "get":
			clientSocket.send(command.encode() + b'?' + filename.encode())
			downloadFile(filename)
			dataSocket.close()
		elif command == "put":
			clientSocket.send(command.encode() + b'?' + filename.encode())
			uploadFile(filename)
			dataSocket.close()
		elif command == "ls":
			listFile()
		elif command == "quit":
			quitProgram()
		else:
			print("Invalid command")
			print("ftp>", end="")
			inputChoice = input()
		

#Connect to the server
serverName = sys.argv[1]
serverPort = sys.argv[2]

#Initiating handshake
print("Requesting connection to serverName. Sending SYN")
clientSocket.connect(((serverName), int(serverPort)))
clientSocket.send(b'SYN')
clientSocket.settimeout(10)
ACK = clientSocket.recv(10).decode()


if(ACK == "SYN ACK"):
	print("Received SYN ACK, sending ACK")
	clientSocket.send(b'ACK')
	print("ftp>", end="")
	inputChoice = input()
	choiceInput(inputChoice)
	

#Close the socket
clientSocket.close()

