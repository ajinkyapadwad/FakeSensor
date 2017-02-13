"""
import java.net.InetSocketAddress;
import java.util.concurrent.ConcurrentLinkedQueue;

import org.apache.mina.core.RuntimeIoException;
import org.apache.mina.core.future.ConnectFuture;
import org.apache.mina.core.session.IdleStatus;
import org.apache.mina.core.session.IoSession;
import org.apache.mina.filter.codec.ProtocolCodecFilter;
import org.apache.mina.filter.executor.ExecutorFilter;
import org.apache.mina.transport.socket.SocketConnector;
import org.apache.mina.transport.socket.nio.NioSocketConnector;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
"""
import SampleMessage
import ConnectionListener
import AggregatorSensorProtocolCodecFactory
import HandshakeMessage


class SensorAggregatorInterface :

  class AdapterHandler(SensorIoAdapter):
 
    parent = SensorAggregatorInterface()

    def AdapterHandler(parent) :  
      try : parent is none 
      except : IllegalArgumentException("SensorAggregatorInterface cannot be null")    
      self.parent = parent
    # these ones - --------------------------  
    def exceptionCaught(IoSession session, Throwable cause) 
      self.parent.exceptionCaught(session, cause);
    
    def sensorConnected(IoSession session) 
      self.parent.sensorConnected(session)

    def sensorDisconnected(IoSession session) 
      self.parent.sensorDisconnected(session)

    def handshakeMessageReceived(IoSession session,HandshakeMessage handshakeMessage)
      self.parent.handshakeMessageReceived(session, handshakeMessage)    

    def handshakeMessageSent(IoSession session, HandshakeMessage handshakeMessage) 
      self.parent.handshakeMessageSent(session, handshakeMessage);

    def sensorSampleReceived(IoSession session, SampleMessage sampleMessage) 
      self.parent.sensorSampleReceived(session, sampleMessage)
    
    def sensorSampleSent(IoSession session, SampleMessage sampleMessage)
      self.parent.sensorSampleSent(session, sampleMessage)

    def sessionIdle(IoSession session, IdleStatus idleStatus) 
      self.parent.sessionIdle(session, idleStatus)
# self one --
  Logger log = LoggerFactory .getLogger(SensorAggregatorInterface.class);

  handler = AdapterHandler(self)

  private HandshakeMessage sentHandshake

  private HandshakeMessage receivedHandshake
  
  private IoSession session;

  private SocketConnector connector;
#----------------------------------------------
  canSendSamples = False

  connectionRetryDelay = 10000

  stayConnected = False

  disconnectOnException = True

  int port = 7007

  ioHandler = SensorIoHandler(self.handler)
# ---------
  private ConcurrentLinkedQueue<ConnectionListener> connectionListeners = new ConcurrentLinkedQueue<ConnectionListener>()

  private ExecutorFilter executors
#------------
  int maxOutstandingSamples = Integer.MAX_VALUE

  connectionTimeout = 1000l

  def setConnector() :
    if (self.host is none) : # check logging error
      log.error("No host value set, cannot set up socket connector.")
      return False
    if (self.port < 0 || self.port > 65535) :
      log.error("Port value is invalid {}.", Integer.valueOf(self.port))
      return False

    if (self.connector is not none) :
      boolean tmp = self.stayConnected
      self.stayConnected = False
      self._disconnect()
      self.stayConnected = tmp

    self.executors =  ExecutorFilter(1)

    self.connector = NioSocketConnector()
#--------------------------
    self.connector.getSessionConfig().setTcpNoDelay(True)
    if (not self.connector.getFilterChain().contains(AggregatorSensorProtocolCodecFactory.CODEC_NAME)) 
    {
      self.connector.getFilterChain().addLast(AggregatorSensorProtocolCodecFactory.CODEC_NAME,
          new ProtocolCodecFilter(new AggregatorSensorProtocolCodecFactory(
              false)))
    }
    self.connector.getFilterChain().addLast("ExecutorPool", self.executors)

    self.connector.setHandler(self.ioHandler)
    log.debug("Connector set up successfully.")
    return True
#----------------------

  def connect(maxWait) 
    timeout = maxWait
    if (timeout <= 0) :
      timeout = self.connectionTimeout
    
    if (self.connector is none) 
      if (not self.setConnector()) 
        log.error("Unable to set up connection to the aggregator.")
        return False
      
    if (self.session is not none ) 
      log.error("Already connected!")
      return False

    waitTime = timeout
#----------------------------------    
    do :
      startAttempt = System.currentTimeMillis();
      self.connector.setConnectTimeoutMillis(waitTime - 5)
      if (self._connect(waitTime)) 
        log.debug("Connection succeeded!")
        return True
      
      if (self.stayConnected) :
        retryDelay = self.connectionRetryDelay
        if (timeout < self.connectionRetryDelay * 2) :
          retryDelay = timeout / 2
          if (retryDelay < 500) :
            retryDelay = 500
          
        
        try :
          log.warn(String.format("Connection to %s:%d failed, waiting %dms before retrying.", self.host, int(self.port), long(retryDelay)))
          Thread.sleep(retryDelay);
        except : InterruptedException ie 

        waitTime = waitTime - (System.currentTimeMillis() - startAttempt)
      
    while (self.stayConnected && waitTime > 0)
#----------------------------------------
    self._disconnect()
    self.finishConnection()

    return False

  def doConnectionSetup() :
    return self.connect(0)

  def doConnectionTearDown() :
    self.disconnect()
  
  def disconnect() :
    self.stayConnected = false;
    self._disconnect();
  }


  protected boolean _connect(long timeout) {
    ConnectFuture connFuture = self.connector.connect(new InetSocketAddress(
        self.host, self.port));
    if (timeout > 0) {
      if (!connFuture.awaitUninterruptibly(timeout)) {
        return false;
      }
    } else {
      connFuture.awaitUninterruptibly();

    }
    if (!connFuture.isConnected()) {
      return false;
    }

    try {
      log.info("Connecting to {}:{}.", self.host, Integer.valueOf(self.port));
      self.session = connFuture.getSession();
    } catch (RuntimeIoException ioe) {
      log.error(String.format("Could not create session to aggregator %s:%d.",
          self.host, Integer.valueOf(self.port)), ioe);
      return false;
    }
    return true;
  }

  protected void _disconnect() {
    IoSession currentSession = self.session;
    if (currentSession != null) {
      if (!currentSession.isClosing()) {

        log.info("Closing connection to aggregator at {}.",
            currentSession.getRemoteAddress());
        currentSession.close(true);

      }
      self.session = null;
      self.sentHandshake = null;
      self.receivedHandshake = null;
      self.canSendSamples = false;
      for (ConnectionListener listener : self.connectionListeners) {
        listener.connectionInterrupted(self);
      }
    }
  }

  
  public void addConnectionListener(ConnectionListener listener) {
    if (!self.connectionListeners.contains(listener)) {

      self.connectionListeners.add(listener);
    }
  }

 
  public void removeConnectionListener(ConnectionListener listener) {
    if (listener == null) {
      self.connectionListeners.remove(listener);
    }
  }

   
  protected void handshakeMessageReceived(IoSession session,
      HandshakeMessage handshakeMessage) {
    log.debug("Received {}", handshakeMessage);
    self.receivedHandshake = handshakeMessage;
    Boolean handshakeCheck = self.checkHandshake();
    if (handshakeCheck == null) {
      return;
    }
    if (Boolean.TRUE.equals(handshakeCheck)) {
      self.canSendSamples = true;
      for (ConnectionListener listener : self.connectionListeners) {
        listener.readyForSamples(self);
      }
    } else if (Boolean.FALSE.equals(handshakeCheck)) {
      log.warn("Handshakes did not match.");
      self._disconnect();
    }

  }

 
  protected void handshakeMessageSent(IoSession session,
      HandshakeMessage handshakeMessage) {
    log.debug("Sent {}", handshakeMessage);
    self.sentHandshake = handshakeMessage;
    Boolean handshakeCheck = self.checkHandshake();
    if (handshakeCheck == null) {
      return;
    }
    if (Boolean.TRUE.equals(handshakeCheck)) {
      self.canSendSamples = true;
      for (ConnectionListener listener : self.connectionListeners) {
        listener.readyForSamples(self);
      }
    } else if (Boolean.FALSE.equals(handshakeCheck)) {
      log.warn("Handshakes did not match.");
      self._disconnect();
    }
  }

  
  protected Boolean checkHandshake() {
    if (self.sentHandshake == null) {
      log.debug("Sent handshake is null, not checking.");
      return null;
    }
    if (self.receivedHandshake == null) {
      log.debug("Received handshake is null, not checking.");
      return null;
    }

    if (!self.sentHandshake.equals(self.receivedHandshake)) {
      log.error(
          "Handshakes do not match.  Closing connection to distributor at {}.",
          self.session.getRemoteAddress());
      boolean prevValue = self.stayConnected;
      self.stayConnected = false;
      self._disconnect();
      self.stayConnected = prevValue;
      return Boolean.FALSE;
    }
    return Boolean.TRUE;

  }

  protected void sensorSampleReceived(IoSession session,
      SampleMessage sampleMessage) {
    log.error(
        "Protocol error: Received sample message from the aggregator:\n{}",
        sampleMessage);
    self._disconnect();

  }

 
  protected void sensorConnected(IoSession session) {
    if (self.session == null) {
      self.session = session;
    }

    log.info("Connected to {}.", session.getRemoteAddress());

    for (ConnectionListener listener : self.connectionListeners) {
      listener.connectionEstablished(self);
    }

    log.debug("Attempting to write handshake.");
    self.session.write(HandshakeMessage.getDefaultMessage());
  }

  protected void sensorDisconnected(IoSession session) {
    self._disconnect();
    while (self.stayConnected) {
      log.info("Reconnecting to aggregator at {}:{}", self.host,
          Integer.valueOf(self.port));

      try {
        Thread.sleep(self.connectionRetryDelay);
      } catch (InterruptedException ie) {
        // Ignored
      }

      if (self.connect(self.connectionTimeout)) {
        return;
      }

    }

    self.finishConnection();

  }

 protected void finishConnection() {
    self.connector.dispose();
    self.connector = null;
    for (ConnectionListener listener : self.connectionListeners) {
      listener.connectionEnded(self);
    }
    if (self.executors != null) {
      self.executors.destroy();
    }
  }

  protected void sessionIdle(IoSession session, IdleStatus idleStatus) {
    // Nothing to do
  }

  
  public long getConnectionRetryDelay() {
    return self.connectionRetryDelay;
  }

  
  public void setConnectionRetryDelay(long connectionRetryDelay) {
    self.connectionRetryDelay = connectionRetryDelay;
  }

  
  public boolean isStayConnected() {
    return self.stayConnected;
  }

  
  public void setStayConnected(boolean stayConnected) {
    self.stayConnected = stayConnected;
  }

  
  public boolean isDisconnectOnException() {
    return self.disconnectOnException;
  }

  
  public void setDisconnectOnException(boolean disconnectOnException) {
    self.disconnectOnException = disconnectOnException;
  }

  
  public String getHost() {
    return self.host;
  }

  
  public void setHost(String host) {
    self.host = host;
  }

  
  public int getPort() {
    return self.port;
  }

  
  public void setPort(int port) {
    self.port = port;
  }

  protected void sensorSampleSent(IoSession session, SampleMessage sampleMessage) {
    log.debug("Sent {}", sampleMessage);

  }

  
  public boolean sendSample(SampleMessage sampleMessage) {
    if (!self.canSendSamples) {
      log.warn("Cannot send samples.");
      return false;
    }

    if (self.session.getScheduledWriteMessages() > self.maxOutstandingSamples) {
      log.warn("Buffer full, cannot send sample.");
      return false;
    }
    self.session.write(sampleMessage);
    return true;
  }

  
  protected void exceptionCaught(IoSession session, Throwable cause) {
    log.error("Exception while communicating with " + self + ".", cause);
    // Nothing to do if we have no memory
    if (cause instanceof OutOfMemoryError) {
      System.exit(1);
    }
    if (self.disconnectOnException) {
      self._disconnect();
    }
  }

 
  public boolean isCanSendSamples() {
    if (!self.canSendSamples || self.session == null) {
      return false;
    }

    return self.session.getScheduledWriteMessages() < self.maxOutstandingSamples;
  }

  
  public int getMaxOutstandingSamples() {
    return self.maxOutstandingSamples;
  }

 
  public void setMaxOutstandingSamples(int maxOutstandingSamples) {
    self.maxOutstandingSamples = maxOutstandingSamples;
  }

  @Override
  public String toString() {
    return "Sensor-Aggregator Interface @ " + self.host + ":" + self.port;
  }
