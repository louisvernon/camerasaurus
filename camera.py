import vlc
import time
import uuid

class Camera:
	def __init__(self, ip, user, password, name, path):
		self.ip = ip
		self.user = user
		self.password = password
		self.name = name
		self.path = path
	def start_recording(self):
		filename = self.path + self.name + str(int(time.time())) + ".ogg"
		print filename
		rtsp_path = "rtsp://" + self.user + ":" + self.password + "@" + self.ip + ":554"
		print rtsp_path
		self.instance=vlc.Instance("--sout=file/avi:" + filename)
		self.player = self.instance.media_player_new()
		self.player.set_mrl(rtsp_path)
		self.player.play()		
	def stop_recording(self):
		self.player.stop()
	def take_snapshot(self):
		filename = self.path + self.name + str(int(time.time())) + ".jpg"
		print vlc.libvlc_video_take_snapshot(self.player, 0, "test.jpg", 0, 0)


		
def record_stream(camera):
	print camera



camera = Camera(ip="192.168.1.84x",user="admin",password="password",name="Location",path="")

camera.start_recording()
time.sleep(100)
camera.stop_recording()
camera.take_snapshot()
