import time
import uuid
import urllib
import os
import subprocess
import tempfile
import pickle

# open config

config = pickle.load(open("config.db"))
for camera in config.cameras:
	# check if camera is enabled
	if(not camera.enabled): continue
	
	# check if we should be recording	


