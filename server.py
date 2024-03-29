#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import json
import configuration



PORT_NUMBER = 8000

def return_exception(self, e):
	print "Crap, exception!"
	print e.message, e.args
	self.send_response(200)
	self.send_header('Content-type',"text/html")
	self.end_headers()
	self.wfile.write("FAILED:Exception")	



#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_POST(self):
		print self.path
		if self.path == "/add_camera":
			try: configuration.add_camera(self)
			except Exception as e: return_exception(self, e)
		if self.path == "/delete_camera":
			try: configuration.delete_camera(self)
			except Exception as e: return_exception(self, e)
		if self.path == "/validate_camera":
			try: configuration.validate_camera(self)
			except Exception as e: return_exception(self, e)
		if self.path == "/update_schedule":
			try: configuration.update_schedule(self)
			except Exception as e: return_exception(self, e)
		
	def do_GET(self):
		# strip and discard hash part from url to avoid caching
		self.path = self.path.split('?')[0]
		
		if self.path=="/":
			self.path="/no_image.gif"
		try:
			#Check the file extension required and
			#set the right mime type
			if self.path == "/get_cameras":
				try: configuration.get_cameras(self)
				except: return_exception(self)
				return				

			sendReply = False            
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".png"):
				mimetype='image/png'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path)
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				#self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
				#self.send_header('Pragma','no-cache')
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			else:
				raise IOError()
			
		
			
			return


		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)

	print 'Started httpserver on port ' , PORT_NUMBER

	#Wait forever for incoming http requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
