#Client code
from socket import *
import os
import sys

		
#Name and port number of the server to
# which want to connect
serverName = "192.168.1.114"
#serverName = "192.168.1.133"
serverPort = 12000
ephemeralPort = 1234

#Create a socket
clientSocket = socket(AF_INET, SOCK_STREAM)


def downloadFile(filename):
	dataSocket = socket(AF_INET, SOCK_STREAM)
	numSent = 0
	ephemeralPortString = clientSocket.recv(1024).decode()
	ephemeralPortInt = int(ephemeralPortString)
	print(ephemeralPortInt)
	
	dataSocket.connect((serverName, ephemeralPortInt))
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
		
		fileSizeBuff = dataSocket.recv(10)

			
			
		# Get the file size
		print(fileSizeBuff)
		fileSize = int(fileSizeBuff)
		
		print ("The file size is " +  str(fileSize))
		
		# Get the file data
		
		print('receiving data...')
		fileData = dataSocket.recv(fileSize)
		bytesDecoded = fileData.decode()
		#print('data=%s', (data))
	
		# write data to a file
		f.write(fileData)
		f.close()
		
				
		
		print('Successfully got the file ' + filename  )
		print('The file size is ' + str(fileSize) + ' bytes')
		print("ftp>", end="")
		
		inputChoice = input()
		choiceInput(inputChoice)
		#replace under with input for switch later
		#clientSocket.close()





def uploadFile(filename):
	dataSocket = socket(AF_INET, SOCK_STREAM)
	numSent = 0
	ephemeralPortString = clientSocket.recv(1024).decode()
	ephemeralPortInt = int(ephemeralPortString)
	print(ephemeralPortInt)
	
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
		numSent = numSent + clientSocket.send(fileData[numSent:].encode())
	
	# The file has been read. We are done
	#else:
	#	break


	print ("Sent ", numSent, " bytes.")
	
	
		
	# Close the socket and the file

	fileObj.close()
	
	print("ftp>", end="")
	
	inputChoice = input()
	choiceInput(inputChoice)
	

def listFile():
	print("Below are the files")
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
	fileSizeBuff = clientSocket.recv(10)
		
	# Get the file size
	print(fileSizeBuff)
	fileSize = int(fileSizeBuff)
	
	print ("The file size is " +  str(fileSize))
	
	# Get the file data
	
	print ("The file data is: ")
	print (fileData)

	fileData = clientSocket.recv(fileSize)
	bytesDecoded = fileData.decode()
	#print('data=%s', (data))
	# write data to a file
	string = fileData.split(b'?')
	for name in string:
		print(name.decode())
	
	print("ftp>", end="")
	
	inputChoice = input()
	choiceInput(inputChoice)
	
	
	
	#print(data)
	
	

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
			print(command)
			print(filename)
		else:
			command = inputChoice

		if command == "get":
			print(inputChoice.encode())
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
			


    

#Connect to the server
clientSocket.connect((serverName, serverPort))
#

print("ftp>", end="")
inputChoice = input()
choiceInput(inputChoice)



#Keep sending bytes until all bytes are sent



# while byteSent != len(data):
    # #send that string!
    # byteSent += clientSocket.send(data[byteSent :])
    # print  ("Trying to send")
    # print (data)


#Close the socket
clientSocket.close()

