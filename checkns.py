#!/usr/bin/python
#
#   Author: Haotian Liu
#   Email:  liuhaotian.air@gmail.com
#
#   usage:  from checkns import checkNS
#           checkNS('your url')
#

from urlparse import urlparse
import subprocess

def checkNS(url):
    try:
        urlObj  = urlparse(url)
        mxdata  = subprocess.check_output(['dig','-t','NS', urlObj.netloc])
        return len([x for x in mxdata.split('\n') if 'NS' in x and ';' not in x])
        #return len(resolver.query(urlObj.netloc, 'NS'))
    except Exception, e:
        return 0

def main():
    print checkNS('http://twitter.com/cnnbrk')
    print '=' * 50
    print checkNS('http://t.co/xdBHUbHc')

if __name__ == '__main__':
    main()