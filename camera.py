import time
import uuid
import urllib
import os
import subprocess
import tempfile

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
		self.streaming = False	

	def start_recording(self):
		self.instance=vlc.Instance("--sout=file/avi:" + filename)
		self.player = self.instance.media_player_new()
		self.player.set_mrl(rtsp_path)
		self.player.play() 		

	def stop_recording(self):
		self.recorder.terminate()
	def save_snapshot(self):
		filename = self.path + self.name + str(int(time.time())) + ".jpg"
		rtsp_path = "rtsp://" + self.user + ":" + self.password + "@" + self.ip + ":" +  str(self.port)
		command = [ffmpeg, "-i", rtsp_path, "-vf", "select=\"eq(pict_type\\,I)\"", "-vframes", "1", "-qscale", "0", filename]
		print command
		subprocess.call(command)
		return filename		
	def get_snapshot(self):
		filename = self.path + "tmp_" + str(uuid.uuid4()) + ".jpg"
		rtsp_path = "rtsp://" + self.user + ":" + self.password + "@" + self.ip + ":" +  str(self.port)
		command = [ffmpeg, "-i", rtsp_path, "-vf", "select=\"eq(pict_type\\,I)\"", "-vframes", "1", "-qscale", "0", filename]
		print command
		subprocess.call(command)
		return filename

	def start_live_stream(self):
		tmpdir = tempfile.mkdtemp()
		filename = os.path.join(tmpdir, 'myfifo')
		try:
			os.mkfifo(filename)
		except OSError, e:
			print "Failed to create FIFO: %s" % e
		else:
			print "open pipe to write"
			fifo = open(filename, 'w+')
		rtsp_path = "rtsp://" + self.user + ":" + self.password + "@" + self.ip + ":" +  str(self.port)
#		command = [ffmpeg, "-rtsp_transport", "tcp", "-i", rtsp_path, "-vcodec", "copy", "-f", "mp4", "-movflags", "frag_keyframe+empty_moov", "-reset_timestamps", "1", "-vsync", "1","-flags", "global_header", "-bsf:v", "dump_extra", "-y", "-"]
		command = [ffmpeg, "-rtsp_transport", "tcp", "-i", rtsp_path, "-vcodec", "copy", "-f", "mp4", "-movflags", "frag_keyframe+empty_moov", 
                    "-reset_timestamps", "1", "-vsync", "1","-flags", "global_header", "-bsf:v", "dump_extra", "-y", "-"]
		print command
		print filename
		self.streamer = subprocess.Popen(command, stdout=fifo, stderr=devnull)
		self.streaming = True
		return filename
#		self.stream = streamer.communicate()[0]
		



camera = Camera(ip="home.nxsfan.co.uk", port=25001, user="admin",password="security",name="Front_Door",path="tmp/")
#print camera.start_live_stream()
