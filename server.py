import os
import tempfile
import camera
from functools import partial
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

class CamerasaurusServer(BaseHTTPRequestHandler):
	def do_GET(self):
		if(".mp4" in self.path):
			if(not camera.camera.streaming): stream = camera.camera.start_live_stream()
			print "streaming from", stream
			self.send_response(200)
#			self.send_header('Transfer-Encoding', 'chunked')
			self.send_header('Connection', 'keep-alive')
			self.send_header('Content-type', 'video/mp4')
			self.send_header('Accept-Ranges', 'bytes')
			self.send_header('Content-length', '102400000000000000')
			self.end_headers()
			try:
				with open(stream, 'rb') as openfileobject:
					for chunk in iter(partial(openfileobject.read, 1024), ''):
						print "chunk"
						self.wfile.write(chunk)
			except: pass
			return
			
						

		else:
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write(self.path)
			self.wfile.write('<video width="320" height="240">')
			self.wfile.write('<source src="movie.mp4" type="video/mp4">')
			self.wfile.write('</video>')
			return



#print camera.camera.save_snapshot()
#print camera.camera.get_snapshot()


server = HTTPServer(('',80),CamerasaurusServer)
server.serve_forever()
