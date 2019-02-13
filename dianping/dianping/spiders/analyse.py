# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Addrdict(object):
	def __init__(self):
		self.pikdict ={}
		self.headers = {
            'Host':'s3plus.meituan.net',
            'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; Chitanda/Akari) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 MicroMessenger/6.0.0.58_r884092.501 NetType/WIFI'
         }
		self.xkz ={
				'xkzvx4':'0',
				'1':'1',
				'xkzt88':'2',
				'xkzy8j':'3',
				'xkztud':'4',
				'xkzor4':'5',
				'xkz632':'6',
				'xkzt2i':'7',
				'xkzolq':'8',
				'xkzols':'9',
		 }
		self.ug ={
				'ugmab':'0',
				'1':'1',
				'ugevc':'2',
				'ug5y2':'3',
				'ugtzu':'4',
				'ugng0':'5',
				'ugjff':'6',
				'ugf6b':'7',
				'ugi45':'8',
				'ug636':'9',
		 }
		self.ge ={
				'gedy0':'0',
				'1':'1',
				'get03':'2',
				'ge83g':'3',
				'ge04l':'4',
				'geaqa':'5',
				'gesbd':'6',
				'ge6d7':'7',
				'geg39':'8',
				'gevd8':'9',
		 }
		self.qxm ={
				'qxmaao':'0',
				'1':'1',
				'qxmu1c':'2',
				'qxmw2q':'3',
				'qxmac4':'4',
				'qxm98y':'5',
				'qxmi1f':'6',
				'qxmubb':'7',
				'qxmwgt':'8',
				'qxmidt':'9',
		 }
		self.ktg ={
				'ktguvx':'0',
				'1':'1',
				'ktg2uh':'2',
				'ktgbl7':'3',
				'ktgeqv':'4',
				'ktgh3y':'5',
				'ktgd4m':'6',
				'ktgt0y':'7',
				'ktgifc':'8',
				'ktgn2z':'9',
		 }
		self.zrr ={
				'zrr1gs':'0',
				'1':'1',
				'zrriac':'2',
				'zrrxjn':'3',
				'zrrwn3':'4',
				'zrr0t1':'5',
				'zrrfgo':'6',
				'zrrzoz':'7',
				'zrre7q':'8',
				'zrrzye':'9',
		 }
		self.uci ={
				'ucizs2':'0',
				'1':'1',
				'uci2fr':'2',
				'uci6p6':'3',
				'uci0ye':'4',
				'uciitc':'5',
				'ucivbx':'6',
				'ucivi8':'7',
				'ucivkr':'8',
				'ucikwr':'9',
		 }
		self.ws ={
				'wsl4p':'0',
				'1':'1',
				'wsn4d':'2',
				'wsu2p':'3',
				'ws1x1':'4',
				'ws74j':'5',
				'ws0w8':'6',
				'wsfd0':'7',
				'wsx2x':'8',
				'ws18h':'9',
		 }
		self.pld ={
				'pldnfy':'0',
				'1':'1',
				'pldw64':'2',
				'pldfit':'3',
				'pldo3s':'4',
				'pldpa8':'5',
				'pld10m':'6',
				'pldu6k':'7',
				'pldvp9':'8',
				'pld30i':'9',
		 }
		self.wqb ={
				'wqbh3o':'0',
				'1':'1',
				'wqbss9':'2',
				'wqb4oe':'3',
				'wqbmwx':'4',
				'wqbkfn':'5',
				'wqbj9l':'6',
				'wqblox':'7',
				'wqbp4h':'8',
				'wqb6w3':'9',
		 }
		self.dw ={
				'dwzwj':'0',
				'1':'1',
				'dwaon':'2',
				'dwhdq':'3',
				'dwq7w':'4',
				'dw8n3':'5',
				'dw7ci':'6',
				'dwxew':'7',
				'dw2j3':'8',
				'dwzib':'9',
		 }
		self.scoremap = {
					'5':'五星商户',
					'4':'四星商户',
					'3':'三星商户',
					'2':'二星商户',
					'1':'一星商户',
					'4.5':'准五星商户',
					'3.5':'准四星商户',
					'2.5':'准三星商户',
					'1.5':'准二星商户',
					'0.5':'准一星商户',
					'0':'该商户暂无星级',
					}
	def get_score(self,index):
		for key,value in self.scoremap.items():
			if value==index:
				return key
		return u'无'
	def get_ws(self,index):
		return self.ws[index]
	def get_zrr(self,index):
		return self.zrr[index]
	def get_wqb(self,index):
		return self.wqb[index]
	def get_pld(self,index):
		return self.pld[index]
	def get_xkz(self,index):
		return self.xkz[index]
	def get_uci(self,index):
		return self.uci[index]
	def get_ktg(self,index):
		return self.ktg[index]
	def get_qxm(self,index):
		return self.qxm[index]
	def get_ug(self,index):
		return self.ug[index]
	def get_ge(self,index):
		return self.ge[index]
	def get_dw(self,index):
		return self.dw[index]
	def get_css(self,url):
		resp = requests.get(url,headers=self.headers)
		print 'get css sucessfully'
		return resp.content.decode('utf-8')
	def get_svg(self,url):
		resp = requests.get(url,headers=self.headers)
		print 'get svg sucessfully'
		return resp.text
	def set_pik_dict(self):
		url = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/4fb494446f78aaedb88026ae33420b94.css'
		css_html = self.get_css(url)
		f  = open("test.log",'w+')
		f.write(css_html)
		regex = re.compile('(pik.*?){background:-(\d+)\.0px.*?-(\d+)\.0px')
		results = re.findall(regex,css_html)
		url2 = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/9dd500a7af53417f1b65c7a65b6c25ff.svg'
		svg_html = self.get_svg(url2)
		soup = BeautifulSoup(svg_html,'lxml')
		M0nodes = soup.find_all('path')
		contents = soup.find_all('textpath')
		for result in results:
			index = result[0]
			print index,result[1],result[2]
			x = result[1]
			y = result[2]
			tx = int(x)/14
			ty = int(y)+23
			for node in M0nodes:
				s = node.get('d')
				flag = re.match('M0.*?(\d+).*?H600',s)
				if(ty==int(flag.group(1))):
					row  = int(node.get('id'))
					print 'find row,%d' % row
					break;
			goal = contents[row-1]
			print (goal.string)[tx]
			self.pikdict[index] = (goal.string)[tx]
		print self.pikdict['pikbzp']
	def get_pik(self,index):
		url = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/4fb494446f78aaedb88026ae33420b94.css'
		css_html = self.get_css(url)
		f  = open("test.log",'w+')
		f.write(css_html)
		regex = re.compile('%s{background:-(\d+)\.0px.*?-(\d+)\.0px' % index)
		results = re.search(regex,css_html)
		x = results.group(1)
		y = results.group(2)
		print 'x:',x,'y:',y
		tx = int(x)/14
		ty = int(y)+23
		
		url2 = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/9dd500a7af53417f1b65c7a65b6c25ff.svg'
		svg_html = self.get_svg(url2)
		f  = open("test.log",'w+')
		f.write(svg_html)
		soup = BeautifulSoup(svg_html,'lxml')
		M0nodes = soup.find_all('path')
		contents = soup.find_all('textpath')
		for node in M0nodes:
			s = node.get('d')
			flag = re.match('M0.*?(\d+).*?H600',s)
			if(ty==int(flag.group(1))):
				row  = int(node.get('id'))
				print 'find row,%d' % row
				break;
		goal = contents[row-1]
		return (goal.string)[tx]
if __name__ == "__main__":
	d = Addrdict()
	d.set_pik_dict()
	