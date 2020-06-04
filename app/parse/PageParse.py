#!/usr/bin/python3
# -*- coding: utf-8 -*-

from config.ConfigUtils import ConfigUtils
from selenium import webdriver
from bs4 import BeautifulSoup

import json
import time

'''
20200521 licl created

解析器,包含页面中url解析提取，内容解析提取

安装模块命令：
pip install selenium
pip install bs4

'''

'''
寻找字符串下标
'''
def find_n_sub_str(src, sub, pos, start):
    index = src.find(sub, start)
    if index != -1 and pos > 0:
        return find_n_sub_str(src, sub, pos - 1, index + 1)
    return index


class PageParse():

    '''
     读取主页面包含子链接列表的部分
     支持分页
     conf_obj:当前主页面配置的配置对象

     注意事项：使用webdriver需要安装chrome浏览器驱动
     可以参考：https://www.cnblogs.com/wenjing2019/p/11957346.html
    '''
    def parse_main_page(self, conf_obj):
        #获取配置信息
        url = conf_obj['down_load_url']
        open_html_time = conf_obj['open_html_time']
        down_load_list_begin = conf_obj['down_load_list_begin']
        down_load_list_end = conf_obj['down_load_list_end']
        down_load_list_end_num = conf_obj['down_load_list_end_num']
        next_page_num = conf_obj['next_page_num']
        next_page = conf_obj['next_page']
        next_page_time = conf_obj['next_page_time']
        #前缀
        self.relative_path_prefix =  conf_obj['relative_path_prefix']
        #主网站
        self.main_path = conf_obj['main_path']
        #获取逻辑
        options = webdriver.ChromeOptions()
        #print(json.dumps(options.__dict__))
        browser = webdriver.Chrome(chrome_options=options)
        browser.maximize_window()
        browser.get(url)
        #第一页
        time.sleep(int(open_html_time))
        main = browser.page_source
        begin = main.find(down_load_list_begin)
        end = find_n_sub_str(main, down_load_list_end, int(down_load_list_end_num), begin)
        list = main[begin:end]
        #翻页
        if int(next_page_num )>0:
            next_page_split = next_page.split(",")
            for count in range( int(next_page_num )):
                    if next_page_split[0] == 'class':
                       browser.find_element_by_class_name(next_page_split[1]).click()
                    elif next_page_split[0] == 'id':
                        browser.find_element_by_id(next_page_split[1]).click()
                    elif next_page_split[0] == 'name':
                        browser.find_element_by_name(next_page_split[1]).click()
                    else :
                        print("翻页配置类型错误，类型范围clss id name中一中")

                    time.sleep(int(next_page_time))
                    main = browser.page_source
                    begin = main.find(down_load_list_begin)
                    end = find_n_sub_str(main, down_load_list_end, int(down_load_list_end_num), begin)
                    list = list +main[begin:end]
        browser.quit()
        self.urls_list_a = self.parse_all_link(list)
        return self.parse_full_urls(self.urls_list_a)
    '''
    解析传入的字符串中的所有a标签
    '''
    def parse_all_link(self, main_urls_str):
        soup = BeautifulSoup(main_urls_str, 'html.parser')
        all_soup = soup.find_all("a")
        return all_soup

    '''
    处理所有a标签，将标签的访问路径规范并存储到url管理器
    '''
    def parse_full_urls(self, urls_list_a):
        page_document_list=[]
        full_urls_set = set()
        if len(urls_list_a) == 0:
            print("未获取到连接列表")
            return
        for link in urls_list_a:
            #获取标题
            title = link.get("title")
            #处理无效标题
            if title is not None and title != 0 and len(title) < 5:
                print("忽略  ： " + title)
                continue;
            # 获取链接
            href = link.get("href")
            if href is None:
                continue
            '''解析链接为绝对路径'''
            #处理不规则的连接
            if href[0:2] == "//":
                href = href[2:]
            #判断是否已经是全路径了，根据判断结果处理
            if not self._is_relative_path(href):
                #不做处理
                pass
            if href[0:3] == "www":
                href = "http://" + href
            href = href.replace(self.relative_path_prefix, "", 1)
            href = self.main_path + "/" + href
            #print(href)
            item_dic = {'title':title, 'href':href}

            page_document_list.append(item_dic)

            full_urls_set.add(href)
        return full_urls_set,page_document_list

    '''
        解析html文件中html地址,判断是否是绝对路径

        例如 href="../../zdjs/stzgg/201709/e6133a882d9c463d945f434b5d63cc3c.shtml"
        应解析成 http://srcurl/zdjs/stzgg/201709/e6133a882d9c463d945f434b5d63cc3c.shtml
    '''
    def _is_relative_path(self, href):
        if href.find('http://') == 0:
            return False
        elif href.find('https://') == 0:
            return False
        else:
            return True
    '''
        检查链接类型是文件还是html链接
        返回值：
        文件类型：file
        html链接：html
    '''
    def check_url_type(self,url):
        #链接类型
        type = ''
        index = url.rfind('.')
        fileName = url[index:]
        if fileName.lower() == ".pdf" or fileName.lower() == ".doc" or fileName.lower() == ".docx":
            type = 'file'

        if type != 'file':
            url = url.lower()
            if (not url.find('www.') == 0) or (not url.find('http') == 0)  or (not url.find('https') == 0):
                type = 'html'
        return type