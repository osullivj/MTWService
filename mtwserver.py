# Mininal Tornado Web Server JOS 2016-05-04
# Requirements: Python 3.4, Tornado 4.3
# Launch at the command line with...
# c:\python34\python mtwserver.py
import socket
import logging
import os
import tornado.ioloop
import tornado.web
import sys

# Some constants - hack these to change the port, or the home page
PORT=9090
HOST=socket.gethostname( )
HomePage="<html><body><p>HomePage http://%s:%d</p></body></html>" % ( HOST, PORT)
TestPage="<html><body><p>TestPage http://%s%s:%d</p></body></html>"

class RootHandler( tornado.web.RequestHandler):
    def get( self):
        self.write( HomePage)

class TestHandler( tornado.web.RequestHandler):
    def get( self):
        self.write( TestPage % ( HOST, self.request.uri, PORT))

class ExitHandler( tornado.web.RequestHandler):
    def get( self):
        tornado.ioloop.IOLoop.current( ).stop( )

def make_app( ):
    return tornado.web.Application([
        (r'/', RootHandler),
        (r'/exit', ExitHandler),
		(r'/.*', TestHandler),
    ])

if __name__ == "__main__":
    # tornado logs to stdout by default - we want it in a file in the %TEMP% dir
    logf = '%s\\mtwserver_%d.log' % ( os.environ.get('TEMP'), os.getpid( ))
    logfmt = '%(asctime)s %(levelname)s %(thread)s %(message)s'
    logging.basicConfig( filename=logf, format=logfmt, level=logging.INFO)
    app = make_app( )
    app.listen( PORT)
    tornado.ioloop.IOLoop.current( ).start( )
