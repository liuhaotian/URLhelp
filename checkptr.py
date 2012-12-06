#!/usr/bin/python
#
#   Author: Haotian Liu
#   Email:  liuhaotian.air@gmail.com
#
#   usage:  from checkptr import checkPTR
#           checkPTR('your url')
#

from urlparse import urlparse
import socket

def checkPTR(url):
    try:
        socket.setdefaulttimeout(2)
        urlObj  = urlparse(url)
        #return socket.getfqdn(urlObj.netloc) == urlObj.netloc
        allips  = [x[4][0] for x in socket.getaddrinfo(urlObj.netloc,80) if ':' not in x[4][0]]
        subips  = [x[4][0] for x in socket.getaddrinfo(socket.gethostbyaddr(urlObj.netloc)[0],80) if ':' not in x[4][0]]
        return all([x in allips for x in subips])
    except Exception, e:
        return False

def main():
    print checkPTR('http://www.renren.com/cnnbrk')
    print '=' * 50
    print checkPTR('http://t.co/xdBHUbHc')

if __name__ == '__main__':
    main()