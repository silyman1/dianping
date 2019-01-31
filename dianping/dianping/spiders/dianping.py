# -*- coding: utf-8 -*-
import scrapy 
from scrapy import Request
from scrapy.spiders import Spider
from dianping.items import DianpingItem
from types import Prepare


class DianpingSpider(Spider):
	
	name = 'dianping'
	
	def __init__(self,):
		self.headers = {
            'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; Chitanda/Akari) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 MicroMessenger/6.0.0.58_r884092.501 NetType/WIFI'
         }
		 self.p = Prepare()
		 self.foodtypes = self.p.get_foodtypes()
		 self.locations = self.p.get_districts()