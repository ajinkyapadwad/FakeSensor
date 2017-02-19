
import time

class SampleMessage :

  DEVICE_ID_SIZE = 16
  
  MESSAGE_TYPE = 6
  
  PHYSICAL_LAYER_UNDEFINED = bytes(0xFF) # convert to byte.
  
  PHYSICAL_LAYER_ALL = 0

  PHYSICAL_LAYER_PIPSQUEAK = 1

  PHYSICAL_LAYER_WIFI = 2

  PHYSICAL_LAYER_WINS = 3

  physicalLayer = PHYSICAL_LAYER_UNDEFINED

  def getPhysicalLayer() :
  	return self.physicalLayer

  def setPhysicalLayer(physicalLayer):
    if physicalLayer == PHYSICAL_LAYER_ALL :
      raise ValueError("Invalid physical layer type. " + PHYSICAL_LAYER_ALL + " is reserved for filtering only.")
    self.physicalLayer = physicalLayer    
 
  def SampleMessage() :
    self.creationTimestamp = time.clock() / 1000

  def SampleMessage(timestamp) :
    self.creationTimestamp = timestamp

  def getLengthPrefixSensor() :
    # physicalLayer, devId, recvId, timestamp, rssi
    length = 1 + DEVICE_ID_SIZE * 2 + 8 + 4
    if self.sensedData is not None :
      length += len(self.sensedData)
    return length

  def getLengthPrefixSolver() :
    # physicalLayer, messageId, devId, recvId, timestamp, rssi
    length = 2 + DEVICE_ID_SIZE * 2 + 8 + 4;
    if self.sensedData is not None :
      length += this.sensedData.length    
    return length

    #deviceId = bytes()

  def getDeviceId() :
    return self.deviceId

  def setDeviceId(deviceId) :
    try : deviceId is None
    except : RuntimeError("Device ID cannot be null.")
    try : deviceId.length is not DEVICE_ID_SIZE
    except : RuntimeError("Device ID must be" + int(DEVICE_ID_SIZE)+ " bytes long.")
    self.deviceId = deviceId

  def getReceiverId() :
    return self.receiverId

  def setReceiverId(receiverId) :
    try : receiverId is None
    except : RuntimeError("Receiver ID cannot be null.")	
    try : receiverId.length != DEVICE_ID_SIZE
    except : RuntimeError("Receiver ID must be "+int(DEVICE_ID_SIZE)+" bytes long.")
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

  # This one here --
  def _str_():
    strlist = []
    strlist.append('Sample' + self.getPhysicalLayer()+", "+chr(self.getDeviceId())+", "+chr(self.getReceiverId())+"): "+self.getRssi()+" @ "+self.getReceiverTimeStamp())
    if self.getSensedData() is not None :
   		strlist.append(" ["+chr(self.getSensedData())+']')		
    out_str = ''.join(str_list)
    return out_str
  #-----------------------------------------------------------
  def getCreationTimestamp() :
    return self.creationTimestamp

  def getTestMessage() : 
    message = SampleMessage()
    a = bytes([ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ])
    message.setDeviceId(a)
    message.setReceiverId(a) # needs new instance of a[] ?
    message.setPhysicalLayer(bytes(1)) # byte of ...
    message.setRssi(float(-50))
    message.setSensedData(bytes([0, 0])) # passs arrray of byte as argument ...
    return message
