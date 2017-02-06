
import java.util.Arrays;

import com.owlplatform.common.util.NumericUtils;


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
  		return this.physicalLayer

  	def setPhysicalLayer( physicalLayer):
  		try:
  			physicalLayer == PHYSICAL_LAYER_ALL
  		except: IllegalArgumentException("Invalid physical layer type. " + PHYSICAL_LAYER_ALL + " is reserved for filtering only.")
  		this.physicalLayer = physicalLayer
    # variables -----------------
    private byte[] deviceId

    private byte[] receiverId

    private long receiverTimeStamp

    private float rssi

    private final long creationTimestamp

    private byte[] sensedData = null

    def SampleMessage() :
    	this.creationTimestamp = System.currentTimeMillis()


    def SampleMessage(final long timestamp) :
    	this.creationTimestamp = timestamp

    def getLengthPrefixSensor() :
    # physicalLayer, devId, recvId, timestamp, rssi
    length = 1 + DEVICE_ID_SIZE * 2 + 8 + 4
    if (this.sensedData != null) :
    	{
    	length += this.sensedData.length;
    	}
    	return length

    def getLengthPrefixSolver() :
    # physicalLayer, messageId, devId, recvId, timestamp, rssi
    	length = 2 + DEVICE_ID_SIZE * 2 + 8 + 4;
    	if (this.sensedData != null) :
    	length += this.sensedData.length    
    	return length

    def getDeviceId() :
    	return this.deviceId

	def setDeviceId(byte[] deviceId) :
    	try : deviceId == null
    	except : RuntimeException("Device ID cannot be null.")

    	try : deviceId.length != DEVICE_ID_SIZE
    	except : RuntimeException(String.format("Device ID must be" + Integer.valueOf(DEVICE_ID_SIZE)+ " bytes long.")
    	
    	this.deviceId = deviceId

    def getReceiverId() :
    	return this.receiverId


	def setReceiverId(byte[] receiverId) :
    	try : receiverId == null
    	except : RuntimeException("Receiver ID cannot be null.")
    			
    	try : receiverId.length != DEVICE_ID_SIZE
    	except : RuntimeException(String.format("Receiver ID must be "+Integer.valueOf(DEVICE_ID_SIZE)+" bytes long.")
    	
    	this.receiverId = receiverId;
    	

    def getReceiverTimeStamp() :
      	return this.receiverTimeStamp
    
    def setReceiverTimeStamp(long receiverTimeStamp) :
    	this.receiverTimeStamp = receiverTimeStamp
      	
    def getRssi() :
    	return this.rssi
    	 
    def setRssi(float rssi) :
    	this.rssi = rssi
    	
    def getSensedData() :
    	return this.sensedData
    	
	def setSensedData(byte[] sensedData) :
    	this.sensedData = sensedData;
    	

    	#-----------------------------------------
    	public String toString() {
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

  	def getCreationTimestamp() :
   		return this.creationTimestamp
   

   	def getTestMessage() 
   		message = new SampleMessage()
   		a =[ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ]
   		message.setDeviceId(a)
		message.setReceiverId(a) # needs new instance of a[] ?
  		message.setPhysicalLayer((byte) 1)
   		message.setRssi(-50f)
   		message.setSensedData(new byte[] { 0, 0 })
 		return message

   	def clone() throws CloneNotSupportedException 
   {
   		SampleMessage clone = (SampleMessage) super.clone()
   		if (this.sensedData != null) 
   		{ 
   			clone.setSensedData(Arrays.copyOf(this.sensedData, this.sensedData.length))
   		}
   		return clone
   }
