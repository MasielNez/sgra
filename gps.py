 #!/usr/bin/env python

import time
import serial
import urllib2
import subprocess

device_id = '1234';
password = 'whatever';

ser = serial.Serial(
	port='/dev/ttyAMA0',
	baudrate = 115200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

while 1:
	subprocess.call("sudo poff fona", shell=True)
	time.sleep(1)
	ser = serial.Serial(
		port='/dev/ttyAMA0',
		baudrate = 115200,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1
	)
	time.sleep(1)
	ser.write('AT+CGNSINF\r')
	counter=0
	x=ser.readline()
	while ('+CGNSINF:' not in x) and (counter < 5):
		x=ser.readline()
		counter+=1
	subprocess.call("sudo pon fona", shell=True)
	time.sleep(3)
	data = x.split(',')
	update = urllib2.urlopen("http://api.dominitec.com/update-gps-info.php?device_id=" + device_id + "&password=" + password + "&latitude=" + data[3] + "&longitude=" + data[4] + "&altitude=" + data[5] + "&utctime=" + data[2] + "&speed=" + data[6] + "&course=" + data[7]).read()
	time.sleep(1)
	print update
	
