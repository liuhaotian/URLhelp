#!/usr/bin/python
#
#   Author: Haotian Liu
#   Email:  liuhaotian.air@gmail.com
#
#   usage:  from checkip import checkIP
#           checkIP('your url')
#

from urlparse import urlparse
import socket

def checkIP(url):
    try:
        urlObj  = urlparse(url)
        return [x[4][0] for x in socket.getaddrinfo(urlObj.netloc,80) if ':' not in x[4][0]]
    except Exception, e:
        return ['127.0.0.1']

def main():
    print checkIP('http://twitter.com/cnnbrk')
    print '=' * 50
    print checkIP('http://t.co/xdBHUbHc')

if __name__ == '__main__':
    main()