import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
response = requests.get("http://www.dianping.com/shop/93738801")

f  = open("test.log",'w+')
f.write(response.text)

	i = raw_input("shuru:\n")
	if i.startswith('xkz'):
		s = d.get_xkz(i)
		print s
	else:
		s = d.get_pik(i)
		print s
