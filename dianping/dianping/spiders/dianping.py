# -*- coding: utf-8 -*-
import scrapy 
from scrapy import Request
from scrapy.spiders import Spider
from dianping.items import DianpingItem
from types import Prepare
from analyse import Addrdict


class DianpingSpider(Spider):
	
	name = 'dianping'
	
	def __init__(self,):
		self.headers = {
            'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; Chitanda/Akari) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 MicroMessenger/6.0.0.58_r884092.501 NetType/WIFI'
         }
		self.base_url = 'http://www.dianping.com/shanghai/ch10/'
		self.p = Prepare()
		self.foodtypes = self.p.get_foodtypes()
		self.locations = self.p.get_districts()
		
		self.d = Addrdict()
		d.set_pik_dict()
		self.xkz = d.xkz
		self.pik = d.pikdict
		
		
	def start_requests(self):
		for type in self.foodtypes:
			for lo in self.locations:
				url = self.base_url + str(type) + str(lo)
				yield scrapy.Request(url=url,callback=self.next_page)
	def next_page(self,response):
		url = str(response.url)
		flag = response.xpath("//*[@class='page']")
		if(flag)
			pages = flag.xpath("//a[last()-1]")
		for i in range(1,int(pages)+1):
			page_url = url + 'p' + str(i)
			yield scrapy.Request(url = page_url ,callback=self.parse_url)
	def parse_url(self,response):
		