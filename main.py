import argparse
import math

from threading import Thread

import cherrypy

import time
import moment
from datetime import datetime


from OSC import OSCServer
import sys
from time import sleep


if __name__ == "__main__":
	oscServer = oscServer()

	MuseIoAdress = "127.0.0.1"
	MuseIoPort = 5000

	server = OSCServer( (MuseIoAdress, MuseIoPort) )
	server.timeout = 0
	run = True

	# this method of reporting timeouts only works by convention
	# that before calling handle_request() field .timed_out is 
	# set to False
	def handle_timeout(self):
		self.timed_out = True

	# funny python's way to add a method to an instance of a class
	import types
	server.handle_timeout = types.MethodType(handle_timeout, server)
	
	server.addMsgHandler( "/muse/elements/experimental/mellow", self.eeg_calmnessBuffer )
	
	def eeg_calmnessBuffer(self, unused_addr, calmness):
		print(calmness)

	# def eeg_batteryStatusBuffer( self, unused_addr, StateOfCharge, FuelGaugeBatteryVoltage, ADCBatteryVoltage, Temperature ):
		# percentageBattery = round(StateOfCharge/100) 
		# print(percentageBattery)

	# def connCheck( self, unused_addr, args, ch1, ch2, ch3, ch4 ):
		# pass 

	# def eeg_connStatusBuffer( self, unused_addr, int ):
		# print("Connection in bytes per second: "+str(int))
	