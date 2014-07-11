# -*- coding: utf-8 -*-
"""
@author: Zibo, Kelly
"""
from functools import wraps
import errno
import os
import signal
import urllib2
import re
import sys
from sgmllib import SGMLParser

reload(sys)
sys.setdefaultencoding('utf-8')
sys.getfilesystemencoding()
class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wraps(func)(wrapper)
    return decorator

output = open("output.txt", "w")

http = re.compile(r'^(?:http|ftp)s?://' # http:// or https://
					r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain
					r'localhost|' #localhost
					r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
					r'(?::\d+)?' # optional port
					r'(?:/?|[/?]\S+)$', re.IGNORECASE)

yuming = re.compile(r'ifeng')
keyword = raw_input("key word: ")
pattern = re.compile(keyword)
date= re.compile('og:time')

url_user = raw_input("initial webpage:  ")
if url_user.find("http://")==-1:
	url_user="http://"+url_user
url_deep = 7
key_threshold = 1
key_threshold2 = 3
threshold = 0
cnt = 0
urllist = []
urllist.append(url_user)

def binsearch(sequence, number, lower = 0, upper = None):
	if len(sequence) == 0: return False
	if upper == None: upper = len(sequence) - 1
	if lower == upper:
		if number == sequence[upper]:
			return True
		return False
	else:
		middle = (lower + upper) // 2
		if number > sequence[middle]:
			return binsearch(sequence, number, middle+1, upper)
		else:
			return binsearch(sequence, number, lower, middle)

@timeout(5)
class URLLister(SGMLParser):
	def reset(self):
		SGMLParser.reset(self)
		self.urls = []
		self.is_a = 0
		self.is_href = 0
		self.key_num = 0
		self.tag=0
	def start_a(self, attrs):
		href = [v for k, v in attrs if k == 'href']
		if href and http.search(href[0]) and yuming.search(href[0]):
			if (href[0])[-1] != '/':
				href[0] += '/'
			if not binsearch(urllist, href[0]):
				self.urls.append(href[0])
				urllist.append(href[0])
				urllist.sort()
	def end_a(self):
		self.is_a = 0
		self.is_href = 0
	def start_meta(self, attrs):
		name = [v for k, v in attrs if k == 'name']
		cont = [v for k, v in attrs if k == 'content']
		for i in range(0,len(name)):
			if (name[i]=='og:time ' and int(cont[i])>1400469332) or (name[i]!='og:time '):
				self.tag=1
	def end_meta(self):
		pass
	def handle_data(self,data):
		pass

@timeout(10)
def process(url, deep):
	global cnt
	global threshold
	if deep > url_deep:
		return
	if deep <= 2:
		threshold = key_threshold
	if deep > 2 and deep < 4:
		threshold = 3
	if deep >= 4 and deep <= 7:
		threshold = 5
	try:
		req=urllib2.Request(url)
		page = urllib2.urlopen(req)
		lister = URLLister()
		cont = page.read()
		cont = re.sub(r'<!','',cont)
		lister.feed(cont)
	except Exception, e:
		print "error: ", e
		return
	page.close()
	print url
	num=len(pattern.findall(cont))
	if lister.tag:
		cnt += num
	if num >= threshold:
		output.write("key num: %d, url: %s, deep: %d\n" % (num, url, deep))
		print ("key num: %d, url: %s, deep: %d" % (num, url, deep))
		for l in lister.urls:
			process(l, deep+1)

process(url_user, 0)
print ("all key num is: %d" % cnt)