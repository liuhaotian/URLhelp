#!/usr/bin/python
#
#   Author: Haotian Liu
#   Email:  liuhaotian.air@gmail.com
#
#   usage:  from checkmx import checkMX
#           checkMX('your url')
#

from urlparse import urlparse
import subprocess

def checkMX(url):
    try:
        urlObj  = urlparse(url)
        mxdata  = subprocess.check_output(['dig','-t','MX', urlObj.netloc])
        return len([x for x in mxdata.split('\n') if 'MX' in x and ';' not in x])
        #return len(resolver.query(urlObj.netloc, 'MX'))
    except Exception, e:
        return 0

def main():
    print checkMX('http://twitter.com/cnnbrk')
    print '=' * 50
    print checkMX('http://t.co/xdBHUbHc')

if __name__ == '__main__':
    main()