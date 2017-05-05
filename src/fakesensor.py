"""
OWL PLATFORM @ RUTGERS WINLAB
PYTHON LIBRARY : FAKESENSOR
AUTHOR : AJINKYA PADWAD

MAIN REFERENCE : https://git.owlplatform.com/wiki/index.php/Category:GRAIL_RTLS_v3_Documentation

GRAIL FAKE SENSOR
"""

	
import struct
import binascii
import time
import sys
from termcolor import colored

import messages.SampleMessage as msg
import messages.HandshakeMessage as handshake
import interface.SensorAggregatorInterface as interface

BadExit = False

def main(host,port):

	try :
		interface.SetHost(host)
		interface.SetPort(port)

		print colored("\n	Connecting to the Aggregator server ...", 'green')
		time.sleep(1)
		
		if interface.IsConnected():
			print colored("	Connection Successful !", 'green')
			time.sleep(1)

			print colored('	Handshake initiated ...\n', 'green')
			time.sleep(1)	

			handshake.StartHandshake()

			# sample sensor data values 
			PhysicalLayer = 1 
			DeviceID = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
			ReceiverID =[16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
			RSSI = -50.0
			SensorData1 = 0xab
			SensorData2 = 0xba
			
			msg.SetPhysicalLayer(PhysicalLayer)
			msg.SetRSSI(RSSI)
			msg.SetDeviceID(DeviceID)
			msg.SetReceiverID(ReceiverID)
			msg.SetSensorData(SensorData1,SensorData2)

			print colored('\n 	Now sending sensor data...', 'blue')
			time.sleep(1)
		
			msg.PackData()

			interface.SendSamples()
		
	except Exception as Err:
		ErrorText = colored('\n\n 	One or more errors have occurred !\n', 'red')
		print(ErrorText)
		print "ERROR:", Err
		print " 	socket disconnected\n"
		BadExit = True

if __name__ == '__main__':
	try:
		# take command line arguments :
		host = sys.argv[1]
		port = int(sys.argv[2]) 
		main(host,port)	

	except:
		if BadExit is False:
			print colored("	Please input appropriate host name and port number.\n",'red') 	
			print colored("	Syntax: python <filename.py>  <hostname>  <portnumber>", 'yellow')
			print colored("\n\n Try Default : \n 	Hostname - localhost \n 	port - 7007 ", 'blue')
			sys.exit()
		else :
			sys.exit()
	


