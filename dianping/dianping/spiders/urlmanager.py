# -*- coding=utf-8 -*-
import cPickle
import hashlib

class UrlManager(object):
	def __init__(self):
		self.new_urls=self.get_urls_process_status(r'new_urls.txt')
		self.crawled_urls=self.get_urls_process_status(r'crawled_urls.txt')

	def get_urls_process_status(self,path):
		print '[+]get processing_status......'
		try:
			with open(path,'rb') as f:
				status = cPickle.load(f)
				return status
		except:
			print '%s first in use,create it'%path
			return set()
	def save_urls_process_status(self,data,path):
		print '[+]save processing_status......'
		try:
			with open(path,'wb') as f:
				cPickle.dump(data, f)
		except:
			print '%s save processing_status error'%path
	def new_urls_size(self):
		return len(self.new_urls)

	def crawled_urls_size(self):
		return len(self.crawled_urls)

	def has_new_url(self):
		return self.new_urls_size()!=0

	def get_new_url(self):
		new_url=self.new_urls.pop()
		m = hashlib.md5()
		m.update(new_url)
		self.crawled_urls.add(m.hexdigest()[8:-8])
		#print 'get new url %s'%new_url
		return new_url

	def add_new_url(self,url):
		if url is None or len(url)==0:
			print u'add empty url.......'
			return 
		m = hashlib.md5()
		m.update(url)

		if url in self.new_urls or m.hexdigest()[8:-8] in self.crawled_urls:
			print u'%s is a repeating url'%url
			return
		else:
			self.new_urls.add(url)
			#print 'adding new url %s'%url
	def add_new_urls(self,urls):
		if urls is None or len(urls)==0:
			print u'add empty urls.......'
			return 
		for url in urls:
			self.add_new_url(url)
