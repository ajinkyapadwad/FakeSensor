
#import java.util.Arrays;

#import com.owlplatform.common.util.NumericUtils;
import time

class SampleMessage :

  DEVICE_ID_SIZE = 16
  
  MESSAGE_TYPE = 6
  
  PHYSICAL_LAYER_UNDEFINED = 0xFF # convert to byte.
  
  PHYSICAL_LAYER_ALL = 0

  PHYSICAL_LAYER_PIPSQUEAK = 1

  PHYSICAL_LAYER_WIFI = 2

  PHYSICAL_LAYER_WINS = 3

  physicalLayer = PHYSICAL_LAYER_UNDEFINED

  def getPhysicalLayer() :
  	return self.physicalLayer

  def setPhysicalLayer(physicalLayer):
    try:
      physicalLayer == PHYSICAL_LAYER_ALL
    except: IllegalArgumentException("Invalid physical layer type. " + PHYSICAL_LAYER_ALL + " is reserved for filtering only.")
    self.physicalLayer = physicalLayer    
 
  def SampleMessage() :
    self.creationTimestamp = time.clock() / 1000

  def SampleMessage(timestamp) :
    self.creationTimestamp = timestamp

  def getLengthPrefixSensor() :
    # physicalLayer, devId, recvId, timestamp, rssi
    length = 1 + DEVICE_ID_SIZE * 2 + 8 + 4
    if self.sensedData is not none :
      length += len(self.sensedData)
    return length

  def getLengthPrefixSolver() :
    # physicalLayer, messageId, devId, recvId, timestamp, rssi
    length = 2 + DEVICE_ID_SIZE * 2 + 8 + 4;
    if self.sensedData is not none :
      length += this.sensedData.length    
    return length

  def getDeviceId() :
    return self.deviceId

  def setDeviceId(deviceId) :
    try : deviceId is none
    except : RuntimeException("Device ID cannot be null.")
    try : deviceId.length is not DEVICE_ID_SIZE
    except : RuntimeException("Device ID must be" + int(DEVICE_ID_SIZE)+ " bytes long.")
    self.deviceId = deviceId

  def getReceiverId() :
    return self.receiverId

  def setReceiverId(receiverId) :
    try : receiverId is none
    except : RuntimeException("Receiver ID cannot be null.")	
    try : receiverId.length != DEVICE_ID_SIZE
    except : RuntimeException("Receiver ID must be "+int(DEVICE_ID_SIZE)+" bytes long.")
    self.receiverId = receiverId;

  def getReceiverTimeStamp() :
    return self.receiverTimeStamp

  def setReceiverTimeStamp(receiverTimeStamp) :
    self.receiverTimeStamp = receiverTimeStamp

  def getRssi() :
    return self.rssi

  def setRssi(rssi) :
    self.rssi = rssi

  def getSensedData() :
    return self.sensedData

  def setSensedData(sensedData) :
    self.sensedData = sensedData

    
    	#-----------------------------------------
    	public String toString() 
      {
    	StringBuffer sb = new StringBuffer()
    	sb.append("Sample (").append(this.getPhysicalLayer())
    	sb.append(", ")
    	sb.append(NumericUtils.toHexString(this.getDeviceId()))
    	sb.append(", ")
    	sb.append(NumericUtils.toHexString(this.getReceiverId()))
    	sb.append("): ")
    	sb.append(this.getRssi())
    	sb.append(" @ ")
    	sb.append(this.getReceiverTimeStamp())
    	if (this.getSensedData() != null) 
    	{
    		sb.append(" [").append(NumericUtils.toHexString(this.getSensedData()));
    		sb.append(']')
    	}		
    	return sb.toString()
    	}
    	#-----------------------------------------
    """
  def getCreationTimestamp() :
    return self.creationTimestamp

  def getTestMessage() : 
    message = SampleMessage()
    a =[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ]
    message.setDeviceId(a)
    message.setReceiverId(a) # needs new instance of a[] ?
    message.setPhysicalLayer(byte(1)) # byte of ...
    message.setRssi(float(-50))
    message.setSensedData(0, 0) # passs arrray of byte as argument ...
    return message
"""
  def clone() throws CloneNotSupportedException 
   {
   		SampleMessage clone = (SampleMessage) super.clone()
   		if (this.sensedData != null) 
   		{ 
   			clone.setSensedData(Arrays.copyOf(this.sensedData, this.sensedData.length))
   		}
   		return clone
   }
"""
