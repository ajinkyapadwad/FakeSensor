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
try :
	# take command line arguments :
	try: 
		host = sys.argv[1]
		port = sys.argv[2]
	except:
		print colored("	Please input the host / port name.\n 	Syntax: python filename.py hostname port", 'red')
		
	# host = 'localhost'	# IPv4 address, localhost for this program
	# port = 7007			# port number	

	# create new socket for TCP / IP connection
	print "\n	connecting to the Aggregator server ..."
	time.sleep(1)

	NewSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 	# ( IPv4, socket constant )
	NewSocket.connect((argv[1], argv[2]))	# attach socket to remote address

except Exception as ex:
	print ("One or more errors have occurred !\n 	Exception: %s"%(ex))
	NewSocket.close()
	sys.exit()

print "Connection Successful."

print 'Handshake initiated..'


handshake = (21,'GRAIL sensor protocol', 0, 0)

packer = struct.Struct('!'+'I 21s b b')				# declare a new struct object
packed_data = packer.pack(*handshake)	

#time.sleep(1)

print 'Sending Handkshake Message..'

data = s.recv(36)
print "Received:",data

s.sendall(packed_data)
print 'Sent    :',packed_data

print 'Handshake Complete.'

# print"Sleep 10 seconds.."
# time.sleep(10)

# ---------------------------------------------------------------------------------------------------------

print 'Now sending sample sensor data...'

LEN = 0x2f  # 4 byte value  -- I
PHY = 1 # 1 byte value -- b ,
#DEV_ID = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11, 12, 13, 14, 15, 16 ]
#RECV_ID = [ 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1 ]
timestamp1 =  int(round(time.time()*1000))
#timestamp2 = str(timestamp1)
RSSI = -50.0
Data1 = 0xab
Data2 = 0xba

SensorData = ( LEN, PHY, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16 ,16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, timestamp1, RSSI , Data1, Data2 )
packer = struct.Struct('!'+'i B 16B 16B Q f 2B')

# SensorData = (47, 1)
# packer = struct.Struct('!'+'H b')



packed_data = packer.pack(*SensorData)

i=1
while 1:
	s.sendall(packed_data)
	print 'SENT: Sample -', i
	i=i+1
	time.sleep(1)
