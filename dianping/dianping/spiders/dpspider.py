# -*- coding: utf-8 -*-
import scrapy 
from scrapy import Request
from scrapy.spiders import Spider
from dianping.items import DianpingItem
from types import Prepare
from analyse import Addrdict
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import random
from bs4 import BeautifulSoup
from getgps import geocodeG
class DianpingSpider(Spider):
	
	name = 'test'
	
	def __init__(self,):
		self.headers=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
			{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
			{'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
			{'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
			{'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
			{'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
			{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
			{'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
			{'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
			{'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
			{'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
			{'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
			{'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]
		self.stdout = sys.stdout
		self.fo = open("mylog.log","w+")
		sys.stdout = self.fo
		self.base_url = 'http://www.dianping.com/shanghai/ch10/'
		self.p = Prepare()
		self.foodtypes = self.p.get_foodtypes()
		self.locations = self.p.get_districts()
		self.d = Addrdict()
		# self.d.set_pik_dict()
		self.xkz = self.d.xkz
		self.ug = self.d.ug
		self.count = 0
		# self.pik = self.d.pikdict
		print '####################init spider ok !!'
	def start_requests(self):
		for type in self.foodtypes:
			for lo in self.locations:
				url = self.base_url + str(type) + str(lo)
				choice = random.randint(0,12)
				yield scrapy.Request(url=url,headers = self.headers[choice],callback=self.next_page)
	def next_page(self,response):
		url = str(response.url)
		soup = BeautifulSoup(response.text)
		pages = soup.find('div',attrs={"class":'page'})
		print 'firsturl:',url
		if pages:
			temp = pages.find_all('a')
			page_num = temp[len(temp)-2]
			for i in range(1,int(page_num.get('title'))+1):
				page_url = url + 'p' + str(i)
				choice = random.randint(0,12)
				yield scrapy.Request(url = page_url ,headers = self.headers[choice],callback=self.parse_detail)
		else:
			choice = random.randint(0,12)
			yield scrapy.Request(url = url ,headers = self.headers[choice],callback=self.parse_detail)
	# def parse_url(self,response):
		# print '#########page url',str(response.url)
		# shoplist = response.xpath("//*[@data-click-name='shop_img_click']/@href")
		# for shop_url in shoplist:
			# print 'shop_url',shop_url.extract()
			# choice = random.randint(0,12)
			# yield scrapy.Request(url=str(shop_url.extract()), headers = self.headers[choice],callback=self.parse_detail)
	def parse_detail(self,response):
		print '========detail url',str(response.url)
		soup = BeautifulSoup(response.text)
		dis = soup.find_all('span',attrs={'itemprop':'title'})
		try:
			print dis[0].string,dis[1].string,dis[2].string,dis[3].string
		except:
			print 'error:',str(response.url)
		goal = soup.find('div',attrs={'id':'shop-all-list'})
		shoplist = goal.find_all('li')
		for shopitem in shoplist:
			item = DianpingItem()
			#编号
			item['No'] = self.count + 1
			temp = shopitem.find('div',attrs={'class':'operate J_operate Hide'}).find_all('a')
			#店名
			item['shop'] = temp[1].get('data-sname')
			#地址
			item['address'] = temp[1].get('data-address').strip()
			print item['shop'],':',item['address']
			if(len(dis)==4):
				#行政区
				item['district'] = dis[2].string
				#街道
				item['street'] = dis[3].string
				#菜系大类
				item['foodtype'] = dis[1].string
				#菜系小类
				item['foodtype2'] = dis[1].string
			else：
			#行政区
				item['district'] = dis[3].string
				#街道
				item['street'] = dis[4].string
				#菜系大类
				item['foodtype'] = dis[1].string
				#菜系小类
				item['foodtype2'] = dis[2].string
			temp2 = shopitem.find('div',attrs={'class':'txt'}).find('div',attrs={'class':'comment'})
			
			#星级
			item['star_level'] = temp2.find('span').get('title')
			print item['star_level']
			
			result = temp2.find('a',attrs={"data-click-name":'shop_iwant_review_click'}).find('b')
			#评论数
			if result:
				contents = result.contents
				count = ''
				for content in contents:
					if content.string:
						count += content.string
					else:
						index = content.get('class')[0]
						count +=self.ug[index]
				item['comments_count'] = count
			else:
				item['comments_count'] = 0
			print 'comments:',item['comments_count']
			#评论数大于100
			if int(item['comments_count'])>100:
				item['is_more_than_100'] = '是'
			else:
				item['is_more_than_100'] = '否'
			#价格
			price= temp2.find('a',attrs={"data-click-name":'shop_avgprice_click'}).find('b')
			if price:
				prices = price.contents
				p = ''
				for i in prices:
					if i.string:
						p += i.string
					else:
						index = i.get('class')[0]
						p += self.ug[index]
				item['price'] = p 
			else:
				item['price'] = '-未知'
			print 'price:',item['price']
			#价格区间
			if item['price'] == '-未知':
				item['price_range'] ='-未知'
			else if int(item['price']) <20:
				item['price_range'] ='0-20元'
			else if int(item['price']) >=20 and int(item['price'])<50:
				item['price_range'] ='20-50元'
			else if int(item['price']) >=50 and int(item['price'])<100:
				item['price_range'] ='50-100元'
			else if int(item['price']) >=100 and int(item['price'])<200:
				item['price_range'] ='100-200元'
			else if int(item['price']) >=200 and int(item['price'])<500:
				item['price_range'] ='200-500元'
			else if int(item['price']) >=500:
				item['price_range'] ='500元以上'
			temp3 = shopitem.find('div',attrs={'class':'txt'}).find('span',attrs={'class':'comment-list'})
			if temp3:
				try:
					assessments =temp3.find_all('span',recursive=False)
					alist = []
					for a in assessments:
						print 'a:',a
						tmp = ''
						for i in a.find('b').contents:
							if i.string:
								tmp += i.string
							else:
								index = i.get('class')[0]
								tmp += self.ug[index]
						alist.append(tmp)
					#口味
					item['flavour'] = alist[0]
					#环境
					item['environment'] = alist[1]
					#服务
					item['service'] = alist[2]
				except:
					print 'error2:' , str(response.url)
			else:
				#口味
				item['flavour'] = '暂无'
				#环境
				item['environment'] = '暂无'
				#服务
				item['service'] = '暂无'
			#综合评分
			if(item['flavour'] == '暂无'):
				item['overall_score'] = '暂无'
			else:
				item['overall_score'] = float(item['flavour'])*0.5+float(item['service'])*0.25+float(item['environment'])*0.25
			print item['overall_score']
			print item['service']
			print item['flavour']
			print item['environment']
			addr = '上海市'+ item['address']
			y,x = geocodeG(addr)
			print x,y
			#经度
			item['longitude'] = y
			#纬度
			item['latitude'] = x
			yield item

