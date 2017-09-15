#!/usr/bin/env python3

import http.server
import socketserver
import urllib.parse as urlparse
import os

machines = {
    'sony-receiver': {
        'power-toggle': (lambda: os.system("/usr/local/bin/irsend SEND_ONCE SONY_RM-AAU014 BTN_POWER"))
    }
}

index_source = "/opt/chip-remote-remote/index.html"

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Get url parameter of 'butt' value (Which button was pressed)
        qs = {}
        path = self.path
        if '?' in path:
            path, tmp = path.split('?', 1)
            qs = urlparse.parse_qs(tmp)
            
            if qs["butt"][0] == "Button A":
                machines['sony-receiver']['power-toggle']()
            else:
                print(qs["butt"][0])
                
        # Construct a response.
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(bytearray(open(index_source, "rb").read()))
        
        os.system("mkdir /var/run/lirc ; /usr/local/sbin/lircd & ") # Crummy hack
        
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
