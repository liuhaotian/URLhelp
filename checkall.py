#!/usr/bin/python
#
#   Author: Haotian Liu
#   Email:  liuhaotian.air@gmail.com
#
#   usage:  just run it
#

from checkredirect import checkRedirect
from checkwhois import checkWhois
from checkgooglesb import checkGoogleSB
from checkip import checkIP
from checkptr import checkPTR
from checkns import checkNS
from checkmx import checkMX
from checkrank import checkRank
import sys

def main(tid = 0):
    fin = open('phishing_list','r')
    urls = [x.split()[0] for x in fin.readlines()]
    fin.close()
    fout = open('phishing_list_result','a')
    if tid == 0:
        therange = range(len(urls))
    else:
        therange = range(400 * (tid - 1), 400 * tid)

    results = []
    for i in therange:
        url = urls[i]
        if 'http' not in url[:6]:
            url = 'http://' + url
            urls[i] = url
        oneresult = dict()
        oneresult['redirecturl'] = checkRedirect(url)
        oneresult['thewhoisdict'] = checkWhois(oneresult['redirecturl'])
        oneresult['ips'] = checkIP(oneresult['redirecturl'])
        oneresult['ptr'] = checkPTR(oneresult['redirecturl'])
        oneresult['num_ns'] = checkNS(oneresult['redirecturl'])
        oneresult['num_mx'] = checkMX(oneresult['redirecturl'])
        #oneresult['rank'] = checkRank([oneresult['redirecturl']])[0]

        #fout.write('%d\t%s\t%d\t%d\t%d\t%s\t%s\t%s\t%s\t%s\t%s\n' % (len(ips), ptr, num_ns, num_mx, rank, thewhoisdict['create_date'].isoformat(), thewhoisdict['update_date'].isoformat(), thewhoisdict['expire_date'].isoformat(), thewhoisdict['registrant'], redirecturl, url))
        results += [oneresult]

    SBlabels = checkGoogleSB([eachresult['redirecturl'] for eachresult in results])
    ranks   = checkRank([eachresult['redirecturl'] for eachresult in results])
    for SBlabel, rank, eachresult in zip(SBlabels, ranks, results):
        eachresult['SBlabel'] = SBlabel
        eachresult['rank']  = rank
        fout.write('%s\t%d\t%s\t%d\t%d\t%d\t%s\t%s\t%s\t%s\t%s\n' % (eachresult['SBlabel'], len(eachresult['ips']), eachresult['ptr'], eachresult['num_ns'], eachresult['num_mx'], eachresult['rank'], eachresult['thewhoisdict']['create_date'].isoformat()[:19], eachresult['thewhoisdict']['update_date'].isoformat()[:19], eachresult['thewhoisdict']['expire_date'].isoformat()[:19], eachresult['thewhoisdict']['registrant'], eachresult['redirecturl']))



if __name__ == '__main__':
    try:
        tid = int(sys.argv[1])
    except Exception, e:
        tid = 0

    main(tid)