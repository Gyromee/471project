#Client code
from socket import *
import os
import sys

		
#Name and port number of the server to
# which want to connect
serverName = "192.168.1.114"
#serverName = "192.168.1.133"
serverPort = 12000

#Create a socket
clientSocket = socket(AF_INET, SOCK_STREAM)


def downloadFile(filename):
	numSent = 0
	print(filename)
	with open(filename, "wb") as f:
		print("Downloading file ", filename)
		while True:
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
			print('receiving data...')
			fileData = clientSocket.recv(fileSize)
			bytesDecoded = fileData.decode()
			#print('data=%s', (data))
			if not fileData:
				break
			# write data to a file
			f.write(fileData)
			f.close()
			break
				
		
		print('Successfully got the file')
		print ("Received ", fileSize,  "bytes.")
		print("ftp>", end="")
		
		inputChoice = input()
		choiceInput(inputChoice)
		#replace under with input for switch later
		#clientSocket.close()



def uploadFile():
	numSent = 0
	print ("What file would you like to upload?")
	downloadChoice = input()
	# The name of the file
	fileName = downloadChoice

	# Open the file
	fileObj = open(fileName, "r")
	# The number of bytes sentE`

	# The file data
	fileData = None

	# Keep sending until all is sent
	while True:
		
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
			fileData = dataSizeStr + fileData	
			
			# The number of bytes sent
			numSent = 0
			
			# Send the data!
			while len(fileData) > numSent:
				numSent = numSent + clientSocket.send(fileData[numSent:].encode())
		
		# The file has been read. We are done
		else:
			break


	print ("Sent ", numSent, " bytes.")
	
	
		
	# Close the socket and the file

	fileObj.close()
	
	print("ftp>", end="")
	
	inputChoice = input()
	choiceInput(inputChoice)
	

def listFile():
	print("Below are the files")
	clientSocket.sendall(b'ls')
	while True:
			data = clientSocket.recv(1024)
			#print('data=%s', (data))
			if not data:
				break
			# write data to a file
			print(data.decode())
			
			


			
	
	
	print("ftp>", end="")
	
	inputChoice = input()
	choiceInput(inputChoice)
	

def quitProgram():
	print("Quitting program")
	
	clientSocket.sendall(b'commandQuit')
	clientSocket.close()
	
def test():
	clientSocket.sendall(b'commandTest')
	clientSocket.close()
	
	
def choiceInput(inputChoice):
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
		clientSocket.send(command.encode() + b'_' + filename.encode())
		downloadFile(filename)
	elif command == "put":
		clientSocket.send(inputChoice.encode())
		uploadFile()
	elif command == "ls":
		listFile()
	elif command == "quit":
		quitProgram()


    
def printChoices():
    print("ftp>", end="")

#Connect to the server
clientSocket.connect((serverName, serverPort))
#

#A string we want to send to the server
data= "Hello world! This is a very long string."
value = True
printChoices()
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
