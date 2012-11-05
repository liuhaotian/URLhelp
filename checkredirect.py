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
        agent = { 'User-Agent' : 'Mozilla/5.0' }
        conn.request("HEAD", url.lstrip(urlObj.scheme).lstrip('://').lstrip(urlObj.netloc), headers=agent)
        res = conn.getresponse()
        returl = [x[1] for x in res.getheaders() if x[0] == 'location'][0]
        if returl == url:
            return returl
        else:
            return checkRedirect(returl)
    except Exception, e:
        return url

def main():
    print checkRedirect('http://bit.ly/Yj18wU') #   test one time redirecting
    print checkRedirect('http://t.co/xdBHUbHc') #   test recursively redirecting

if __name__ == '__main__':
    main()