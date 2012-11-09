#!/usr/bin/python
#
#   Author: Haotian Liu
#   Email:  liuhaotian.air@gmail.com
#
#   usage:  from checkwhois import checkWhois
#           checkWhois('your url')
#

import subprocess
import re
from urlparse import urlparse
from dateutil import parser

def checkWhois(url):
    try:
        urlObj  = urlparse(url)
        retdata = subprocess.check_output(['whois',urlObj.netloc])
        try:
            expire_date = re.search(r'[Ee][Xx][Pp][Ii][Rr][^:]*:(.*)',retdata).groups()[0]
            expire_date = parser.parse(expire_date)
        except Exception, e:
            expire_date = parser.parse('1970-01-01 00:00:00')

        try:
            update_date = (re.search(r'[Uu][Pp][Dd][Aa][Tt][Ee][^:]*[Dd][Aa][Tt][Ee][^:]*:(.*)',retdata) or re.search(r'[Uu][Pp][Dd][Aa][Tt][Ee][^:]*:(.*)',retdata)).groups()[0]
            update_date = parser.parse(update_date)
        except Exception, e:
            update_date = parser.parse('1970-01-01 00:00:00')

        try:
            create_date = (re.search(r'[Rr][Ee][Gg][Ii][Ss][Tt][^:]*[Dd][Aa][Tt][Ee][^:]*:(.*)',retdata) or re.search(r'[Cc][Rr][Ee][Aa][Tt][Ee][^:]*[Dd][Aa][Tt][Ee][^:]*:(.*)',retdata) or re.search(r'[Cc][Rr][Ee][Aa][Tt][Ee][^:]*:(.*)',retdata)).groups()[0]
            create_date = parser.parse(create_date)
        except Exception, e:
            create_date = parser.parse('1970-01-01 00:00:00')
        

        return dict([('expire_date', expire_date), ('update_date', update_date), ('create_date', create_date)])
    except Exception, e:
        return url

def main():
    print checkWhois('http://bit.ly/Yj18wU') #   test one time redirecting
    print '=' * 50
    print checkWhois('http://t.co/xdBHUbHc') #   test recursively redirecting

if __name__ == '__main__':
    main()