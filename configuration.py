import json
import configuration
import cgi
import string
import control
import os
import urllib

# receive handler for web server and return json encoded camera configuration
def get_cameras(web_handler):
    web_handler.send_response(200)
    web_handler.send_header('Content-type','text/html')
    web_handler.end_headers()
    # read configuration from disk
    
    try:
        settings_file = open("cameras.json")
        settings_json = string.join(settings_file.readlines(), "")
        camera_settings = json.loads(settings_json)
        settings_file.close()
    except:
        camera_settings = {}
    camera_settings = json.dumps(camera_settings)
    print camera_settings
    
    web_handler.wfile.write(camera_settings)


def add_camera(web_handler):
    web_handler.send_response(200)
    web_handler.send_header('Content-type','text/html')
    web_handler.end_headers()
    ctype, pdict = cgi.parse_header(web_handler.headers.getheader('content-type'))
    if ctype == 'multipart/form-data':
        postvars = cgi.parse_multipart(web_handler.rfile, pdict)
    elif ctype == 'application/x-www-form-urlencoded':
        length = int(web_handler.headers.getheader('content-length'))
        postvars = cgi.parse_qs(web_handler.rfile.read(length), keep_blank_values=1)
    else:
        postvars = {}
        
    if(len(postvars)==0):
            web_handler.wfile.write("Failed:Post")
            return
        
    camera = {}
    for key in postvars.keys():
        camera[key] = postvars[key][0]
    #camera = json.loads(camera)    
    print camera
    
            
    try:
        settings_file = open("cameras.json")
        settings_json = string.join(settings_file.readlines(), "")
        camera_settings = json.loads(settings_json)
        settings_file.close()
    except:
        camera_settings = {}
    
    if(camera["camera_name"] in camera_settings.keys()):
        if("camera_edit" in camera.keys()):
            if(camera["camera_edit"] == "off"):
                web_handler.wfile.write("Failed:Name")
                return
            else:
                schedule = camera_settings[camera["camera_name"]][schedule]
        else:
            web_handler.wfile.write("Failed:Name")
            return
        
    # test for schedule, if not create blank
    try:
        schedule[0][0]
    except:
        schedule = []
        for i in range(7):
            day = []
            for j in range(24):
                day.append(0)
            schedule.append(day)
        
    camera["schedule"] = schedule
    print "Adding:", camera["camera_name"]
    camera_settings[camera["camera_name"]] = camera
    try:
        settings_file = open("cameras.json", "w")
        settings_json = json.dumps(camera_settings)
        settings_file.write(settings_json)
        settings_file.close()
    except:
        web_handler.wfile.write("Failed:Write")
        return
    
    web_handler.wfile.write("Added")
    

def delete_camera(web_handler):
    web_handler.send_response(200)
    web_handler.send_header('Content-type','text/html')
    web_handler.end_headers()
    ctype, pdict = cgi.parse_header(web_handler.headers.getheader('content-type'))
    if ctype == 'multipart/form-data':
        postvars = cgi.parse_multipart(web_handler.rfile, pdict)
    elif ctype == 'application/x-www-form-urlencoded':
        length = int(web_handler.headers.getheader('content-length'))
        postvars = cgi.parse_qs(web_handler.rfile.read(length), keep_blank_values=1)
    else:
        postvars = {}
        
    if(len(postvars)==0):
            web_handler.wfile.write("Failed:Post")
            return
    camera_name = postvars.keys()[0]
    print "Deleting:", camera_name
    
    try:
        settings_file = open("cameras.json")
        settings_json = string.join(settings_file.readlines(), "")
        camera_settings = json.loads(settings_json)
        settings_file.close()
    except:
        web_handler.wfile.write("Failed:Read")
        return
        
    try:
        camera_settings.pop(camera_name)
    except:
        web_handler.wfile.write("Failed:Name")
        return
    
    print camera_settings
    
    try:
        settings_file = open("cameras.json", "w")
        settings_json = json.dumps(camera_settings)
        settings_file.write(settings_json)
        settings_file.close()
    except:
        web_handler.wfile.write("Failed:Write")
        return
    
    web_handler.wfile.write("Deleted")



def validate_camera(web_handler):
    web_handler.send_response(200)
    web_handler.send_header('Content-type','text/html')
    web_handler.end_headers()
    ctype, pdict = cgi.parse_header(web_handler.headers.getheader('content-type'))
    if ctype == 'multipart/form-data':
        postvars = cgi.parse_multipart(web_handler.rfile, pdict)
    elif ctype == 'application/x-www-form-urlencoded':
        length = int(web_handler.headers.getheader('content-length'))
        postvars = cgi.parse_qs(web_handler.rfile.read(length), keep_blank_values=1)
    else:
        postvars = {}
        
    if(len(postvars)==0):
            web_handler.wfile.write("Failed:Post")
            return
    camera_name = postvars.keys()[0]
    print "validating:", camera_name
    
    try:
        settings_file = open("cameras.json")
        settings_json = string.join(settings_file.readlines(), "")
        camera_settings = json.loads(settings_json)
        settings_file.close()
    except:
        web_handler.wfile.write("Failed:Read")
        return
    
    
    
    writable = os.access(camera_settings[camera_name]["camera_storage_path"], os.W_OK)
    print "storage path", camera_settings[camera_name]["camera_storage_path"]
    if(not writable):
        web_handler.wfile.write("Failed:Path")
        return
    
    # create camera instance!
    try:
        camera_control = control.Camera(name=camera_name, url=camera_settings[camera_name]["camera_url"])
    except:
        web_handler.wfile.write("Failed:Instantiation")
        return

    
    # generate snapshot
    print camera_name, type(camera_name)
    snapshot_file = urllib.quote_plus(camera_name) + ".jpg"
    exit_code = camera_control.take_snapshot(snapshot_file)
    
    try:
        exit_code = camera_control.take_snapshot(snapshot_file)
                                                 
        if(exit_code!=0):
            web_handler.wfile.write("Failed:FFMPEG")
            return                
    except:
        web_handler.wfile.write("Failed:Snapshot")
        return
    web_handler.wfile.write("Validated")
    
    
    
    
    
    
def update_schedule(web_handler):
    web_handler.send_response(200)
    web_handler.send_header('Content-type','text/html')
    web_handler.end_headers()
    ctype, pdict = cgi.parse_header(web_handler.headers.getheader('content-type'))
    if ctype == 'multipart/form-data':
        postvars = cgi.parse_multipart(web_handler.rfile, pdict)
    elif ctype == 'application/x-www-form-urlencoded':
        length = int(web_handler.headers.getheader('content-length'))
        postvars = cgi.parse_qs(web_handler.rfile.read(length), keep_blank_values=1)
    else:
        postvars = {}
        
    if(len(postvars)==0):
            web_handler.wfile.write("Failed:Post")
            return

    camera = {}
    for key in postvars.keys():
        camera[key] = postvars[key][0]    
    print camera
    camera = json.loads(camera["camera"])      
    print camera
    

    print "Updating Schedule for camera:", camera["camera_name"]
    
    try:
        settings_file = open("cameras.json")
        settings_json = string.join(settings_file.readlines(), "")
        camera_settings = json.loads(settings_json)
        settings_file.close()
    except:
        web_handler.wfile.write("Failed:Read")
        return    
    print camera["camera_name"]
    print camera["schedule"]
    print camera_settings[camera["camera_name"]]["schedule"]
    camera_settings[camera["camera_name"]]["schedule"] = camera["schedule"]
    
    
    try:
        settings_file = open("cameras.json", "w")
        settings_json = json.dumps(camera_settings)
        settings_file.write(settings_json)
        settings_file.close()
    except:
        web_handler.wfile.write("Failed:Write")
        return
    
    web_handler.wfile.write("Updated")    

    
    