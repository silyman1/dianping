#!/usr/bin/env python  
# encoding: utf-8 
import urllib
from selenium import webdriver
import time
import re
from pyquery import PyQuery as pq
from pandas import DataFrame
import requests
import json
def start():
    # #为打开列表页做准备
    driver = webdriver.Chrome()
    #url = "http://www.dianping.com/shanghai"
    url='http://www.dianping.com/shanghai/ch10/g34256r812'
    driver.get(url)
    '''
    #time.sleep(1)
    driver.find_element_by_xpath(r'//input[@id="J-search-input"]').send_keys("一只酸奶牛")#输入搜索内容
    #time.sleep(2)
    driver.find_element_by_xpath(r'//a[@id="J-all-btn"]').click()
    #time.sleep(1)
    driver.switch_to_window(driver.window_handles[-1])    '''
    

    #列表页的总页数
    page_number_total = int(driver.find_element_by_xpath('//div[@class="page"]//a[last()-1]').text)
    shop_name_list = []#存储店铺名称
    shop_address_list = []#存储店铺地址
    shop_telephone_list = []#存储店铺电话
    comment_list=[]#存储口味
    huanj_list=[]#环境评分
    seve_list=[]#服务分
    star_list=[]
    reviw_list=[]#评论总数分
    avg_list=[]#价格
    count_list=[]#价格
    pl_list=[]#评论区间
    are_list=[]
    street_list=[]
    ne_list=[]#经纬度
    for page_number in range(1,page_number_total+1):
        shop_url_list = driver.find_elements_by_xpath('//div[@class="shop-list J_shop-list shop-all-list"]//li//div[@class="tit"]/a[@data-click-name="shop_title_click"]')
        for single_shop in shop_url_list:
            single_shop.click()
            driver.switch_to_window(driver.window_handles[-1])
            #店铺名称
            html=driver.page_source
            try:
                shop_name = driver.find_element_by_xpath('//h1[@class="shop-name"]').get_attribute('innerHTML')
            except:
                shop_name = " "
            #店铺地址
            try:
                shop_address = driver.find_element_by_xpath('//span[@id="address"]').get_attribute('innerHTML')
            except:
                shop_address = " "
            try:#所属区域
                are = driver.find_element_by_xpath('//*[@id="body"]/div/div[1]/a[3]').get_attribute('innerHTML')
                #print are
            except:
                are = " "
            try:#所属街道
                street = driver.find_element_by_xpath('//*[@id="body"]/div/div[1]/a[4]').get_attribute('innerHTML')
                #print street
            except:
                street = " "
                
            #店铺电话
            try:
                shop_telephone = driver.find_element_by_xpath('//p[@class="expand-info tel"]').get_attribute('innerHTML')
            except:
                shop_telephone = " "
              # 口味
            try:
                comment = driver.find_element_by_xpath('//*[@id="comment_score"]/span[1]').get_attribute('innerHTML')
            except:
                comment = " "
            # 环境
            try:
                huanj = driver.find_element_by_xpath('//*[@id="comment_score"]/span[2]').get_attribute('innerHTML')
            except:
                huanj = " "
            # 服务
            try:
                seve = driver.find_element_by_xpath('//*[@id="comment_score"]/span[3]').get_attribute('innerHTML')
            except:
                seve = " "
            # 星级
            try:
                star = re.findall(r'<span title="(.+?)" class',html,re.S)[0]
                #print star
            except:
                star = u"无星级信息"
            # 评论数量
            time.sleep(1)
            try:
                review_count = driver.find_element_by_xpath('//*[@id="reviewCount"]').get_attribute('innerHTML')
            except:
                review_count = " "
            # 价格
            try:
                AVG = driver.find_element_by_xpath('//*[@id="avgPriceTitle"]').get_attribute('innerHTML')
            except:
                AVG = " "           
            
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
            dict_svg_text, list_svg_y, dict_css_x_y = css_get_zh(csslink)
            shop_Name = re.sub(re.compile(r'<a class(.+?)</a>', re.S), "", shop_name)#名称
            shop_Address = css_decode_zh(dict_css_x_y, dict_svg_text,list_svg_y,shop_address)#地址
            comment=css_decode_zh(dict_css_x_y, dict_svg_text,list_svg_y,comment)#口味
            huanj=css_decode_zh(dict_css_x_y, dict_svg_text,list_svg_y,huanj)#环境评分
            seve=css_decode_zh(dict_css_x_y, dict_svg_text,list_svg_y,seve)#服务评分
            
            
            #review_count=css_decode_zh(dict_css_x_y, dict_svg_text,list_svg_y,review_count)#评论数量
            AVG=css_decode_zh(dict_css_x_y, dict_svg_text,list_svg_y,AVG)#人均消费
            
            
            #处理消失的数字
            dict_svg_text,dict_css_x_y = css_get_num(csslink)
            shop_Address = css_decode_num(dict_css_x_y, dict_svg_text, shop_Address)
            shop_Telephone = css_decode_num(dict_css_x_y, dict_svg_text, shop_telephone)
            
            shop_Telephone = shop_Telephone.replace(" ","").replace("&nbsp;","  ")
            comment=css_decode_num(dict_css_x_y, dict_svg_text, comment)
            huanj=css_decode_num(dict_css_x_y, dict_svg_text,huanj)#环境评分
            seve=css_decode_num(dict_css_x_y, dict_svg_text,seve)#服务评分
            #star=re.sub('\s','',star)#星级
            review_count=css_decode_num(dict_css_x_y, dict_svg_text,review_count)#评论数量
            #print review_count
            AVG=css_decode_num(dict_css_x_y, dict_svg_text,AVG)#人均消费
            #print re.findall('\d+',review_count)
            review_count_num=int(re.findall('\d+',review_count)[0])
            #print review_count_num
            
            if review_count_num>100:
                count=u'是'
            else:
                count=u'否'               
            pl_list.append(count)#评论区间            
            try:
                AVG_num=int(re.findall('\d+',AVG)[0])
                #print AVG_num
                if 100<AVG_num<=200:
                    count1=u'100-200元'
                    count_list.append(count1)#价格qujian
                elif 0<AVG_num<=100:
                    count1=u'0-100元'
                    count_list.append(count1)#价格qujian
                elif 200<AVG_num<=500:
                    count1=u'200-500元'
                    count_list.append(count1)#价格qujian
                elif 500<AVG_num<=1000:
                    count1=u'500-1000元'
                    count_list.append(count1)#价格qujian
            except:                
                count_list.append(AVG)
            #print count_list
            #print count1
                
            
            
            
            #print comment
            #print huanj
            #print seve
            
            if u"无" in shop_Telephone:
                shop_Telephone = " "
            
            
            #print star
            #存储下来
            print shop_Address
            ne=getapi(shop_Address.encode('utf-8'))
            ne_list.append(ne)
            shop_name_list.append(shop_Name)
            shop_address_list.append(shop_Address)
            shop_telephone_list.append(shop_Telephone)
            comment_list.append(comment)#存储口味
            huanj_list.append(huanj)#环境评分
            seve_list.append(seve)#服务分
            star_list.append(star)
            reviw_list.append(review_count)#评论总数
            avg_list.append(AVG)#价格
            are_list.append(are)
            street_list.append(street)
            
            
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
                '行政区':are_list,
                '街道':street_list,
                '店铺地址':shop_address_list,
                #'店铺电话':shop_telephone_list,
                '评论数量':reviw_list,
                '评论数>100':pl_list,
                '价格':avg_list,
                '价格区间':count_list,
                '星级':star_list,
                '口味':comment_list,
                '环境':huanj_list,
                '服务':seve_list,
                '经纬度':ne_list
            }
        )
    

    df.to_csv(
        r"C:\Users\hacker\Desktop\pinglun_.csv",encoding='utf_8_sig'
    )

####这里的函数用来对数字进行处理


#1 获取svg数字列表，以及样式字典
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


# 5-实现还原数字
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



#########___________________这是分界线________________#########
####这下面的函数用来对文本的处理

# # 1-评论隐含部分字体css样式, 获取svg链接，获取加密汉字background，参数已调整
def css_get_zh(csslink):
    css_link = csslink
    background_link = requests.get(css_link)
    svg_link = r'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/b17b46173817564bd630ef0191629fe9.svg'
    """
    svg_text() 方法：请求svg字库，并抓取加密字
    dict_svg_text: svg整个加密字库，以字典形式返回
    list_svg_y：svg背景中的<path>标签里的[x,y]坐标轴，以[x,y]形式返回
    """
    dict_avg_text, list_svg_y = svg_text_zh(svg_link)
    """
    css_dict() 方法：生成css样式中background的样式库
    dict_css: 返回css字典样式
    """
    dict_css = css_dict_zh(background_link.text)
    return dict_avg_text, list_svg_y, dict_css
    #dict_avg_text---{1 : 思肿藏楼迅池贼拜在缠敬种棍诉博鼓偶还演棋扑覆沟发}
    #list_svg_y----[[1,33],[2,80],...]<path xmlns="http://www.w3.org/2000/svg" id="1" d="M0 33 H600"/>


# 2-字体库链接,参数已调整
def svg_text_zh(url):
    html = requests.get(url)
    dict_svg, list_y = svg_dict_zh(html.text)
    return dict_svg, list_y


# 3-生成svg字库字典，与2有关。参数不用调整
def svg_dict_zh(csv_html):
    svg_text_r = r'<textPath xlink:href="(.*?)" textLength="(.*?)">(.*?)</textPath>'
    svg_text_re = re.findall(svg_text_r, csv_html)
    dict_avg = {}
    # 生成svg加密字体库字典
    for data in svg_text_re:
        dict_avg[data[0].replace("#", "")] = list(data[2])
    """
    重点：http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/74d63812e5b327d850ab4a8782833d47.svg
        svg <path> 标签里内容对应css样式中background的y轴参数，小于关系，
        如果css样式中的background的y参数小于 svg_y_re 集合中最小的数，则向上取y轴，('18', 'M0', '748', 'H600')，
        如.gqi4j {background: -98.0px -745.0px;} 中的y-745，取正数745，小于748，则对应加密字库实际y轴为748，对应的18就是<textPath>中的x轴
    """
    svg_y_r = r'<path id="(.*?)" d="(.*?) (.*?) (.*?)"/>'
    svg_y_re = re.findall(svg_y_r, csv_html)
    list_y = []
    # 存储('18', 'M0', '748', 'H600') eg:(x坐标，未知，y坐标，未知)
    for data in svg_y_re:
        list_y.append([data[0], data[2]])
    return dict_avg, list_y


# 4-生成css字库字典,与1有关，参数已调整
def css_dict_zh(html):
    css_text_r = r'.(.*?){background:(.*?)px (.*?)px;}'
    css_text_re = re.findall(css_text_r, html)
    dict_css = {}
    for data in css_text_re:
        """
        加密字库.gqi4j {background: -98.0px -745.0px;}与svg文件对应关系，x/14，就是svg文件加密字体下标
        y，原样返回，需要在svg函数中做处理
        """
        x = int(float(data[1])/-14)
        """
        字典参数：{css参数名：(background-x,background-y,background-x/14,background-y)}
        """
        dict_css[data[0]] = (data[1], data[2], x, data[2])
    return dict_css
    #rjmgf8{background:-266.0px -1607.0px;}
    #{rjmgf8: (-266,-1607,19,-1607)}

# 5-
def css_decode_zh(css_html, svg_dict, svg_list, pinglun_html):
    """
    dict_css_x_y, dict_svg_text, list_svg_y, pinglun
    :param css_html: css 的HTML源码{rjmgf8: (-266,-1607,19,-1607)}
    :param svg_dict: svg加密字库的字典{1 : 思肿藏楼迅池贼拜在缠敬种棍诉博鼓偶还演棋扑覆沟发}
    :param svg_list: svg加密字库对应的坐标数组[x, y][[1,33],[2,80]
    :param pinglun_html: 评论的HTML源码，对应0-详情页的评论，在此处理
    :return: 最终合成的评论
    """
    css_dict_text = css_html
    csv_dict_text, csv_dict_list = svg_dict, svg_list
    # 处理评论源码中的span标签，生成字典key
    pinglun_text = re.sub(re.compile(r'<a class(.+?)/a>', re.S), "", pinglun_html).replace('<e class="', ',').replace('">', ",").replace("</e>",'').replace(",</d>",'"></d>')
    pinglun_list = [x for x in pinglun_text.split(",") if x != '']
    pinglun_str = []
    for msg in pinglun_list:
        # 如果有加密标签
        if msg in css_dict_text:
            # 参数说明：[x,y] css样式中background 的[x/14，y]
            x = int(css_dict_text[msg][2])
            y = -float(css_dict_text[msg][3])
            # 寻找background的y轴比svg<path>标签里的y轴小的第一个值对应的坐标就是<textPath>的href值
            for g in csv_dict_list:
                if y <= int(g[1]):
                    # print(g)
                    # print(csv_dict_text[g[0]][x])
                    pinglun_str.append(csv_dict_text[g[0]][x])
                    break
        # 没有加密标签
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
