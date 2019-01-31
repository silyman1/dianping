# -*- coding: utf-8 -*-
import scrapy 
from scrapy import Request
from scrapy.spiders import Spider
from dianping.items import DianpingItem
from types import Prepare
from analyse import Addrdict

import requests


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
		shoplist = response.xpath("//*[@data-click-name='shop_img_click']/@href")
		for shop_url in shoplist:
			 yield scrapy.Request(url=shop_url, callback=self.parse_detail)
	def parse_detail(self,response):
		rep = requests.get(response.url)
		soup = BeautifulSoup(rep.text)
		item = DianpingItem()
		#店名
		item['shop'] = soup.find('h1',attrs={'class':'shop-name'})
		
		temp = soup.find('div',attrs={'class':'breadcrumb'})
		dtemp = temp.find_all('a')
		#行政区
		item['district'] = dtemp[2]
		#街道
		item['street'] = dtemp[3]
		#菜系
		item['foodtype'] = dtemp[1]
		try:
			reviewitem = soup.find('div',attrs={'id':'comment'}).find('span').string
		#评论数
			item['comments_count'] = reviewitem.replace('(','').replace(')','')
		except:
			item['comments_count'] = 0
		#评论数大于100
		if int(item['comments_count'])>100:
			item['is_more_than_100'] = '是'
		else:
			item['is_more_than_100'] = '否'
			
		brief = soup.find('div',attrs={'class':'brief-info'}).find_all('span')
		#星级
		item['star_level'] = brief[0].get('title')
		#价格
		item['price'] = 
		#口味
		flavour = scrapy.Field()
		#环境
		environment = scrapy.Field()
		#服务
		service = scrapy.Field()
		#经度
		longitude = scrapy.Field()
		#纬度
		latitude = scrapy.Field()
		#综合评分
		overall_score = scrapy.Field()