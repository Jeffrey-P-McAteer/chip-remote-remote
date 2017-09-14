#!/usr/bin/env python3

import http.server

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        
        # Construct a response.
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(open("index.html").read())
        return

httpd = socketserver.TCPServer(('', 80), Handler)
httpd.serve_forever()

