# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class Prepare(object):
	def __init__(self):
		self.foodtype = []
		self.districts = []
	
	def get_foodtypes(self)