__author__ = "Ganapathy Raman"

from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse
import re
import urllib
import urllib2

student_message = '<html> \
                      <head> \
                         <title>Student\'s Portal</title> \
                      </head> \
                      <body> \
                         <h1 align=\'center\'>Welcome to Student\'s Portal</h1> \
			 <h3 align=\'center\'>(From Server - 1)</h3> \
                      </body> \
                   </html>'

staff_message = '<html> \
                    <head> \
                       <title>Staff\'s Portal</title> \
                    </head> \
                    <body> \
                          <h1 align=\'center\'>Welcome to Staff\'s Portal</h1> \
			  <h3 align=\'center\'>(From Server - 1)</h3> \
                    </body> \
                </html>'

class GetHandler(BaseHTTPRequestHandler):

    global student_message, staff_message
    def do_GET(self):
	client_address = self.client_address
        parsed_path = urlparse.urlparse(self.path)
	print "Client IP: ", client_address
	ipaddr = '200.0.0.2'
	if ipaddr in client_address:
		print "Inside"
		message = staff_message
	else:
		message = student_message
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)
        return

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('', 80), GetHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
