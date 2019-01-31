#!/usr/bin/env python  
# encoding: utf-8 
import urllib
import json
from selenium import webdriver
import time
import re
from pyquery import PyQuery as pq
from pandas import DataFrame
import requests
def start():
   # #为打开列表页做准备
    driver = webdriver.Chrome()
    #url = "http://www.dianping.com/shanghai"
    url='http://www.dianping.com/shanghai/ch10/g34256r812'
    driver.get(url)
    time.sleep(20)
    #列表页的总页数
    page_number_total = int(driver.find_element_by_xpath('//div[@class="page"]//a[last()-1]').text)

    shop_name_list = []#存储店铺名称
    shop_address_list = []#存储店铺地址
    shop_telephone_list = []#存储店铺电话
    ne_list=[]#经纬度
    for page_number in range(1,page_number_total+1):
        shop_url_list = driver.find_elements_by_xpath('//div[@class="shop-list J_shop-list shop-all-list"]//li//div[@class="tit"]/a[@data-click-name="shop_title_click"]')
        for single_shop in shop_url_list:
            single_shop.click()
            driver.switch_to_window(driver.window_handles[-1])
            time.sleep(4)
            #店铺名称
            try:
                shop_name = driver.find_element_by_xpath('//h1[@class="shop-name"]').get_attribute('innerHTML')
            except:
                shop_name = " "
            #店铺地址
            try:
                shop_address = driver.find_element_by_xpath('//span[@id="address"]').get_attribute('innerHTML')
            except:
                shop_address = " "
            #店铺电话
            try:
                shop_telephone = driver.find_element_by_xpath('//p[@class="expand-info tel"]').get_attribute('innerHTML')
            except:
                shop_telephone = " "
            
            #获取css网页链接
            try:
                try:
                    csslink = driver.find_element_by_xpath('//*[@id="staticPage"]/link[2]').get_attribute('href')
                except:
                    csslink = driver.find_element_by_xpath('/html/head/link[10]').get_attribute('href')
            except:
                driver.close()
                driver.switch_to_window(driver.window_handles[-1])
                continue
                
            #处理消失的中文
            dict_svg_text,dict_css_x_y = css_get_zh(csslink)
            shop_Name = re.sub(re.compile(r'<a class(.+?)</a>', re.S), "", shop_name)
            shop_Address = css_decode_zh(dict_css_x_y, dict_svg_text, shop_address)
            
            #处理消失的数字
            dict_svg_text,dict_css_x_y = css_get_num(csslink)
            shop_Name = re.sub(re.compile(r'<a class(.+?)</a>', re.S), "", shop_name)
            shop_Address = css_decode_num(dict_css_x_y, dict_svg_text, shop_Address)
            shop_Telephone = css_decode_num(dict_css_x_y, dict_svg_text, shop_telephone)
            shop_Telephone = shop_Telephone.replace(" ","").replace("&nbsp;","  ")
            if u"无" in shop_Telephone:
                shop_Telephone = " "
            
            #存储下来
            print shop_Address
            ne=getapi(shop_Address.encode('utf-8'))
            ne_list.append(ne)
            shop_name_list.append(shop_Name)
            shop_address_list.append(shop_Address)
            shop_telephone_list.append(shop_Telephone)
            
            time.sleep(1)
            driver.close()
            driver.switch_to_window(driver.window_handles[-1])
            time.sleep(1)
        if page_number == page_number_total:
            break
        driver.find_element_by_xpath('//a[@class="next"]').click()
        
    driver.quit()

    df = DataFrame(
            {
                '店铺名称':shop_name_list,
                '店铺地址':shop_address_list,
                '店铺电话':shop_telephone_list,
                '经纬度':ne_list
            }
        )

    df.to_csv(
        "C://Users//CGD//Desktop//pinglun_.csv",encoding='utf_8_sig'
    )

# 1.1-获取svg汉字列表，以及样式字典
def css_get_zh(css_link):
    background_link = requests.get(css_link)
    svg_link = r'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/b17b46173817564bd630ef0191629fe9.svg'
    dict_avg_text = svg_text(svg_link)
    dict_css = css_dict(background_link.text)
    return dict_avg_text, dict_css

#1.2 获取svg数字列表，以及样式字典
def css_get_num(css_link):
    background_link = requests.get(css_link)
    svg_link = r'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/cdf9c1c10e53a0c40f5ff2cbbb9e4a2a.svg'
    dict_avg_text = svg_text(svg_link)
    dict_css = css_dict(background_link.text)
    return dict_avg_text, dict_css

# 2-获得svg字体库
def svg_text(url):
    html = requests.get(url)
    dict_svg = svg_dict(html.text)
    return dict_svg

# 3-得到我们想要的svg列表
def svg_dict(csv_html):
    svg_text_r = r'<text x="(.*?)" y="(.*?)">(.*?)</text>'
    svg_text_re = re.findall(svg_text_r, csv_html)
    dict_avg = []
    # 生成svg加密字体库字典
    for data in svg_text_re:
        dict_avg.append([data[1], list(data[2])])
    return dict_avg

# 4-从css样式网页获得我们想要的css样式字典
def css_dict(html):
    css_text_r = r'.(.*?){background:(.*?)px (.*?)px;}'
    css_text_re = re.findall(css_text_r, html)
    dict_css = {}
    for data in css_text_re:
        x = int(float(data[1])/-14)
        dict_css[data[0]] = (data[1], data[2], x, data[2])
    return dict_css

# 5.1 -实现还原汉字
def css_decode_zh(css_dict_text, csv_dict_text, pinglun_html):

    # 对文本源码进行处理
    pinglun_text = re.sub(re.compile(r'<a class(.+?)/a>', re.S), "", pinglun_html).replace('<e class="', ',').replace('">', ",").replace("</e>",'').replace(",</d>",'"></d>')
    pinglun_list = [x for x in pinglun_text.split(",") if x != '']
    
    pinglun_str = []
    for msg in pinglun_list:
        # 加密文字
        if msg in css_dict_text:
            # [x,y] css样式中background 的[x/14，y]
            x = int(css_dict_text[msg][2])
            y = -float(css_dict_text[msg][3])
            # 寻找background的y轴比svg<path>标签里的y轴小的第一个值对应的坐标就是<textPath>的href值
            for g in csv_dict_text:
                if y < int(g[0]):
                    pinglun_str.append(g[1][x])
                    break
        # 普通文字
        else:
            pinglun_str.append(msg.replace("\n", ""))
    str_pinglun = ""
    for x in pinglun_str:
        str_pinglun += x
    return str_pinglun

# 5.2 -实现还原数字
def css_decode_num(css_dict_text, csv_dict_text, pinglun_html):

    # 对文本源码进行处理
    pinglun_text = re.sub(re.compile(r'<span class(.+?)/span>', re.S), "", pinglun_html).replace('<d class="', ',').replace('">', ",").replace('</d>', "")
    pinglun_list = [x for x in pinglun_text.split(",") if x != '']
    
    pinglun_str = []
    for msg in pinglun_list:
        # 加密数字
        if msg in css_dict_text:
            # [x,y] css样式中background 的[x/14，y]
            x = int(css_dict_text[msg][2])
            y = -float(css_dict_text[msg][1])
            # 寻找background的y轴比svg<path>标签里的y轴小的第一个值对应的坐标就是<textPath>的href值
            for g in csv_dict_text:
                if y < int(g[0]):
                    pinglun_str.append(g[1][x])
                    break
        # 普通数字
        else:
            pinglun_str.append(msg.replace("\n", ""))
    str_pinglun = ""
    for x in pinglun_str:
        str_pinglun += x
    return str_pinglun
def getapi(addr):
    
    s=requests.session()
    
    data=urllib.quote('上海')
    add=urllib.quote(addr)
    url='http://restapi.amap.com/v3/geocode/geo?key=44004bce62f708e61df776b076bb1b92&address={0}&city={1}'.format(addr,data)
                      
    html=s.get(url).text
    json_data=json.loads(html)
    return json_data['geocodes'][0]['location']


if __name__ == '__main__':
    start()
