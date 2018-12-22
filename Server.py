#Server Code
from socket import *
import os
import sys

#The port on which to listen
serverPort = sys.argv[1]

#Create a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

#Bind the socket to the port
serverSocket.bind(('', int(serverPort)))


#Start listening for incoming connections
serverSocket.listen()

#Setup the ephemeral port on serverSocket2
#Create a socket
serverSocket2 = socket(AF_INET, SOCK_STREAM)

# Bind the socket to port 0
serverSocket2.bind(('',0))

#Send a file to the client
def uploadToClient(filename):

	#Send the ephemeral port number to the client
	connectionSocket.send(str(serverSocket2.getsockname()[1]).encode())
	ephemeralPort = str(serverSocket2.getsockname()[1])

	#listen for new connections on the ephemeral port
	serverSocket2.listen(1)

	#Accept connections on the ephemeral port
	dataSocket, addr2 =serverSocket2.accept()
	
	print("Connected by " + str(addr2[0]) + " on ephemeral port " + str(ephemeralPort))
	
	#Open the file
	fileObj = open(filename.decode(),'r')
	
	# Read the data
	fileData = fileObj.read()
	
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

	# Send the data
	while len(fileData) > numSent:
		numSent = numSent + dataSocket.send(fileData[numSent:].encode())
	print("Done sending.")
	fileObj.close()
	dataSocket.close()
	print("Closing data channel with ", addr, " on ephemeral port ",serverSocket2.getsockname()[1] )


#Receive a file from the client
def downloadFromClient(filename):

	#Send the ephemeral port number to the client
	connectionSocket.send(str(serverSocket2.getsockname()[1]).encode())
	ephemeralPort = str(serverSocket2.getsockname()[1])
	
	#listen for new connections on the ephemeral port
	serverSocket2.listen(1)

	#Accept connections on the ephemeral port
	dataSocket, addr2 =serverSocket2.accept()
	
	print("Connected by " + str(addr2[0]) + " on ephemeral port " + str(ephemeralPort))

	with open(filename, "wb") as f:
		print("Downloading file ", filename.decode())
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
		dataSocket.settimeout(20)
		fileSizeBuff = dataSocket.recv(10)
			
		# Get the file size
		fileSize = int(fileSizeBuff.decode())
		
		#Make sure the file obeys the size limit
		if(fileSize > 65536):
			print("File size" + str(fileSize) + " exceeds maximum capacity")
			dataSocket.settimeout(20)
			temp = dataSocket.recv(fileSize)
			f.close()
			print("Closing data channel with ", addr, " on ephemeral port ",serverSocket2.getsockname()[1] )
			dataSocket.close()	
			return
		
		print ("The file size is " +  str(fileSize))
		
		# Get the file data
		print('receiving data...')
		dataSocket.settimeout(20)
		fileData = dataSocket.recv(fileSize)
		
		# write data to a file		
		f.write(fileData)
		f.close()
			
	print('File received successfully!')
	print("Closing data channel with ", addr, " on ephemeral port ",serverSocket2.getsockname()[1] )
	dataSocket.close()
	

#List all files in the directory
def ls():
	path = '.'
	
	# Run ls command, get output, and setup the data
	files = os.listdir(path)
	data = ""
	for name in files:
		data += name + "?"
	
	# Get the size of the data read
	# and convert it to string
	dataSizeStr = str(len(data))
	
	# Prepend 0's to the size string
	# until the size is 10 bytes
	while len(dataSizeStr) < 10:
		dataSizeStr = "0" + dataSizeStr
		
	data = dataSizeStr + str(data)
	
	# The number of bytes sent
	numSent = 0

	# Send the data!
	while len(data) > numSent:
		numSent = numSent + connectionSocket.send(data[numSent:].encode())
	print("Done sending")

		
	
#Close the connection 
def quit():
	print("Closing connection with ", addr)
	connectionSocket.close()
	sys.exit(0)
	
def clientInput():
	with connectionSocket:
		
		while True:
			print("\nwaiting for command...")
			#Receive a command from the client
			connectionSocket.settimeout(300)
			command = connectionSocket.recv(1024)
			
			#If using get or put, split the command to obtain the filename
			string = command.split(b'?')
			stringCount = len(string)
			if(stringCount > 1 and stringCount < 3):
				command, filename = string
				
				
			print("SUCCESS: " + command.decode())	
			command = b'?' + command

			if command == b'?':
				break
			if command == b'?get':		
				uploadToClient(filename)		
			elif command == b'?put':				
				downloadFromClient(filename)
			elif command ==b'?ls':
				ls()
			elif command ==b'?quit':				
				quit()
			else:
				print("FAILURE")

print ("The server is ready to receive ")
connectionSocket, addr=serverSocket.accept()
#Initiate three-way hanshake
connectionSocket.settimeout(20)
message = connectionSocket.recv(1024)
if(message == b'SYN'):
	connectionSocket.send(b'SYN ACK')
	#wait for ACK
	connectionSocket.settimeout(20)
	message = connectionSocket.recv(1024)
	if(message == b'ACK'):
		print('Connected by', addr)
		clientInput()
