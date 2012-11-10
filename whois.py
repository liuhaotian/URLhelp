#!/usr/bin/python
#
#   Author: Haotian Liu
#   Email:  liuhaotian.air@gmail.com
#
#   usage:  from whois import whois
#           whois('your domain')
#
import socket

def whois(domain):
    HOST = 'whois.verisign-grs.com'
    PORT = 43 

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(domain + '\r\n')
    data = s.recv(65536) + s.recv(65536)
    s.close()
    return data

def main():
    print whois('aa.com')

if __name__ == '__main__':
    main()