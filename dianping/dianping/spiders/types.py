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
		self.foodtype = set()
		self.districts = set()
	def get_base_html(self):
		base_html = requests.get(self.base_url,headers = self.headers)
		return base_html
	def get_foodtypes(self):
		base_html = self.get_base_html()
		soup = BeautifulSoup(base_html.text)
		results = soup.find('div',attrs = {'id':'classfy','class':"nc-items"})
		f  = open("test.log",'w+')
		sys.stdout = f
		for child in results.find_all('a'):
			url2 = child.get('href')
			food_html = requests.get(url2,headers = self.headers)
			soup2 = BeautifulSoup(food_html.text)
			items = soup.find('div',attrs = {"class":"con"})
			if(items == []):
				print url2
				continue
			for item in items.find_all('a'):
				self.foodtype.add('g'+str(item.get('data-cat-id')))
		print self.foodtype
		return self.foodtype
	def get_districts(self):
		base_html = self.get_base_html()
		soup = BeautifulSoup(base_html.text)
		results = soup.find('div',attrs = {'id':'region-nav','class':"nc-items"})
		for child in results.find_all('a'):
			url2 = child.get('href')
			streets_html = requests.get(url2,headers = self.headers)
			soup2 = BeautifulSoup(streets_html.text)
			items = soup.find('div',attrs = {'id':'J_nt_items'})
			for item in items.find_all('a'):
				self.districts.add('r'+str(item.get('data-cat-id')))
		print self.districts
		return self.districts
if __name__ == '__main__':
	 p = Prepare()
	 p.get_foodtypes()
	 p.get_districts()