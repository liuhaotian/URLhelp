#!/usr/bin/python
#
#   Author: Haotian Liu
#   Email:  liuhaotian.air@gmail.com
#
#   usage:  from checkrank import checkRank
#           checkRank('your list of urls')
#

from urlparse import urlparse

def checkRank(urls):
    rankfile    = open('top-1m.csv','r')
    rankdb      = rankfile.readlines()
    rankfile.close()
    rankdict    = dict()
    for eachline in rankdb:
        rank, domain    = eachline.rstrip('\n').split(',')
        rankdict[domain]    = int(rank)
    
    urlranks    = []

    for eachurl in urls:
        theurl  = urlparse(eachurl).netloc
        while '.' in theurl:
            try:
                rankdict[theurl]
                break
            except Exception, e:
                theurl = theurl.split('.',1)[1]

        if '.' in theurl:
            urlranks.append(rankdict[theurl])
        else:
            urlranks.append(1000001)

    return urlranks

def main():
    urls = []
    urls += ['http://www.google.com/']
    urls += ['http://wenku.baidu.com/']
    urls += ['http://ianfette.org/']
    print checkRank(urls)

if __name__ == '__main__':
    main()