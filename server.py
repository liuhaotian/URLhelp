#!/usr/bin/python
#
#   Author: Haotian Liu
#   Email:  liuhaotian.air@gmail.com
#
#   usage:  just run it
#

import webapp2
import socket

class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, webapp2!')

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(open('www/index.html').read())

class cssHandler(webapp2.RequestHandler):
    def get(self):
        #self.response.write('pic')
        try:
            self.response.write(open('www' + self.request.path).read())
            self.response.headers['Content-Type'] = 'text/css'
        except Exception, e:
            pass

class jsHandler(webapp2.RequestHandler):
    def get(self):
        #self.response.write('pic')
        try:
            self.response.write(open('www' + self.request.path).read())
            self.response.headers['Content-Type'] = 'text/javascript'
        except Exception, e:
            pass

class htmlHandler(webapp2.RequestHandler):
    def get(self):
        #self.response.write('pic')
        try:
            self.response.write(open('www' + self.request.path).read())
        except Exception, e:
            pass

class pngFileHandler(webapp2.RequestHandler):
    def get(self):
        #self.response.write('pic')
        try:
            self.response.write(open('www' + self.request.path).read())
            self.response.headers['Content-Type'] = 'image/png'
        except Exception, e:
            pass
        
class pdfFileHandler(webapp2.RequestHandler):
    def get(self):
        #self.response.write('pic')
        try:
            self.response.write(open('www' + self.request.path).read())
            self.response.headers['Content-Type'] = 'application/pdf'
        except Exception, e:
            pass

def main():
    from paste import httpserver
    app = webapp2.WSGIApplication([
        ('/', MainPage),
        (r'/.*\.pdf', pdfFileHandler),
        (r'/.*\.css', cssHandler),
        (r'/.*\.html', htmlHandler),
        (r'/.*\.png', pngFileHandler),
        (r'/.*\.js', jsHandler),
        ('/hello', HelloWebapp2),
        ], debug=True)
    httpserver.serve(app, host = socket.gethostbyname(socket.gethostname()), port='8080')

if __name__ == '__main__':
    main()