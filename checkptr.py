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
        urlObj  = urlparse(url)
        return socket.getfqdn(urlObj.netloc) == urlObj.netloc
    except Exception, e:
        return False

def main():
    print checkPTR('http://twitter.com/cnnbrk')
    print '=' * 50
    print checkPTR('http://t.co/xdBHUbHc')

if __name__ == '__main__':
    main()