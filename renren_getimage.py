#download photos from a friend's album in renren.com
# -*- coding:utf-8 -*-
import requests
import re
import urllib
from bs4 import BeautifulSoup
def getImage(http):
	soup=BeautifulSoup(http)
	temp=soup.find_all('a',{'class':'picture'})
	total=[]
	counts=0
	for item in temp:
		total.insert(counts,item['href'])
		counts+=1
	return total

def saveImage(http,count):
	soup=BeautifulSoup(http)
	temp=soup.find_all('img',{'id':'photo'})
	for item in temp:
		urllib.urlretrieve(item['src'],"picture%s.jpg"%count)
		count+=1
		print count
	return count
	
s=requests.Session()
headers ={"User-agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
logininfo={"email":"******","password":"******"}
r=s.post("http://www.renren.com/PLogin.do",data=logininfo,headers=headers)
r2=s.get("http://photo.renren.com/photo/*********/album/relatives") ## ********:friend's id
images=getImage(r2.text)
count=0
for item in images:
	r=s.get(item)
	count=saveImage(r.text,count)
