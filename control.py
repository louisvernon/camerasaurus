import time
import uuid
import urllib
import os
import subprocess
import string

devnull = open(os.devnull, 'w')
ffmpeg = "ffmpeg"

class Camera:
	def __init__(self, url, name):
		self.url = url
		self.name = name

	def start_recording(self, filepath):
		command = '%s -i %s -codec copy -y %s' % (ffmpeg, self.url, filename)
		self.recorder = subprocess.Popen(string.split(command))

	def stop_recording(self):
		self.recorder.terminate()

	def take_snapshot(self, filepath):
		command = '%s -i %s -vframes 1 -q:v 1 -y %s' % (ffmpeg, self.url, filepath)
		exit_code = subprocess.call(string.split(command))
		return exit_code
