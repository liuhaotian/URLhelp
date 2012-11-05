#!/usr/bin/python
#
#   Author: Haotian Liu
#   Email:  liuhaotian.air@gmail.com
#
#   usage:  from checkredirect import checkRedirect
#           checkRedirect('your url')
#

import httplib
from urlparse import urlparse

def checkRedirect(url):
    try:
        urlObj = urlparse(url)
        conn = httplib.HTTPConnection(urlObj.netloc)
        conn.request("HEAD", url.lstrip(urlObj.scheme).lstrip('://').lstrip(urlObj.netloc)
)
        res = conn.getresponse()
        returl = [x[1] for x in res.getheaders() if x[0] == 'location'][0]
        
        if res.status == 301:
            return checkRedirect(returl)
        else:
            return url
    except Exception, e:
        return url

def main():
    print checkRedirect('http://bit.ly/Yj18wU') #   test one time redirecting
    print checkRedirect('http://t.co/xdBHUbHc') #   test recursively redirecting

if __name__ == '__main__':
    main()