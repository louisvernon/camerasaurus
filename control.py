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
		command = '%s -i %s -codec copy -y %s' % (ffmpeg, self.url)
		command_components = string.split(command)
		command_components.append(filepath)
		self.recorder = subprocess.Popen(command_components)

	def stop_recording(self):
		self.recorder.terminate()

	def take_snapshot(self, filepath):
		command = '%s -i %s -vframes 1 -q:v 1 -y' % (ffmpeg, self.url)
		command_components = string.split(command)
		command_components.append(filepath)
		exit_code = subprocess.call(command_components)
		return exit_code
