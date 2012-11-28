#!/usr/bin/python
#
#   Author: Haotian Liu
#   Email:  liuhaotian.air@gmail.com
#
#   usage:  from whois import whois
#           whois('your domain')
#
import socket
import re

def whois(domain, host = None):
    if host is None:
        HOST = domain.rsplit('.',1)[1] + '.whois-servers.net'
    else:
        HOST = host
    PORT = 43 

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(domain + '\r\n')

    data = s.recv(65536)
    length = 0
    while length < len(data):
        length = len(data)
        data += s.recv(65536)
    s.close()

    if "\"=xxx\"" in data:
        return whois('domain ' + domain)
    elif findhost(data) is not None and findhost(data) != host:
        return data + '\n' + whois(domain, findhost(data))
    else:
        return data

    #return findhost(data) is not None and whois(domain, findhost(data)) or "\"=xxx\"" in data and whois('=' + domain) or data

def findhost(rawdata):
    whoisserv = [\
    "whois.abuse.net",\
    "whois.crsnic.net",\
    "whois.networksolutions.com",\
    "whois.nic.mil",\
    "whois.nic.gov",\
    "whois.arin.net",\
    "whois.lacnic.net",\
    "whois.ripe.net",\
    "whois.apnic.net",\
    "whois.ra.net",\
    "whois.6bone.net",\
    "whois.registro.br",\
    "whois.norid.no",\
    "whois.iana.org"]
    try:
        #server = re.search(r'Whois Server:[^\w]*([\.\w]*)',rawdata).groups()[0]
        return re.search(r'Whois Server:[^\w]*([\.\w]*)',rawdata).groups()[0]
    except Exception, e:
        return None
'''
    if server in whoisserv:
        return server
    elif 'whois-servers' in server.rsplit('.'):
        return server
    else:
        return None
'''

def main():
    print whois('t.co')

if __name__ == '__main__':
    main()