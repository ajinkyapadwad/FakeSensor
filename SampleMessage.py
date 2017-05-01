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
import SensorAggregatorInterface as interface
import time

# default values

MessageLength = 0x2f 
PhysicalLayer = 1 
DeviceID = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
ReceiverID =[16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
ReceptionTime =  int(round(time.time()*1000))
RSSI = -50.0
SensorData1 = 0xab
SensorData2 = 0xba

def GetPhysicalLayer():
	return PhysicalLayer

def SetPhysicalLayer(phylayer):
	try:
		PhysicalLayer=phylayer
	except:
		print " Error at setting Physical Layer."

def SetRSSI(rssi):
	try:
		RSSI=rssi
	except:
		print " Error at setting RSSI."


def SetDeviceID(dev):
	try:
		DeviceID=dev
	except:
		print " Error at setting Device ID."

def SetReceiverID(rec):
	try:
		ReceiverID=rec
	except:
		print " Error at setting Receiver ID."

def SetSensorData(data1,data2):
	try:
		SensorData1=data1
		SensorData2=data2
	except:
		print " Error at setting Sensor Data."

def CreateSensorData():

	SensorData = ( MessageLength, PhysicalLayer,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16 , 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, ReceptionTime, RSSI , SensorData1, SensorData2 )
	Packer = struct.Struct('!'+'i B 16B 16B Q f B B')
	DataPacket = Packer.pack(*SensorData)
	interface.SendSensorData(DataPacket)

