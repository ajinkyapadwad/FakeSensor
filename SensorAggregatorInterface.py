"""
import java.net.InetSocketAddress
import java.util.concurrent.ConcurrentLinkedQueue

import org.apache.mina.core.RuntimeIoException
import org.apache.mina.core.future.ConnectFuture
import org.apache.mina.core.session.IdleStatus
import org.apache.mina.core.session.IoSession
import org.apache.mina.filter.codec.ProtocolCodecFilter
import org.apache.mina.filter.executor.ExecutorFilter
import org.apache.mina.transport.socket.SocketConnector
import org.apache.mina.transport.socket.nio.NioSocketConnector

import org.slf4j.Logger
import org.slf4j.LoggerFactory
"""
import sys

import logging 

import SampleMessage
import ConnectionListener
import AggregatorSensorProtocolCodecFactory
import HandshakeMessage


class SensorAggregatorInterface :

  class AdapterHandler(SensorIoAdapter):
 
    parent = SensorAggregatorInterface()

    def AdapterHandler(parent) :  
      try : parent is None 
      except : IllegalArgumentException("SensorAggregatorInterface cannot be None")    
      self.parent = parent
    # check arguments - --------------------------  
    def exceptionCaught(IoSession session, Throwable cause) 
      self.parent.exceptionCaught(session, cause)
    
    def sensorConnected(IoSession session) 
      self.parent.sensorConnected(session)

    def sensorDisconnected(IoSession session) 
      self.parent.sensorDisconnected(session)

    def handshakeMessageReceived(IoSession session,HandshakeMessage handshakeMessage)
      self.parent.handshakeMessageReceived(session, handshakeMessage)    

    def handshakeMessageSent(IoSession session, HandshakeMessage handshakeMessage) 
      self.parent.handshakeMessageSent(session, handshakeMessage)

    def sensorSampleReceived(IoSession session, SampleMessage sampleMessage) 
      self.parent.sensorSampleReceived(session, sampleMessage)
    
    def sensorSampleSent(IoSession session, SampleMessage sampleMessage)
      self.parent.sensorSampleSent(session, sampleMessage)

    def sessionIdle(IoSession session, IdleStatus idleStatus) 
      self.parent.sessionIdle(session, idleStatus)
      
  # Logger ?
  Logger log = LoggerFactory .getLogger(SensorAggregatorInterface.class)

  handler = AdapterHandler(self)

  sentHandshake = HandshakeMessage()

  receivedHandshake = HandshakeMessage()
  
  session = IoSession() 

  connector =  SocketConnector() 
  
  canSendSamples = False

  connectionRetryDelay = 10000

  stayConnected = False

  disconnectOnException = True

  port = 7007

  ioHandler = SensorIoHandler(self.handler)
  
  # This one - 
  private ConcurrentLinkedQueue<ConnectionListener> connectionListeners = new ConcurrentLinkedQueue<ConnectionListener>()

  executors = ExecutorFilter() 
  
  maxOutstandingSamples = sys.maxint

  connectionTimeout = 1000l

  def setConnector() :
    # check logging error
    if self.host is None : 
      logging.error("No host value set, cannot set up socket connector.")
      return False
    if (self.port < 0 || self.port > 65535) :
      logging.error("Port value is invalid .", Integer.valueOf(self.port))
      return False

    if (self.connector is not None) :
      boolean tmp = self.stayConnected
      self.stayConnected = False
      self._disconnect()
      self.stayConnected = tmp

    self.executors =  ExecutorFilter(1)

    self.connector = NioSocketConnector()
    #--------------------------
    self.connector.getSessionConfig().setTcpNoDelay(True)
    if (not self.connector.getFilterChain().contains(AggregatorSensorProtocolCodecFactory.CODEC_NAME)) 
    
      self.connector.getFilterChain().addLast(AggregatorSensorProtocolCodecFactory.CODEC_NAME,
          new ProtocolCodecFilter(new AggregatorSensorProtocolCodecFactory(
              False)))
    
    self.connector.getFilterChain().addLast("ExecutorPool", self.executors)

    self.connector.setHandler(self.ioHandler)
    logging.debug("Connector set up successfully.")
    return True
    #----------------------

  def connect(maxWait) 
    timeout = maxWait
    if (timeout <= 0) :
      timeout = self.connectionTimeout
    
    if (self.connector is None) : 
      if (not self.setConnector()) 
        logging.error("Unable to set up connection to the aggregator.")
        return False
      
    if (self.session is not None ) :
      logging.error("Already connectednot ")
      return False

    waitTime = timeout
    #----------------------------------   
    click = 1 # replicates do-while looping 
    while (click is 1 or (self.stayConnected && waitTime > 0)):
      startAttempt = System.currentTimeMillis()
      self.connector.setConnectTimeoutMillis(waitTime - 5)
      if (self._connect(waitTime)) 
        logging.debug("Connection succeedednot ")
        return True
      
      if (self.stayConnected) :
        retryDelay = self.connectionRetryDelay
        if (timeout < self.connectionRetryDelay * 2) :
          retryDelay = timeout / 2
          if (retryDelay < 500) :
            retryDelay = 500
          
        
        try :
          logging.warn(String.format("Connection to %s:%d failed, waiting %dms before retrying.", self.host, int(self.port), long(retryDelay)))
          Thread.sleep(retryDelay)
        except : InterruptedException ie 

        waitTime = waitTime - (System.currentTimeMillis() - startAttempt)
      click=2  
    
    #----------------------------------------
    self._disconnect()
    self.finishConnection()

    return False

  def doConnectionSetup() :
    return self.connect(0)

  def doConnectionTearDown() :
    self.disconnect()
  
  def disconnect() :
    self.stayConnected = False
    self._disconnect()

  def _connect(timeout) 
    ConnectFuture connFuture = self.connector.connect(new InetSocketAddress(self.host, self.port))
    if (timeout > 0) :
      if (not connFuture.awaitUninterruptibly(timeout)) :
        return False    
    else 
      connFuture.awaitUninterruptibly()

    if (not connFuture.isConnected()) 
      return False

    try :
      logging.info("Connecting to :.", self.host, Integer.valueOf(self.port))
      self.session = connFuture.getSession()
    except : 
      (RuntimeIoException ioe) 
      logging.error(String.format("Could not create session to aggregator %s:%d.", self.host, Integer.valueOf(self.port)), ioe)
      return False   
    return True
  
  def _disconnect() 
    #this --
    IoSession currentSession = self.session
    if (currentSession is not None) :
      if (not currentSession.isClosing()) :
        logging.info("Closing connection to aggregator at .",currentSession.getRemoteAddress())
        currentSession.close(True)

      self.session = None
      self.sentHandshake = None
      self.receivedHandshake = None
      self.canSendSamples = False
      for (ConnectionListener listener : self.connectionListeners) 
        listener.connectionInterrupted(self)
    
  listener = ConnectionListener()
  def addConnectionListener( listener) 
    if (not self.connectionListeners.contains(listener)) :
      self.connectionListeners.add(listener)
    
  
  def removeConnectionListener( listener) :
    if (listener is None) :
      self.connectionListeners.remove(listener)
  
  #session = IoSession()
  #handshakeMessage = HandshakeMessage()
  
  def handshakeMessageReceived( session , handshakeMessage) 
    logging.debug("Received ", handshakeMessage)
    self.receivedHandshake = handshakeMessage
    handshakeCheck = self.checkHandshake()
    if (handshakeCheck is None): 
      return
    
    if (handshakeCheck):
      self.canSendSamples = True
      for (listener : self.connectionListeners) 
        listener.readyForSamples(self)
      
    else if (not handshakeCheck):
      logging.warn("Handshakes did not match.")
      self._disconnect()
 
  def handshakeMessageSent( session, handshakeMessage) 
    logging.debug("Sent ", handshakeMessage)
    self.sentHandshake = handshakeMessage
    handshakeCheck = self.checkHandshake()
    if (handshakeCheck is None): 
      return
    if (handshakeCheck):
      self.canSendSamples = True
      for (ConnectionListener listener : self.connectionListeners) 
        listener.readyForSamples(self)
      
    else if (Boolean.False.equals(handshakeCheck)) 
      logging.warn("Handshakes did not match.")
      self._disconnect()
  
  protected Boolean checkHandshake() 
    if (self.sentHandshake is None) 
      logging.debug("Sent handshake is None, not checking.")
      return None
    
    if (self.receivedHandshake == None) 
      logging.debug("Received handshake is None, not checking.")
      return None
    

    if (not self.sentHandshake.equals(self.receivedHandshake)) 
      logging.error("Handshakes do not match.  Closing connection to distributor at .", self.session.getRemoteAddress())
      prevValue = self.stayConnected
      self.stayConnected = False
      self._disconnect()
      self.stayConnected = prevValue
      return False
    
    return True
  
  def sensorSampleReceived( session, sampleMessage) :
    logging.error("Protocol error: Received sample message from the aggregator:\n", sampleMessage)
    self._disconnect()

  def sensorConnected(session) :
    if (self.session == None) 
      self.session = session
    
    logging.info("Connected to .", session.getRemoteAddress())

    for ( listener : self.connectionListeners) 
      listener.connectionEstablished(self)
    

    logging.debug("Attempting to write handshake.")
    self.session.write(HandshakeMessage.getDefaultMessage())
  

  def  sensorDisconnected( session) 
    self._disconnect()
    while (self.stayConnected) 
      logging.info("Reconnecting to aggregator at :", self.host,
          Integer.valueOf(self.port))

      try 
        Thread.sleep(self.connectionRetryDelay)
       catch (InterruptedException ie) 

      if (self.connect(self.connectionTimeout)) 
        return  

    self.finishConnection()

  
  def finishConnection() :
    self.connector.dispose()
    self.connector = None
    for (ConnectionListener listener : self.connectionListeners) 
      listener.connectionEnded(self)
    
    if (self.executors not = None) :
      self.executors.destroy()
    
  idleStatus = IdleStatus()
  def sessionIdle( session,  idleStatus) :

  
  def getConnectionRetryDelay() :
    return self.connectionRetryDelay
  
  
  def setConnectionRetryDelay(long connectionRetryDelay) :
    self.connectionRetryDelay = connectionRetryDelay
  
  
  def isStayConnected() :
    return self.stayConnected
  
  
  def setStayConnected(boolean stayConnected) :
    self.stayConnected = stayConnected
  
  
  def isDisconnectOnException() :
    return self.disconnectOnException  
 
  def setDisconnectOnException(boolean disconnectOnException) :
    self.disconnectOnException = disconnectOnException
  
  def getHost() :
    return self.host
  
  def setHost(host) :
    self.host = host
  
  def  getPort() :
    return self.port
   
  def setPort( port) :
    self.port = port
  
  sampleMessage=SampleMessage()
  def sensorSampleSent( session,  sampleMessage) 
    logging.debug("Sent ", sampleMessage)

  def  sendSample( sampleMessage) 
    if (not self.canSendSamples) :
      logging.warn("Cannot send samples.")
      return False
    
    if (self.session.getScheduledWriteMessages() > self.maxOutstandingSamples) :
      logging.warn("Buffer full, cannot send sample.")
      return False
    
    self.session.write(sampleMessage)
    return True
  
  def  exceptionCaught( session, Throwable cause) :
    logging.error("Exception while communicating with " + self + ".", cause)
    if (cause instanceof OutOfMemoryError): 
      sys.exit(1)
    
    if (self.disconnectOnException) :
      self._disconnect()
    
  def  isCanSendSamples() :
    if (not self.canSendSamples or self.session is None) :
      return False
    
    return self.session.getScheduledWriteMessages() < self.maxOutstandingSamples
  
  def  getMaxOutstandingSamples() :
    return self.maxOutstandingSamples
  

  def setMaxOutstandingSamples(maxOutstandingSamples) :
    self.maxOutstandingSamples = maxOutstandingSamples
  
  #public String toString() 
  #  return "Sensor-Aggregator Interface @ " + self.host + ":" + self.port
   print "Sensor-Aggregator Interface @ " + self.host + ":" + self.port
