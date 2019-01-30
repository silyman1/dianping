# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Addrdict(object):
	def __init__(self):
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
	def get_xkz(self,index):
		return self.xkz[index]
		
	def get_css(self,url):
		resp = requests.get(url,headers=self.headers)
		print 'get css sucessfully'
		return resp.content.decode('utf-8')
	def get_svg(self,url):
		resp = requests.get(url,headers=self.headers)
		print 'get svg sucessfully'
		return resp.text
	def set_pik_dict(self):
		
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
		print contents
		for node in M0nodes:
			s = node.get('d')
			flag = re.match('M0.*?(\d+).*?H600',s)
			if(ty==int(flag.group(1))):
				row  = int(node.get('id'))
				print 'find row,%d' % row
				break;
		goal = contents[row-1]
		print goal.string
		return (goal.string)[tx]
if __name__ == "__main__":
	d = Addrdict()
	i = raw_input("shuru:\n")
	if i.startswith('xkz'):
		s = d.get_xkz(i)
		print s
	else:
		s = d.get_pik(i)
		print s