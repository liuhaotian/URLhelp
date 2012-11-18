# Crawler to crawl the URLs in www.dmoz.org

import os
import sys
from bs4 import BeautifulSoup
from bs4.element import Tag
import urllib2

def DMOZCrawler():
	url=''
	if len(sys.argv) == 1:
		url = 'http://www.dmoz.org'
	else:
		url = sys.argv[1]

	content = urllib2.urlopen(url).read()
	soup = BeautifulSoup(content)
	elems = soup.find('div',{'class','one-third'})

	while elems != None:
		samps = elems.findAll('samp')
		#samps.findAll()
		for item in samps:
			#print type(item)
			for a in item.contents:
				if type(a)==Tag:
					DMOZSubCrawler(a['href'])
		elems = elems.findNextSibling('div',{'class','one-third'})


def DMOZSubCrawler(path):
	#print path
	base = 'http://www.dmoz.org'
	url = base+path
	soup = None
	try:
		#print path
		content = urllib2.urlopen(url).read()
		soup = BeautifulSoup(content)
	except Exception as e:
		print >>sys.stderr, 'Error URL: ',url
		return

	print >>sys.stderr, 'Processing URL: ',url
	if soup == None:
		return
	dir_1 = soup.find('div',class_='dir-1 borN')
	while dir_1 != None:
		elem = dir_1.find('ul',class_="directory dir-col")
		while elem != None:
			item=elem.find('li')
			while item != None:
				a = item.find('a')
				if a != None:
					DMOZSub2Crawler(a['href'])
				item = item.findNextSibling('li');
			#print '=========================='		
			elem = elem.findNextSibling('ul',class_="directory dir-col")
		dir_1 = dir_1.findNextSibling('div',class_='dir-1 borN')
	
def DMOZSub2Crawler(path):
	base = 'http://www.dmoz.org'
	url = base+path
	
	try:
		content = urllib2.urlopen(url).read()
		soup = BeautifulSoup(content)
	except Exception as e:
		print >>sys.stderr, 'Error URL: ',url
		return
	if soup == None:
		return
	field = soup.find('fieldset')
	while field != None:
		ul = field.find('ul',class_='directory-url')
		if ul != None:
			li = ul.find('li')
			while li != None:
				a = li.find('a')
				if a != None:
					print a['href']
				li = li.findNextSibling('li')			
		field = field.findNextSibling('fieldset')


DMOZCrawler()
