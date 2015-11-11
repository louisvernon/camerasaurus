import json
import configuration
import cgi
import string
import control

# receive handler for web server and return json encoded camera configuration
def get_cameras(web_handler):
    web_handler.send_response(200)
    web_handler.send_header('Content-type','text/html')
    web_handler.end_headers()
    # read configuration from disk
    
    #try:
    settings_file = open("cameras.json")
    settings_json = string.join(settings_file.readlines(), "")
    camera_settings = json.loads(settings_json)
    settings_file.close()
    #except:
     #   camera_settings = "false"
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
            web_handler.wfile.write("Failed:Name")
            return
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
    
    
    
    # create camera instance!
    try:
        camera_control = control.Camera(name=camera_name, url=camera_settings[camera_name]["camera_url"])
    except:
        web_handler.wfile.write("Failed:Camera Instantiation")
        return
    
    try:
        camera_control.take_snapshot(camera_name + ".jpg")
    except:
        web_handler.wfile.write("Failed:Camera Snapshot")
        return
    web_handler.wfile.write("Validated")
    # generate snapshot
    
    