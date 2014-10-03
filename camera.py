import time
import uuid
import urllib
import os
import subprocess

devnull = open(os.devnull, 'w')
ffmpeg = "./ffmpeg"

class Camera:
	def __init__(self, ip, user, password, name, path):
		self.ip = ip
		self.user = user
		self.password = password
		self.name = name
		self.path = path
		
	def start_recording(self):
		filename = self.path + self.name + str(int(time.time())) + "_%04d.mkv"
		rtsp_path = "rtsp://" + self.user + ":" + self.password + "@" + self.ip + ":554"
		command = [ffmpeg, "-i", rtsp_path, "-codec", "copy",  "-map", "0", "-f", "segment", "-segment_time", "3600", filename]
		print filename
		self.recorder = subprocess.Popen(command, stdout=devnull, stderr=devnull)
		
	def stop_recording(self):
		self.recorder.kill()	
	def take_snapshot(self):
		filename = self.path + self.name + str(int(time.time())) + ".jpg"
		urllib.urlretrieve("http://" + self.user + ":" + self.password + "@" + self.ip + "/Streaming/Channels/1/picture", filename)
		
def record_stream(camera):
	print camera



camera = Camera(ip="192.168.1.86",user="admin",password="security",name="Front_Door",path="tmp/")
camera.start_recording()
time.sleep(100)
camera.stop_recording()
