from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import parse_qsl
from values import config
from lib import router
import SocketServer
import json
import sys

from controllers import client

run_types = ['server', 'client']

if len(sys.argv) == 1:
    print "Please provide a parameter defining if this is a `server` or `client`"
    exit()
    
run_type = sys.argv[1]

if run_type not in run_types:
    print "Invalid run type provided"
    
class Handler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.end_headers()
        
    def _get_body(self):
        request_sz = int(self.headers["Content-length"])
        request_str = self.rfile.read(request_sz) + " "
        return dict(parse_qsl(request_str))
        
    def _json_response(self, data, status=200):
        print "Sending response:", data
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data))

    def do_GET(self):
        print "Received GET: ", self.path
        
        if run_type == 'client':
            if self.headers["Server-Access-Key"] == config.ACCESS_KEY:
                response_data = router.client_router(self.path) 
                self._json_response(response_data)
            else:
                self._json_response({
                    "error": "Unauthorized request"
                }, status=403)
        else:
            self._set_headers(404)
            
    def do_POST(self):
        self._set_headers()
        body = self._get_body()
    
        if run_type == 'client':
            router.client_router(self.path, body) 
            
        if run_type == 'server':
            if self.path == '/sms/reply/':
                if body['AccountSid'] == config.ACC_ID:
                    router.server_router(body['From'], body['Body'])
                else:
                    print "Unauthorized twilio account ID"


if __name__ == '__main__':
    server_address = ('', int(config.PORT))
    httpd = HTTPServer(server_address, Handler)
    print 'HTTP server running'
    httpd.serve_forever()
