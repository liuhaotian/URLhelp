#!/usr/bin/python
#
#   Author: Haotian Liu
#   Email:  liuhaotian.air@gmail.com
#
#   usage:  just run it
#

import webapp2

class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, webapp2!')

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('main')
        
class Paper(webapp2.RequestHandler):
    def get(self):    
        self.response.headers['Content-Type'] = 'application/pdf'
        self.response.write(open('paper.pdf').read())

def main():
    from paste import httpserver
    app = webapp2.WSGIApplication([
        ('/', MainPage),
        ('/paper', Paper),
        ('/hello', HelloWebapp2),
        ], debug=True)
    httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()