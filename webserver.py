#!/usr/bin/env python3

import http.server
import socketserver
import urllib.parse as urlparse
import os
import time

machines = {
    'lg-tv': {
        'power-toggle': (lambda: os.system("/usr/local/bin/irsend SEND_ONCE LG_AKB73715601 KEY_POWER"))
    },
    'xfinity-box': {
        '0': (lambda: os.system("/usr/local/bin/irsend SEND_ONCE Xfinity-XR2 0")),
        '1': (lambda: os.system("/usr/local/bin/irsend SEND_ONCE Xfinity-XR2 1")),
        '2': (lambda: os.system("/usr/local/bin/irsend SEND_ONCE Xfinity-XR2 2")),
        '3': (lambda: os.system("/usr/local/bin/irsend SEND_ONCE Xfinity-XR2 3")),
        '4': (lambda: os.system("/usr/local/bin/irsend SEND_ONCE Xfinity-XR2 4")),
        '5': (lambda: os.system("/usr/local/bin/irsend SEND_ONCE Xfinity-XR2 5")),
        '6': (lambda: os.system("/usr/local/bin/irsend SEND_ONCE Xfinity-XR2 6")),
        '7': (lambda: os.system("/usr/local/bin/irsend SEND_ONCE Xfinity-XR2 7")),
        '8': (lambda: os.system("/usr/local/bin/irsend SEND_ONCE Xfinity-XR2 8")),
        '9': (lambda: os.system("/usr/local/bin/irsend SEND_ONCE Xfinity-XR2 9")),
    },
    'sony-receiver': {
        'power-toggle': (lambda: os.system("/usr/local/bin/irsend SEND_ONCE SONY_RM-AAU014 BTN_POWER")),
        'xfinity-input': (lambda: os.system("/usr/local/bin/irsend SEND_ONCE SONY_RM-AAU014 BTN_VIDEO1")),
        
        'vol-up': (lambda: os.system("/usr/local/bin/irsend SEND_ONCE SONY_RM-AAU014 BTN_VOLUME_UP")),
        'vol-down': (lambda: os.system("/usr/local/bin/irsend SEND_ONCE SONY_RM-AAU014 BTN_VOLUME_DOWN")),
        
    },
    'sony-media': {
        'power-toggle': (lambda: os.system("/usr/local/bin/irsend SEND_ONCE SONY_DP KEY_POWER"))
    }
}

index_source = "/opt/chip-remote-remote/index.html"

def do_action(action):
    if action == "Button A":
        machines['sony-receiver']['power-toggle']()
    elif action == "Jeopardy":
        # Assumes everything is turned off
        machines['lg-tv']['power-toggle']()
        machines['sony-receiver']['power-toggle']()
        
        time.sleep(0.900)
        
        machines['sony-receiver']['xfinity-input']()
        machines['xfinity-box']['0']()
        machines['xfinity-box']['7']()
        
        for i in range(0, 7): # 7 total iterations
           machines['sony-receiver']['vol-up']()
        
    else:
        print(action)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytearray(open(index_source, "rb").read()))
        
        os.system("mkdir /var/run/lirc ; /usr/local/sbin/lircd & ") # Crummy hack, both do nothing if unecessary
        
        return
    
    def do_POST(self):
        # Get url parameter of 'butt' value (Which button was pressed)
        qs = {}
        path = self.path
        if '?' in path:
            path, tmp = path.split('?', 1)
            qs = urlparse.parse_qs(tmp)
            
            do_action(qs["butt"][0])
                
        # Construct a response.
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytearray(open(index_source, "rb").read()))
        
        os.system("mkdir /var/run/lirc ; /usr/local/sbin/lircd & ") # Crummy hack, both do nothing if unecessary
        
        return

try:
    httpd = socketserver.TCPServer(('', 80), Handler)
    httpd.serve_forever()
except:
    index_source = "index.html"
    httpd = socketserver.TCPServer(('', 8080), Handler)
    httpd.serve_forever()

# Deploy with
# scp ./webserver.py root@192.168.10.2:/opt/chip-remote-remote/
# and kill the old python server
# ssh root@192.168.10.2
