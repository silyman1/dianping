# -*- coding: utf-8 -*-
"""
date: Tue Nov 27 09:48:08 2018
python: Anaconda 3.6.5
author: kanade
email: kanade@blisst.cn
"""
import requests
import re

class DianPingSpider(object):
    '''
    获取商家信息
    '''
    def __init__(self, url='http://www.dianping.com/shop/586341'):
        html = self.get_index_html(url)
        css_html = self.get_css_html(html)
        # 数字密码本class属性的开头两个字母，比如kj
        numcb = re.search(r'id="reviewCount".*?>[\s\S]*?class="(\w\w)-\w{4}"', html).group(1)
        # 文字密码本class属性的开头两个字母
        charcb = re.search(r'id="address".*?>[\s\S]*?class="(\w\w)-\w{4}"', html).group(1)
        self.kjs = self.get_kjs(css_html, numcb)
        self.bis = self.get_bis(css_html, charcb)
              
    def get_index_html(self, url):
        '''
        获取初始网页
        '''
        headers = {
            'Host':'www.dianping.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.61 Safari/537.36'
         }
        resp = requests.get(url, headers=headers)
        print(resp.status_code)
        html = resp.text
        print(len(html))
        return html
        
    def get_css_html(self, html):
        '''
        获取css文件的内容
        '''
        # 从html中提取css文件的url
        regex = re.compile(r'(s3plus\.meituan\.net.*?)\"')
        css_url = re.search(regex, html).group(1)
        css_url = 'http://' + css_url
        # 得到css文件的内容
        resp = requests.get(css_url)
        css_html = resp.content.decode('utf-8')
        return css_html
        
    def get_kjs(self, css_html, numcb):
        '''
        获取kj开头的class属性对应显示的文字字典
        '''
        # 从css_html中提取kj的svg文件url
        regex = re.compile(r'\[class\^="%s-"\][\s\S]*?url\((.*?)\)'%numcb)
        svg_url = re.search(regex, css_html).group(1)
        if svg_url.startswith('//'):
            svg_url = 'http:' + svg_url
        # 得到svg文件内容
        resp = requests.get(svg_url)
        svg_html = resp.text
        # 从svg内容中提取10位数字
        number = re.search(r'\d{10}', svg_html).group()
        # 匹配出以kj-开头的class属性中的偏移量
        regex_kj = re.compile(r'\.(%s-\w{4})[\s\S]*?-(\d+)'%numcb)
        kjs = re.findall(regex_kj, css_html)
        # 根据偏移量排序
        kjs.sort(key=lambda x:int(x[1]))
        # 将class属性其真正显示的数字组成字典
        kjs = {i[0]:number[n] for n,i in enumerate(kjs)}
        
        return kjs
    
    def get_bis(self, css_html, charcb):
        '''
        获取bi开头的class属性真正显示的汉字
        '''
        # 提取相应的svg文件的url
        regex = re.compile(r'\[class\^="%s-"\][\s\S]*?url\((.*?)\)' % charcb)
        svg_url = re.search(regex, css_html).group(1)
        if svg_url.startswith('//'):
            svg_url = 'http:' + svg_url
        # 得到svg的内容
        resp = requests.get(svg_url)
        svg_html = resp.text
        # 提取svg文件中的所有文字信息
        regex = re.compile(r'<text[\s\S]*?>(\w+)<')
        content = regex.findall(svg_html)
        # 提取css_html中以bi-开头的class属性的偏移量
        regex = re.compile(r'(%s-\w{4})[\s\S]*?-(\d+)\.0px -(\d+)\.0px' % charcb)
        css = regex.findall(css_html)
        # 将偏移量转化为content内容的索引，不要问为什么，自己试试就知道了。
        # 规律而已，并将class属性和索引内容组成字典
        bis = {i[0]:content[int((int(i[2])-7)/30)][int(i[1])//14] for i in css}
        
        return bis
    
    

if __name__ == '__main__':
    dp = DianPingSpider()
    print(dp.bis)
    print(dp.kjs)
