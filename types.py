# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class Prepare(object):
	def __init__(self):
		self.base_url = 'http://www.dianping.com/shanghai/ch10'
		self.headers = {
            'Host':'www.dianping.com',
            'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; Chitanda/Akari) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 MicroMessenger/6.0.0.58_r884092.501 NetType/WIFI'
         }
		self.count = 0
		self.foodtype = set()
		self.districts = set()
		self.urls = [] 
	def get_base_html(self):
		base_html = requests.get(self.base_url,headers = self.headers)
		return base_html
	def get_foodtypes(self):
		base_html = self.get_base_html()
		soup = BeautifulSoup(base_html.text)
		results = soup.find('div',attrs = {'id':'classfy','class':"nc-items"})
		for child in results.find_all('a'):
			url2 = child.get('href')
			# self.foodtype.add('g'+str(child.get('data-cat-id')))
			food_html = requests.get(url2,headers = self.headers)
			soup2 = BeautifulSoup(food_html.text)
			items = soup2.find('div',attrs = {"class":"con"})
			if(items == []):
				print url2
				continue
			for item in items.find_all('a'):
				self.foodtype.add('g'+str(item.get('data-cat-id')))
		print self.foodtype
		return self.foodtype
	def get_districts(self,url):
		base_html2 = requests.get(url,headers = self.headers)
		soup = BeautifulSoup(base_html2.text)
		results = soup.find('div',attrs = {'id':'region-nav','class':"nc-items"})
		for child in results.find_all('a'):
			url2 = child.get('href')
			# self.districts.add('r'+str(child.get('data-cat-id')))
			streets_html = requests.get(url2,headers = self.headers,timeout=5)
			soup2 = BeautifulSoup(streets_html.text)
			items = soup2.find('div',attrs = {'id':'region-nav-sub'})
			if(items == None):
				print 'error:',url2
				self.urls.append(url2)
				continue
			for item in items.find_all('a'):
				url4 = item.get('href')
				self.count +=1
				print self.count,':',url4
				self.urls.append(url4)
	def get_urls(self):
		base_html = self.get_base_html()
		soup = BeautifulSoup(base_html.text)
		results = soup.find('div',attrs = {'id':'classfy','class':"nc-items"})
		for child in results.find_all('a'):
			url2 = child.get('href')
			# self.foodtype.add('g'+str(child.get('data-cat-id')))
			food_html = requests.get(url2,headers = self.headers)
			soup2 = BeautifulSoup(food_html.text)
			items = soup2.find('div',attrs = {"id":"classfy-sub"})
			if(items == None):
				print 'error:',url2
				continue
			for item in items.find_all('a'):
				url3 = item.get('href')
				self.get_districts(url3)
if __name__ == '__main__':
	 fo = open("test.log",'w+')
	 sys.stdout = fo
	 p = Prepare()
	 p.get_urls()