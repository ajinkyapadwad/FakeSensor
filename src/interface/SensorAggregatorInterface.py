"""
OWL PLATFORM @ RUTGERS WINLAB
PYTHON LIBRARY : FAKESENSOR
AUTHOR : AJINKYA PADWAD

MAIN REFERENCE : https://git.owlplatform.com/wiki/index.php/Category:GRAIL_RTLS_v3_Documentation

GRAIL FAKE SENSOR
"""
import socket
import messages.SampleMessage
import messages.HandshakeMessage
from termcolor import colored
import time


host = 'localhost'
port = 7007

MessageBuffer = 50

def GetHost():
	return host
def GetPort():
	return port

def SetHost(newhost):
	host = newhost	
def SetPort(newport):
	host = newport	

def IsConnected():
	try:
		global NewSocket
		NewSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 	# ( IPv4, socket constant )
		NewSocket.connect((host, port))	# attach socket to remote address
		print "		Host:",host
		print "		Port:",port
		return True
	except:
		print " Connection Error !\n"
		return False

def SendHandshake(DataPacket):

	print colored('	Sending handkshake message..', 'cyan')
	time.sleep(1)

	Received = NewSocket.recv(MessageBuffer)
	print "Received:",Received

	NewSocket.sendall(DataPacket)
	print 'Sent    :',DataPacket

	print colored('\n\n 	Handshake complete.','green')

def SendSensorData(DataPacket):
		i=1
		while 1:
			NewSocket.sendall(DataPacket)
			print 'SENT: Sample -', i

			i=i+1
			time.sleep(1)
