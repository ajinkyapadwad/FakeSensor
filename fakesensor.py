"""
OWL PLATFORM @ RUTGERS WINLAB
PYTHON LIBRARY : FAKESENSOR
AUTHOR : AJINKYA PADWAD

MAIN REFERENCE : https://git.owlplatform.com/wiki/index.php/Category:GRAIL_RTLS_v3_Documentation

GRAIL FAKE SENSOR
"""

# -------------------- DEPENDENCIES -----------------------------
import socket	
import struct
import binascii
import time
import sys
from termcolor import colored

import com.owlplatform.common.SampleMessage

# ------------------- CONNECTION SETUP --------------------------


BadExit = False

def main(host,port):

	# handshake message values
	StringLength = 21
	ProtocolMessage = 'GRAIL sensor protocol'
	Version = 0
	ReservedBits = 0

	
	# # sample sensor data values 
	# MessageLength = 0x2f 
	# PhysicalLayer = 1 
	# # DeviceID = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
	# # ReceiverID =[16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
	# DeviceID = '\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15\x16'
	# ReceptionTime =  int(round(time.time()*1000))
	# RSSI = -50.0
	# SensorData1 = 0xab
	# SensorData2 = 0xba
	
	MessageBuffer = 50


	try :
		# create new socket for TCP / IP connection
		print colored("\n	Connecting to the Aggregator server ...", 'green')
		time.sleep(1)

		
		NewSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 	# ( IPv4, socket constant )
		NewSocket.connect((host, port))	# attach socket to remote address

		

		print colored("	Connection Successful !", 'green')


	 # ------------------ HANDSHAKE -------------------------------------
		
	 	HandshakeMessage = (StringLength, ProtocolMessage, Version, ReservedBits)

		print colored('	Handshake initiated ...\n', 'green')
		time.sleep(1)
		

		Packer = struct.Struct('!'+'I 21s b b')				# declare a new struct object
		DataPacket = Packer.pack(*HandshakeMessage)	

		
		print colored('	Sending handkshake message..', 'cyan')
		time.sleep(1)

		Received = NewSocket.recv(MessageBuffer)
		print "Received:",Received

		NewSocket.sendall(DataPacket)
		print 'Sent    :',DataPacket

		print colored('\n\n 	Handshake complete.','green')

	 # ------------------ SENDING SAMPLES -------------------------------

		print colored('\n 	Now sending sensor data...', 'blue')
		time.sleep(1)
		

		SensorData = ( MessageLength, PhysicalLayer,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16 , 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, ReceptionTime, RSSI , SensorData1, SensorData2 )
		Packer = struct.Struct('!'+'i B 16B 16B Q f B B')

		DataPacket = Packer.pack(*SensorData)

		i=1
		while 1:
			NewSocket.sendall(DataPacket)
			print 'SENT: Sample -', i
			#print '	[',binascii.hexlify(*DeviceID),':', binascii.hexlify(*ReceiverID),' ] @', RSSI, ':- ', ReceptionTime
			i=i+1
			time.sleep(1)

			
	except Exception as Err:
		ErrorText = colored('\n\n 	One or more errors have occurred !\n', 'red')
		print(ErrorText)
		print "ERROR:", Err
		print " 	socket disconnected\n"
		#NewSocket.close()
		BadExit = True
		#sys.exit(0)



if __name__ == '__main__':
	try:
		# take command line arguments :
		host = sys.argv[1]
		port = int(sys.argv[2]) 

		if len(sys.argv) is 3:
			print "		Host:" , host
			print "		Port:" , port
			main(host,port)	

	except:
		if BadExit is False:
			print colored("	Please input appropriate host name and port number.\n",'red') 	
			print colored("	Syntax: python <filename.py>  <hostname>  <portnumber>", 'yellow')
			print colored("\n\n Try Default : \n 	Hostname - localhost \n 	port - 7007 ", 'blue')
			sys.exit()
		else :
			sys.exit()
	



# ----------------- END --------------------------------------------------------------------------

