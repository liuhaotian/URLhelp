#!/usr/bin/python
#
#   Author: Haotian Liu
#   Email:  liuhaotian.air@gmail.com
#
#   usage:  from checkwhois import checkWhois
#           checkWhois('your url')
#

import subprocess
from urlparse import urlparse

def checkWhois(url):
    try:
        urlObj = urlparse(url)
        return subprocess.check_output(['whois',urlObj.netloc])
    except Exception, e:
        return url

def main():
    print checkWhois('http://bit.ly/Yj18wU') #   test one time redirecting
    print '=' * 50
    print checkWhois('http://t.co/xdBHUbHc') #   test recursively redirecting

if __name__ == '__main__':
    main()