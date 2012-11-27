#!/usr/bin/python
#
#   Author: Haotian Liu
#   Email:  liuhaotian.air@gmail.com
#
#   usage:  from checkns import checkNS
#           checkNS('your url')
#

from urlparse import urlparse
import dns.resolver

def checkNS(url):
    try:
        urlObj  = urlparse(url)
        return len(dns.resolver.query(urlObj.netloc, 'NS'))
    except Exception, e:
        return 0

def main():
    print checkNS('http://twitter.com/cnnbrk')
    print '=' * 50
    print checkNS('http://t.co/xdBHUbHc')

if __name__ == '__main__':
    main()