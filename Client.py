#Client code
from socket import *

		
#Name and port number of the server to
# which want to connect
serverName = "192.168.1.114"
serverPort = 12000

#Create a socket
clientSocket = socket(AF_INET, SOCK_STREAM)


def downloadFile():
	print ("What file would you like to download?")
	downloadChoice = input()
	clientSocket.connect((serverName, serverPort))
	#clientSocket.send(input)
	with open('received_file', 'wb') as f:
		print("file opened")
		while True:
			print('receiving data...')
			data = clientSocket.recv(1024)
			#print('data=%s', (data))
			if not data:
				break
			# write data to a file
			f.write(data)
			
	f.close()
	print('Successfully get the file')
	#replace under with input for switch later
	print('connection closed')
	return



def uploadFile():
	print("Upload file")
	return;
	

def listFile():
	print("List file")

def quitProgram():
	print("Quitting program")
	clientSocket.close()
	print("Connection now closed")
	
def choiceInput(inputChoice):

	if inputChoice == "1":
		downloadFile()
		printChoices()
		inputChoice = input()
		choiceInput(inputChoice)
	elif inputChoice == "2":
		uploadFile()
	elif inputChoice == "3":
		listFile()
	elif inputChoice == "4":
		quitProgram()

	
def printChoices():
	print ("Hello. What would you like to do?")
	print ("1. Download file")
	print ("2. Upload file")
	print ("3. List files")
	print ("4. Quit")	
		


#Connect to the server
#clientSocket.connect((serverName, serverPort))

#A string we want to send to the server
data= "Hello world! This is a very long string."

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
