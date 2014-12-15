import time
import uuid
import urllib
import os
import subprocess
import tempfile
import pickle



class Camera:
        def __init__(self, ip, port, user, password, name):
                self.ip = ip
                self.port = port
                self.user = user
                self.password = password
                self.name = name
		self.enabled = True
		self.schedule= []
		for i in range(7):
			self.schedule.append([])
			self.schedule[-1] = []
			for j in range(24): self.schedule[-1].append([])
		

camera = Camera(ip="home.nxsfan.co.uk", port=25001, user="admin",password="security",name="Front_Door")

try: config = pickle.load(open("config.db"))
except: config = {}

camera.enabled=True
config[camera.name] = camera
pickle.dump(config, open("config.db", "w"))
