import time
import uuid
import urllib
import os
import subprocess

devnull = open(os.devnull, 'w')
ffmpeg = "ffmpeg"

class Camera:
	def __init__(self, ip, port, user, password, name, path):
		self.ip = ip
		self.port = port
		self.user = user
		self.password = password
		self.name = name
		self.path = path
		
	def start_recording(self):
		filename = self.path + self.name + str(int(time.time())) + "_%04d.mkv"
		rtsp_path = "rtsp://" + self.user + ":" + self.password + "@" + self.ip + ":" +  str(self.port)
		command = [ffmpeg, "-i", rtsp_path, "-codec", "copy",  "-map", "0", "-f", "segment", "-segment_time", "3600", filename]
		print filename
		self.recorder = subprocess.Popen(command)
		
	def stop_recording(self):
		self.recorder.kill()
	def take_snapshot(self):
		filename = self.path + self.name + str(int(time.time())) + ".jpg"
		rtsp_path = "rtsp://" + self.user + ":" + self.password + "@" + self.ip + ":" +  str(self.port)
		command = [ffmpeg, "-i", rtsp_path, "-vf", "select=\"eq(pict_type\,I)\"", "-vframes", "1", "-qscale", "0", filename]
		print command
		subprocess.Popen(command)
		return filename		
		
def record_stream(camera):
	print camera



camera = Camera(ip="home.nxsfan.co.uk", port=25001, user="admin",password="security",name="Front_Door",path="tmp/")
#camera.start_recording()
print camera.take_snapshot()
time.sleep(2)
#camera.stop_recording()
