"""
OWL PLATFORM @ RUTGERS WINLAB
PYTHON LIBRARY : COMMON
AUTHOR : AJINKYA PADWAD

MAIN REFERENCE : https://git.owlplatform.com/wiki/index.php/Category:GRAIL_RTLS_v3_Documentation

GRAIL FAKE SENSOR
"""
from termcolor import colored
import struct
import socket


# handshake message values
StringLength = 21
ProtocolMessage = 'GRAIL sensor protocol'
Version = 0
ReservedBits = 0

def StartHandshake():
	import interface.SensorAggregatorInterface as interface 
	
	HandshakeMessage = (StringLength, ProtocolMessage, Version, ReservedBits)
	Packer = struct.Struct('!'+'I 21s b b')				# declare a new struct object
	DataPacket = Packer.pack(*HandshakeMessage)	

	interface.SendHandshake(DataPacket)