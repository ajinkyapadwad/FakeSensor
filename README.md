OWL PLATFORM @ RUTGERS WINLAB
PYTHON LIBRARY : SENSOR
AUTHOR : AJINKYA PADWAD
SPRING 2017

SOURCE: https://git.owlplatform.com/wiki/index.php/Category:GRAIL_RTLS_v3_Documentation

GRAIL FAKE SENSOR


Python alternative library for the existing Java Fakesensor. 

=================================================================

DEPENDENCIES :
..python libraries : struct, binascii, time, sys, termcolor, socket
..SampleMessage.py  :  wraps the sensor data into packet
..HandshakeMessage.py : wraps the standard sensor-aggregator handshake protocol
..SensorAggregatorInterface : connects to the aggregator and sends samples

-----------------------------------------------------------------

File / package heirarchy :

python-owl-sensor /
	src /
		interface /
			SensorAggregatorInterface.py
		messages /
			HandshakeMessage.py
			SampleMessage.py	
		fakesensor.py

-----------------------------------------------------------------

Library position :
	Client side : Fakesensor
	Server side : Aggregator

-----------------------------------------------------------------

Running the python library :

1. Run the Aggregator :

	sudo /etc/init.d/owl-aggregator start ( or stop )

	java -jar ./aggregator/target/aggregator-3.0.4-SNAPSHOT-jar-with-dependencies.jar 
	
Sample successful terminal output :

[2017-05-05 18:21:05,208] INFO  main/Aggregator - GRAIL Aggregator is listening for sensors on on port 7007.
[2017-05-05 18:21:05,208] INFO  main/Aggregator - GRAIL Aggregator is listening for solvers on on port 7008.
[2017-05-05 18:21:15,192] INFO  Timer-0/Aggregator - Processed 0 samples since last report.
Statistics
	Avg. Process Time: NaN ms
	Avg. Sample Lifetime: NaN ms

2. New terminal - run the Fakesensor client
	
	python fakesensor.py <hostname> <port-number>

	Default :	python fakesensor.py localhost 7007

	On successful run, the fakesensor continually sends samples at interval of 1 second.

-----------------------------------------------------------------





		
	

