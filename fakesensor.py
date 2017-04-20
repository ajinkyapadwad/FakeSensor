"""
OWL PLATFORM @ RUTGERS WINLAB
PYTHON LIBRARY : FAKESENSOR
"""

# -------------------- DEPENDENCIES -----------------------------
import socket	
import struct
import binascii
import time
import array
import sys
from termcolor import colored

# ------------------- CONNECTION SETUP --------------------------
def main(host,port):

	# sample data values 
	message_length = 0x2f 
	physical_layer = 1 
	timestamp =  int(round(time.time()*1000))
	RSSI = -50.0
	sensor_data1 = 0xab
	sensor_data2 = 0xba
	
	try :
		# create new socket for TCP / IP connection
		print colored("\n	connecting to the Aggregator server ...", 'green')
		time.sleep(1)

		
		NewSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 	# ( IPv4, socket constant )
		NewSocket.connect((host, port))	# attach socket to remote address

		

		print colored("	Connection Successful !", 'green')


	 # ------------------ HANDSHAKE -------------------------------------
		print colored('	Handshake initiated ...\n', 'green')
		time.sleep(1)
		handshake = (21,'GRAIL sensor protocol', 0, 0)

		packer = struct.Struct('!'+'I 21s b b')				# declare a new struct object
		packed_data = packer.pack(*handshake)	

		#time.sleep(1)

		print colored('	Sending Handkshake Message..', 'cyan')

		data = NewSocket.recv(36)
		print "Received:",data

		NewSocket.sendall(packed_data)
		print 'Sent    :',packed_data

		print colored('\n\n 	Handshake Complete.','green')

	 # ------------------ SENDING SAMPLES -------------------------------

		print colored('\n 	Now sending sample sensor data...', 'blue')
		time.sleep(1)
		

		SensorData = ( message_length, physical_layer, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16 ,16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, timestamp, RSSI , sensor_data1, sensor_data2 )
		packer = struct.Struct('!'+'i B 16B 16B Q f 2B')

		packed_data = packer.pack(*SensorData)

		i=1
		while 1:
			NewSocket.sendall(packed_data)
			print 'SENT: Sample -', i
			i=i+1
			time.sleep(1)

			# NewSocket.close()
			# sys.exit()

	except:
		ErrorText = colored('\n\n 	One or more errors have occurred !\n', 'red')
		print(ErrorText)
		print " 	socket disconnected\n"
		#NewSocket.close()
		sys.exit(0)



if __name__ == '__main__':
	try:
		# take command line arguments :
		host = sys.argv[1]
		port = int(sys.argv[2]) 
	
		if message_length(sys.argv) is 3:
			print "		Host:" , host
			print "		Port:" , port
			main(host,port)	

	except:
		print colored("	Please input appropriate host name and port number.\n",'red') 	
		print colored("	Syntax: python <filename.py>  <hostname>  <portnumber>", 'yellow')
		print colored("\n\n Try Default : \n 	Hostname - localhost \n 	port - 7007 ", 'blue')
		sys.exit()
	



# ----------------- END --------------------------------------------------------------------------

