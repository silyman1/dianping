# -*- coding: utf-8 -*-
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def geocodeG(address):
	par = {'address': address, 'key': '44004bce62f708e61df776b076bb1b92'}
	base = 'http://restapi.amap.com/v3/geocode/geo'
	response = requests.get(base, par)
	answer = response.json()
	print answer
	GPS=answer['geocodes'][0]['location'].split(",")
	return GPS[0],GPS[1]
if __name__ =="__main__":
	addr = '上海市康定路877号'
	y,x = geocodeG(addr)
	print x,y
	headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
		'host':'www.dianping.com',
		'Cookie':'showNav=#nav-tab|0|0; navCtgScroll=0; showNav=javascript:; navCtgScroll=100; _lxsdk_cuid=1689c87ecafc8-0ebc81f63e643b-5f6c3a73-c0000-1689c87ecafc8; _lxsdk=1689c87ecafc8-0ebc81f63e643b-5f6c3a73-c0000-1689c87ecafc8; _hc.v=aa4b3d4e-4be1-2a26-9965-3c1b3425853e.1548814381; cy=1; cye=shanghai; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; s_ViewType=10; _lxsdk_s=168ac74ab50-62c-58f-600%7C%7C288'
		}
	url = 'http://www.dianping.com/shanghai/ch10/g2887r812'
	fo = open('test.log','w+')
	sys.stdout = fo
	for i in range(20):
		rep = requests.get(url,headers=headers)
		print rep.status_code,rep.url


