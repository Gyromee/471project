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


#Setup the ephemeral port
# Create a socket
serverSocket2 = socket(AF_INET, SOCK_STREAM)

# Bind the socket to port 0
serverSocket2.bind(('',0))

#Send a file to the client
def uploadToClient(filename):
	# Retreive the ephemeral port number
	print ("I chose ephemeral port: ", serverSocket2.getsockname()[1])

	#Send the ephemeral port number to the client
	connectionSocket.send(str(serverSocket2.getsockname()[1]).encode())

	#listen for new connections on the ephemeral port
	serverSocket2.listen(1)

	#Accept connections on the ephemeral port
	dataSocket, addr2 =serverSocket2.accept()
	
	print('Connected by', addr2)
	
	print("succkerrrrq")	
	
	#Open the file
	fileObj = open(filename.decode(),'r')
	
	# Read 65536 bytes of data
	fileData = fileObj.read(65536)
	
	

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
	fileData = dataSizeStr + str(fileData)

	# The number of bytes sent
	numSent = 0
	print(fileData)
	print("poop")
	# Send the data!
	while len(fileData) > numSent:
		print(numSent)
		numSent = numSent + dataSocket.send(fileData[numSent:].encode())
		print(numSent)
	print("Done sending")
	fileObj.close()
	dataSocket.close()
	print("Closing connection with ", addr, " on port ",serverSocket2.getsockname()[1] )


	

	
	

#Receive a file from the client
def downloadFromClient(filename):
	# Retreive the ephemeral port number
	print ("I chose ephemeral port: ", serverSocket2.getsockname()[1])

	#Send the ephemeral port number to the client
	connectionSocket.send(str(serverSocket2.getsockname()[1]).encode())

	#listen for new connections on the ephemeral port
	serverSocket2.listen(1)

	#Accept connections on the ephemeral port
	dataSocket, addr2 =serverSocket2.accept()
	
	print('Connected by', addr2)
	
	numSent = 0
	print(filename)
	with open(filename, "wb") as f:
		print("Downloading file ", filename)
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
		fileSizeBuff = connectionSocket.recv(10)
			
		# Get the file size
		print(fileSizeBuff)
		fileSize = int(fileSizeBuff.decode())
		
		print ("The file size is " +  str(fileSize))
		
		# Get the file data
		
		print ("The file data is: ")
		print (fileData)
		print('receiving data...')
		fileData = connectionSocket.recv(fileSize)
		bytesDecoded = fileData.decode()
		#print('data=%s', (data))
	
		# write data to a file
		
		f.write(fileData)
		f.close()		
	print('File received successfully!')
	dataSocket.close()
	print("Closing connection with ", addr, " on port ",serverSocket2.getsockname()[1] )
	

#List all files in the directory
def ls():
	path = '.'
	print("succker")
	# Run ls command, get output, and setup the data
	files = os.listdir(path)
	data = ""
	for name in files:
		data += name + "?"
			
		print("im in here")
	
	# Get the size of the data read
	# and convert it to string

	dataSizeStr = str(len(data))
	print(dataSizeStr)
	
	# Prepend 0's to the size string
	# until the size is 10 bytes
	while len(dataSizeStr) < 10:
		dataSizeStr = "0" + dataSizeStr
		
	data = dataSizeStr + str(data)
	
	# The number of bytes sent
	numSent = 0

	# Send the data!
	while len(data) > numSent:
		print(numSent)
		numSent = numSent + connectionSocket.send(data[numSent:].encode())
		print(numSent)
	print("Done sending")

		
	
#Close the connection 
def quit():
	print("Closing connection with ", addr)
	connectionSocket.close()
	sys.exit(0)
	





def clientInput():
	with connectionSocket:
		
		while True:
			print("waiting for command...")
			#Receive a command from the client
			command = connectionSocket.recv(1024)
			
			#If using get or put, split the command to obtain the filename
			string = command.split(b'?')
			stringCount = len(string)
			if(stringCount > 1 and stringCount < 3):
				command, filename = string
				
				print("hey")
				
				print(filename)				
			
			
			command = b'?' + command
			print(command)
			if command == b'?':
				break
			if command == b'?get':		
				uploadToClient(filename)		
			elif command == b'?put':
				print("hi")
				downloadFromClient(filename)
			elif command ==b'?ls':
				ls()
			elif command ==b'?quit':
				print("im qutting")
				quit()
			else:
				print("invalid command")

print ("The server is ready to receive ")
connectionSocket, addr=serverSocket.accept()
print('Connected by', addr)
clientInput()


	#connectionsMade = connectionsMade + 1
	
	#print ("The server is ready to receive. Connections made: ")
	#print (connectionsMade)
