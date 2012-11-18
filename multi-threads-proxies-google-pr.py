#
#	Multi-Threads Handler Class:	ThreadHandleURLs	(threads_num, url_queue,proxy_queue, handler )
#					Parameters:		threads_num:	the number of threads
#					 				url_queue:		A queue of URLs to be handled
#									proxy_queue:	A queue of proxies 
#									handler:		A handler class, it should have a re-enter function #													handleURL(url, proxy_url)
#					Details:		This class can handle URLs by multiple threads and proxies
#  
#	Google Page Rank Retrival Class:GooglePageRank		()
#					Parameters:								
#					Details:		This class provides a function handleURL(url,proxy_url), which is re#									quired by class ThreadHandleURLs 	
#															
#	Simple Page Crawler Class:		PageCrawler	()	
#					Parameters:
#					Details:		This class also provides handleURL(url,proxy_url) function, which is#									used to test class ThreadHandleURLs 				

import urllib2
import re
import sys
from threading import Thread, Lock
from Queue import Queue
import time
import socket
from threading import stack_size

#Set Environment
#socket.setdefaulttimeout(30)
stack_size(32768*16)

class GooglePageRank():
	def __init__(self):
		pass
	def handleURL(self,url,proxy_url):
		gurl='http://www.google.com/search?q=link%3A{0}&ie=utf-8&oe=utf-8&rls=org.mozilla:en-US:official&client=firefox-a'.format(urllib2.quote(url))
		headers = {
			'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:14.0) Gecko/20100101 Firefox/14.0.1'
		}	
				
		#proxy
		proxy_support = urllib2.ProxyHandler({'http':proxy_url})
		opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)

		#Build Request
		req = urllib2.Request(
			url = gurl,
			headers = headers
		)
		try:
			content = opener.open(req).read()
			link_num = self.extractLinkNum(content,url)
		except ValueError as e:
			print >> sys.stderr, 'Value Error:[',url,', ',proxy_url,']',e
			return -1
		except urllib2.HTTPError as e:
			print >> sys.stderr, 'HTTPError Error:[',url,', ',proxy_url,']',e
			return -2
		except urllib2.URLError as e:
			print >> sys.stderr, 'URLError Error:[',url,', ',proxy_url,']',e
			return -3
		except:
			print >> sys.stderr, 'UnExpected Error:[',url,', ',proxy_url,']',sys.exc_info()[0]
			return -4

		if link_num < 0:
			#print url,' failed to get link number'
			print >> sys.stderr, 'Failed Error:[',url,', ',proxy_url,']',sys.exc_info()[0]
			print >> sys.stderr, content
			return -5
		else:
			#print 'Result: ',url, ' ', link_num
			return link_num
	
	def extractLinkNum(self,content,url):
		start_pos = 0
		p1 = re.compile('(\d+[,.;])*\d+')
		p2 = re.compile('(\d+(&#160;))+\d+')
		while True:
			index1 = content.find('<div id=resultStats>',start_pos)
			if index1 == -1: 
				index1 = content.find('link:'+url.strip()+' - Google')
				if index1 >= 0:	
					return 0
				else:
					return -1
			end = len(content)
			if end>index1+100:
				end = index1+100
			number = content[index1+20:end]
			m1 = p1.search(number)
			m2 = p2.search(number)
			if not m2 is None:
				return m2.group().replace('&#160;','')
			elif not m1 is None:
				number = m1.group().strip()
				number = number.replace(',','')
				number = number.replace('.','')
				#print 'DEBUG convert:',number
				return int(number)
		return -1

#Retrive the size of the URL pages
class PageCrawler():
	def __init__(self):
		pass
	
	def handleURL(self,url,proxy):
		#proxy
		#if not url.startswith('http'):
		#	url = 'http://'+url
		proxy_support = urllib2.ProxyHandler({'http':proxy})
		self.opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    	#Build Request
		headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:14.0) Gecko/20100101 Firefox/14.0.1'}
		req = urllib2.Request(
			url = url,
			headers = headers
    	)   
		#print req.get_full_url()
   		#content = urllib2.urlopen(req).read()
		try:
			content = self.opener.open(req).read()
		except ValueError as e:
			print >>sys.stderr,'value error: ',e
			return -1
		except urllib2.HTTPError as e:
			print >>sys.stderr,'HTTPError: ',e
			return -1
		except urllib2.URLError as e:
			print >>sys.stderr,'URLERROR: ',e
			return -1
		except:
			print sys.stderr, 'Unexpected Error:',sys.exc_info()[0]
			return -2
		return len(content)

#Parameters:	threads_num is the number of threads
#				url_queue is a queue recording the URLs to be handled
#				proxy_queue is a queue recording the available proxies
#				handler is an object with method handleURL(URL,proxy)
class ThreadHandleURLs:
	def __init__(self,threads_num, url_queue,proxy_queue, handler ):
		self.lock = Lock()			# threading clock
		self.task_q = url_queue   	# queue of task to be done
		self.finished_q = Queue()	# queue of finished tasks
		self.unfinished_q = Queue()	# queue of tasks that can't be handled
		self.proxy_q = proxy_queue	# queue of available proxies
		self.bad_proxy_q = Queue()	# queue of invalid proxies
		self.threads_n = threads_num# number of threads
		self.failed_times = {}		# dictionary of failed times for each proxy
		self.handler = handler
		self.running = 0 
		for i in range(self.threads_n):
			t = Thread(target=self.handleURLs)
			t.setDaemon(True)
			t.start()
	
	def push(self,url):
		self.task_q.put(url)
	def pop(self):
		return self.finished_q.get()
	def displayEveryQueue():
		print 'Final Result:'
		print 'Extracted Results:'
		while self.finished_q.qsize()>0:
			print self.finished_q.get()
		print ''
		print 'Unfinished URLs:'
		while self.unfinished_q.qsize()>0:
			print self.unfinished_q.get()
		print ''
		print 'Number of valid proxies: ',self.proxy_q.qsize()
		print 'Number of invalid proxies: ',self.bad_proxy_q.qsize()
	
	def hasTaskLeft(self):
		return self.task_q.qsize()+self.running+self.finished_q.qsize()

	def getNextProxy(self):
	#	if self.proxy_q.qsize()<50:
	#		print >>sys.stderr, 'There are few proxies left! [%d]' %(self.proxy_q.qsize())
		return self.proxy_q.get()	
			
	def handleURLs(self):
		while True:
			req = self.task_q.get()
			with self.lock:
				self.running += 1
			#print 'Threads start to work!'
			url = self.task_q.get()
			try:
				flag = False
				proxy_url = ''
				#Each URL will try three times before putting in unfinished_q 
				proxy_url = self.getNextProxy()
				for i in range(1,6):
					ans = self.handler.handleURL(url,proxy_url)
					if ans < 0:
						#self.bad_proxy_q.put(proxy_url)
						times = 0
						with self.lock:
							times = self.failed_times.setdefault(proxy_url,0)
							times += 1
							if times < 1500:
								self.failed_times[proxy_url]=times
								#self.proxy_q.put(proxy_url)

						if times >= 1500:
							print >>sys.stderr, 'INVALID PROXY, ', proxy_url
							print >>sys.stderr, 'Size of Valid Proxy:',self.proxy_q.qsize()
							self.bad_proxy_q.put(proxy_url)
							proxy_url = self.getNextProxy()
					else:
						temp_rs = url+' result:'+str(ans)
						print temp_rs
						sys.stdout.flush()
						self.finished_q.put(temp_rs)
						flag = True
						self.proxy_q.put(proxy_url)
						break
				if flag==False:
					#self.unfinished_q.put(url)	
					self.unfinished_q.put(url)	
					self.proxy_q.put(proxy_url)
			except Exception as e:
				#We assueme normal exception will be captured in object handler
				#So if program comes here, something must be wrong
				print >>sys.stderr,' Exception in handleURLs, should see log ASAP!!! [URL:',url,'Proxy:',proxy_url,']'
				print >>sys.stderr,e
				self.unfinished_q.put(url)
				self.bad_proxy_q.put(proxy_url)	

			with self.lock:
				self.running -= 1
			self.task_q.task_done()
			time.sleep(0.1)

def main():
	
	f = open('result','r')
	h_urls = []
	for line in f:
		m=line.split()
		m[0] = m[0].strip()
		if not m[0] in h_urls:
			h_urls.append(m[0])
	print 'Handled ',len(h_urls),' URLs!'
	f.close()	
	
	f = open('top10000','r')
	#def __init__(self,threads_num, url_queue,proxy_q, handler ):
	url_queue = Queue()
	for line in f:
		if line.strip() in h_urls:
			continue
		url_queue.put(line.strip())
	f.close()

	f = open('good_proxy','r')
	proxy_queue = Queue()
	for line in f:
		proxy_queue.put(line.strip())
	f.close()

	print 'URL:',url_queue.qsize(),' Proxy:',proxy_queue.qsize()
	handler = PageCrawler()
	handler = GooglePageRank()
	#print handler.handleURL('taobao.com','200.106.149.26')
	
	crawlers = ThreadHandleURLs(3,url_queue,proxy_queue,handler)
	while crawlers.hasTaskLeft():
		crawlers.pop()

main()
