#!/usr/bin/python
import httplib
from urlparse import urlparse

def checkRedirect(url):
	try:
		urlObj = urlparse(url)
		conn = httplib.HTTPConnection(urlObj.netloc)
		conn.request("HEAD", urlObj.path)
		res = conn.getresponse()
		return [x[1] for x in res.getheaders() if x[0] =='location'][0]
	except Exception, e:
		return url

def main():
	print checkRedirect('http://bit.ly/Yj18wU')

if __name__ == '__main__':
	main()