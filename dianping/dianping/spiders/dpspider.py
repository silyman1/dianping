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
from urlmanager import  UrlManager
# 在spider中时在方法里直接写

# self.crawler.engine.close_spider(self, 'cookie失效关闭爬虫')
 
# 在pipeline和downloaderMiddlewares里

# spider.crawler.engine.close_spider(spider, '没有新数据关闭爬虫')
class DianpingSpider(Spider):
	
	name = 'test'
	
	def __init__(self,):
		self.headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
		'host':'www.dianping.com',
		'Cookie':'showNav=#nav-tab|0|0; navCtgScroll=0; showNav=javascript:; navCtgScroll=100; _lxsdk_cuid=1689c87ecafc8-0ebc81f63e643b-5f6c3a73-c0000-1689c87ecafc8; _lxsdk=1689c87ecafc8-0ebc81f63e643b-5f6c3a73-c0000-1689c87ecafc8; _hc.v=aa4b3d4e-4be1-2a26-9965-3c1b3425853e.1548814381; cy=1; cye=shanghai; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; s_ViewType=10; _lxsdk_s=168ac74ab50-62c-58f-600%7C%7C288'
		}
		self.stdout = sys.stdout
		self.fo = open("mylog.log","w+")
		sys.stdout = self.fo
		self.base_url = 'http://www.dianping.com/shanghai/ch10/'
		self.p = Prepare()
		# self.foodtypes = self.p.get_foodtypes()
		# self.locations = self.p.get_districts()
		self.d = Addrdict()
		self.curkey = self.d.get_ge
		self.scoremap = self.d.get_score
		# self.d.set_pik_dict()
		self.count = 0
		self.urlmanager = UrlManager()
		# self.pik = self.d.pikdict
		print '####################init spider ok !!'
	def start_requests(self):
		if self.urlmanager.has_new_url()==False:
			ulist = self.p.get_urls()
			print '####################get ulist ok !!'
			self.urlmanager.add_new_urls(ulist)
			self.urlmanager.save_urls_process_status(urlmanager.new_urls,r'new_urls.txt')
			self.urlmanager.save_urls_process_status(urlmanager.crawled_urls,r'crawled_urls.txt')
		while self.urlmanager.has_new_url():
			new_url = self.urlmanager.get_new_url()
		# for type in self.foodtypes:
			# for lo in self.locations:
				# url = self.base_url + str(type) + str(lo)
				# choice = random.randint(0,12)
			yield scrapy.Request(url=new_url,headers = self.headers,callback=self.next_page)
	def next_page(self,response):
		url = str(response.url)
		soup = BeautifulSoup(response.text)
		pages = soup.find('div',attrs={"class":'page'})
		print 'firsturl:',url,'count:',self.count
		if url == '':
			self.urlmanager.save_urls_process_status(urlmanager.new_urls,r'new_urls.txt')
			self.urlmanager.save_urls_process_status(urlmanager.crawled_urls,r'crawled_urls.txt')
			self.crawler.engine.close_spider(self, u'出现验证码,关闭爬虫')
		if pages:
			temp = pages.find_all('a')
			page_num = temp[len(temp)-2]
			for i in range(1,int(page_num.get('title'))+1):
				page_url = url + 'p' + str(i)
				# choice = random.randint(0,12)
				yield scrapy.Request(url = page_url ,headers = self.headers,callback=self.parse_detail)
		else:
			# choice = random.randint(0,12)
			yield scrapy.Request(url = url ,headers = self.headers,callback=self.parse_detail)
	# def parse_url(self,response):
		# print '#########page url',str(response.url)
		# shoplist = response.xpath("//*[@data-click-name='shop_img_click']/@href")
		# for shop_url in shoplist:
			# print 'shop_url',shop_url.extract()
			# choice = random.randint(0,12)
			# yield scrapy.Request(url=str(shop_url.extract()), headers = self.headers[choice],callback=self.parse_detail)
	def parse_detail(self,response):
		print '========detail url',str(response.url)
		if response.url == '':
			self.urlmanager.save_urls_process_status(urlmanager.new_urls,r'new_urls.txt')
			self.urlmanager.save_urls_process_status(urlmanager.crawled_urls,r'crawled_urls.txt')
			self.crawler.engine.close_spider(self, u'出现验证码,关闭爬虫')
		if response.status != 200:
			fx =open("403.txt",'a+')
			fx.write(str(response.url))
			fx.write(response.status)
			fx.close()
			return
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
			self.count +=1
			item['No'] = self.count
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
			else:
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
			#评分
			item['score'] = self.scoremap(item['star_level'])
			print 'score:',item['score']
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
						if index.startswith('ug'):
							self.curkey =self.d.get_ug
						elif index.startswith('ge'):
							self.curkey = self.d.get_ge
						count +=self.curkey(index)
				item['comments_count'] = count
			else:
				item['comments_count'] = 0
			print 'comments:',item['comments_count']
			#评论数大于100
			if int(item['comments_count'])>100:
				item['is_more_than_100'] = u'是'
			else:
				item['is_more_than_100'] = u'否'
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
						p += self.curkey(index)
				item['price'] = p.replace('￥','') 
			else:
				item['price'] = u'未知'
			print 'price:',item['price']
			#价格区间
			print(type(item['price']))
			if item['price'] == u'未知':
				item['price_range'] =u'未知'
			elif int(item['price']) <20:
				item['price_range'] ='0-20元'
			elif int(item['price']) >=20 and int(item['price'])<50:
				item['price_range'] ='20-50元'
			elif int(item['price']) >=50 and int(item['price'])<100:
				item['price_range'] ='50-100元'
			elif int(item['price']) >=100 and int(item['price'])<200:
				item['price_range'] ='100-200元'
			elif int(item['price']) >=200 and int(item['price'])<500:
				item['price_range'] ='200-500元'
			elif int(item['price']) >=500:
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
								tmp += self.curkey(index)
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

