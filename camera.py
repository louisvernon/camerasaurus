import time
import uuid
import urllib
import os
import subprocess
import string

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
		#command = [ffmpeg, "-i", rtsp_path, "-codec", "copy",  "-map", "0", "-f", "segment", "-segment_time", "3600", filename]
		command = '%s -i %s -codec copy %s' % (ffmpeg, rtsp_path, filename)
		self.recorder = subprocess.Popen(string.split(command))

	def stop_recording(self):
		self.recorder.terminate()

	def take_snapshot(self):
		filename = self.path + self.name + str(int(time.time())) + ".jpg"
		rtsp_path = "rtsp://" + self.user + ":" + self.password + "@" + self.ip + ":" +  str(self.port)
		command = '%s -i %s -vframes 1 -q:v 1 %s' % (ffmpeg, rtsp_path, filename)
		subprocess.call(string.split(command))
		return filename




camera = Camera(ip="garage", port=554, user="admin",password="security",name="Front_Door",path="tmp/")
#camera.start_recording()
print camera.take_snapshot()

time.sleep(2)

camera.start_recording()

time.sleep(5)

camera.stop_recording()

#camera.stop_recording()
