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


class oscServer:
	serverThread = None

	MuseIoAdress= None
	MuseIoPort = None

	def __init__(self, adress="127.0.0.1", port=5000):
		self.MuseIoAdress = adress 
		self.MuseIoPort = port

		self.serverThread = threading.Thread(target=self.run, daemon = True)
		self.serverThread.start() 

	#init OSC server thread
	def run(self):
		from pythonosc import dispatcher
		from pythonosc import osc_server

		dispatcher = dispatcher.Dispatcher()
		dispatcher.map("/muse/batt", print)

		server = osc_server.ThreadingOSCUDPServer((self.MuseIoAdress, self.MuseIoPort), dispatcher)
		server.serve_forever()  				
				
class HttpServer:
	httpServerThread = None

	def __init__(self):
		self.httpServerThread = threading.Thread(target=self.run, daemon = True)
		self.httpServerThread.start() 

	def run(self):
		import os
		import cherrypy
		
		#Http server class
		class cherryModel(object):
			@cherrypy.expose
			def index(self):
				return """Hello World XD"""	
		
		conf = {
			'/': {
				'tools.sessions.on': True,
				'tools.staticdir.root': os.path.abspath(os.getcwd())
			},
			'/static': {
				'tools.staticdir.on': True,
				'tools.staticdir.dir': './client'
			}
		}
		cherrypy.engine.signals.subscribe()
		cherrypy.quickstart(cherryModel(), '/', conf)	
		
if __name__ == "__main__":
	print("Aby wylaczyc nacisnij q albo klawisz ESC")
	
	oscServer = oscServer()
	httpServe = HttpServer()
	
	# Wait for exit sign
	while 1:
		x = input()
		if x == "q":
			break
		
