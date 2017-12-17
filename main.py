#!/usr/bin/python3
import argparse
import math

import threading

def keypress(): 
    """
    Waits for the user to press a key. Returns the ascii code 
    for the key pressed or zero for a function key pressed.
    """                             
    import msvcrt               
    while 1:
        if msvcrt.kbhit():              # Key pressed?
            a = ord(msvcrt.getch())     # get first byte of keyscan code     
            if a == 0 or a == 224:      # is it a function key?
                msvcrt.getch()          # discard second byte of key scan code
                return 0                # return 0
            else:
                return a                # else return ascii code


def eeg_calmnessBuffer(self, unused_addr, calmness):
	print(calmness)

# def eeg_batteryStatusBuffer( self, unused_addr, StateOfCharge, FuelGaugeBatteryVoltage, ADCBatteryVoltage, Temperature ):
	# percentageBattery = round(StateOfCharge/100) 
	# print(percentageBattery)

# def connCheck( self, unused_addr, args, ch1, ch2, ch3, ch4 ):
	# pass 

# def eeg_connStatusBuffer( self, unused_addr, int ):
	# print("Connection in bytes per second: "+str(int))


	
	
class oscServerThread(threading.Thread):
	def __init__(self, threadID, name, ip, port):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.ip = ip
		self.port = port
		self._stop_event = threading.Event()
	
	def run(self):
		from pythonosc import dispatcher
		from pythonosc import osc_server

		parser = argparse.ArgumentParser()

		parser.add_argument("--ip", default=self.ip, help="The ip to listen on")

		parser.add_argument("--port", type=int, default=self.port, help="The port to listen on")

		args = parser.parse_args()

		dispatcher = dispatcher.Dispatcher()
		dispatcher.map("/muse/elements/experimental/mellow", print)

		server = osc_server.ThreadingOSCUDPServer( (args.ip, args.port), dispatcher )
		print("Serving on {}".format(server.server_address))
		server.serve_forever()
	
	def stop(self):
		self._stop_event.set()

	def stopped(self):
		return self._stop_event.is_set()

	
if __name__ == "__main__":
	print("Aby wyłączyć naciśnij q albo klawisz ESC")
	
	# Init Threads
	OSCServerThread = oscServerThread(1, "OSCServerThread", "127.0.0.1", 5000)

	# Start Threads
	OSCServerThread.start()
	
	# Wait for exit sign
	x = input()
	if x == "q":
		OSCServerThread.stop()
		return 0
