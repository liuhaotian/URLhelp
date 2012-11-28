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
from whois import whois

def checkWhois(url):
    try:
        urlObj  = urlparse(url)
        retdata = whois(urlObj.netloc)
        #retdata = subprocess.check_output(['whois',urlObj.netloc])
        try:
            expire_date = re.search(r'[Ee][Xx][Pp][Ii][Rr][^:]{0,20}[:OoNn]{1,2}(.*[\d].*[\d].*)',retdata).groups()[0]
            expire_date = parser.parse(expire_date.strip('. '))
        except Exception, e:
            expire_date = parser.parse('1970-01-01 00:00:00')

        try:
            update_date = (re.search(r'[Uu][Pp][Dd][Aa][Tt][Ee][^:]{0,20}[Dd][Aa][Tt][Ee][^:]{0,20}[:OoNn]{1,2}(.*[\d].*[\d].*)',retdata) or re.search(r'[Uu][Pp][Dd][Aa][Tt][Ee][^:]{0,20}[:OoNn]{1,2}(.*[\d].*[\d].*)',retdata)).groups()[0]
            update_date = parser.parse(update_date.strip('. '))
        except Exception, e:
            update_date = parser.parse('1970-01-01 00:00:00')

        try:
            create_date = (re.search(r'[Rr][Ee][Gg][Ii][Ss][Tt][^:]{0,20}[Dd][Aa][Tt][Ee][^:]{0,20}[:OoNn]{1,2}(.*[\d].*[\d].*)',retdata) or re.search(r'[Cc][Rr][Ee][Aa][Tt][EeIi][^:]{0,20}[Dd][Aa][Tt][Ee][^:]{0,20}[:OoNn]{1,2}(.*[\d].*[\d].*)',retdata) or re.search(r'[Cc][Rr][Ee][Aa][Tt][Ee][^:]{0,20}[:OoNn]{1,2}(.*[\d].*[\d].*)',retdata)).groups()[0]
            create_date = parser.parse(create_date.strip('. '))
        except Exception, e:
            create_date = parser.parse('1970-01-01 00:00:00')

        try:
            registrant  = re.search(r'[^@]*\ ([^\ ]+@[^\ ]+\.[\w]+)[\W]',retdata).groups()[0]
        except Exception, e:
            registrant  = ''
        
        if registrant  == '' and expire_date == parser.parse('1970-01-01 00:00:00') and update_date == parser.parse('1970-01-01 00:00:00') and create_date == parser.parse('1970-01-01 00:00:00') and len(urlObj.netloc.split('.')) > 1:
            #print urlObj.scheme + '://' + urlObj.netloc.split('.',1)[1]
            #print retdata
            return checkWhois(urlObj.scheme + '://' + urlObj.netloc.split('.',1)[1])
        else:
            return dict([('expire_date', expire_date), ('update_date', update_date), ('create_date', create_date), ('registrant', registrant)])
        #return dict([('expire_date', expire_date), ('update_date', update_date), ('create_date', create_date), ('registrant', registrant)])
    except Exception, e:
        return dict([('expire_date', parser.parse('1970-01-01 00:00:00')), ('update_date', parser.parse('1970-01-01 00:00:00')), ('create_date', parser.parse('1970-01-01 00:00:00')), ('registrant', '')])

def main():
    print checkWhois('http://twitter.com/cnnbrk') #   test one time redirecting
    print '=' * 50
    print checkWhois('http://t.co/xdBHUbHc') #   test recursively redirecting

if __name__ == '__main__':
    main()