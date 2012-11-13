#!/usr/bin/python
#
#   Author: Haotian Liu
#   Email:  liuhaotian.air@gmail.com
#
#   usage:  from checkgooglesb import checkGoogleSB
#           checkGoogleSB('your list of urls')
#

import urllib2

def checkGoogleSB(urls):
    key     = ''
    sbapi = 'https://sb-ssl.google.com/safebrowsing/api/lookup?client=URLhelp&apikey=' + key + '&appver=1.0&pver=3.0'
    reqdata = '\n'.join([str(len(urls))] + urls)
    try:
        return urllib2.urlopen(sbapi, reqdata).read().split('\n')
    except Exception, e:
        return ['ok'] * len(urls)

def main():
    urls = []
    urls += ['http://www.google.com/']
    urls += ['http://ianfette.org/']
    print checkGoogleSB(urls)

if __name__ == '__main__':
    main()