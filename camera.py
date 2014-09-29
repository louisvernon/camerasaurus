import vlc
import time
import uuid
import urllib

class Camera:
	def __init__(self, ip, user, password, name, path):
		self.ip = ip
		self.user = user
		self.password = password
		self.name = name
		self.path = path
		
	def start_recording(self):
		filename = self.path + self.name + str(int(time.time())) + ".ogg"
		rtsp_path = "rtsp://" + self.user + ":" + self.password + "@" + self.ip + ":554"
		self.instance=vlc.Instance("--sout=file/avi:" + filename)
		self.player = self.instance.media_player_new()
		self.player.set_mrl(rtsp_path)
		self.player.play()		
	def stop_recording(self):
		self.player.stop()
	def take_snapshot(self):
		filename = self.path + self.name + str(int(time.time())) + ".jpg"
		urllib.urlretrieve("http://" + self.user + ":" + self.password + "@" + self.ip + "/Streaming/Channels/1/picture", filename)
		
def record_stream(camera):
	print camera



camera = Camera(ip="192.168.1.107",user="admin",password="password",name="Garage",path="")
camera.start_recording()
time.sleep(5)
camera.take_snapshot()
time.sleep(5)
camera.stop_recording()
