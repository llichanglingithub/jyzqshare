#!/usr/bin/python3
# -*- coding: utf-8 -*-

import traceback
import urllib
import urllib.request
import datetime
import os
import chardet
from bs4 import BeautifulSoup
from parse.PageParse import PageParse

'''
20200521 licl created

下载器
'''

class Downloader():

    #构造器
    def __init__(self, conf_obj):
        self.conf_obj = conf_obj

    '''
        下载附件
        url: 附件地址
        down_load_dir: 存放路径
        title:附件名称
        create_dir:是否创建子目录 1：表示创建  0：表示不创建
    '''
    def down_load_attach(self, url, down_load_dir, title,create_dir):
        # 存放目录不存在则创建目录
        date = datetime.datetime.now().strftime('%Y%m%d')
        save_dir = ''
        if create_dir == '1':
            save_dir = down_load_dir + "\\" + date + '\\'+ title
        else:
            save_dir = down_load_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        index = url.rfind('/')
        file_Name = url[index + 1:]
        encode_file_Name = file_Name;
        # 如果文件的url是中文encode过的，则跳过
        # url路径包括中文这需要encode 改url
        # encode过的url如/main/files/2018/01/22/D%E5%BF%83%E5%88%87%E6%8D%A22018%E5%B9%B41%E6%9C%88271%88.docx
        if file_Name.find("%") == -1:
            encode_file_Name = urllib.parse.quote(file_Name)
        else:
            file_Name = urllib.parse.unquote(file_Name)
        '''
        if create_dir == '1':
            file_Name = title + file_Name[file_Name.find('.'):]
        else:
            file_Name = title + file_Name[file_Name.find('.'):]
        '''
        file_Name = title + file_Name[file_Name.find('.'):]
        #print("url =" + url)
        url = url[:url.rfind('/') + 1] + encode_file_Name
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = urllib.request.Request(url=url, headers=headers)
        try:
            # with urllib.request.urlopen(url) as web:
            with urllib.request.urlopen(req) as web:
                with open(save_dir + '\\' + file_Name, 'wb') as outfile:
                    outfile.write(web.read())
        except BaseException:
            print("下载附件异常   url = " + url + " --- 文件名称 = " + file_Name)
            traceback.print_exc()

    '''
       下载页面 将内容下载到txt文本文件中
       如果该html文件有附件，则需要建立一个已该html文件命名的目录，该目录存储此页面的附件
       url：页面地址
       down_load_dir：存放路径
       title：标题
       '''
    def down_load_page(self, url, down_load_dir, title):
        # 下载html页面
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = urllib.request.Request(url=url, headers=headers)
        #创建当日下改标题目录
        date = datetime.datetime.now().strftime('%Y%m%d')
        file_dir = down_load_dir + '\\' + date + '\\' + title
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        with urllib.request.urlopen(req) as web:
            with open(file_dir + '\\' + title + '.html', 'wb') as outfile:
                outfile.write(web.read())
        # 下载html的内容，将内容存入txt文件中
        self._pre_content(file_dir, title, self.conf_obj)
        # 下载该页面的附件,附件存储在该页面文件夹下
        self._down_page_atts(url, title, file_dir)
    '''
    下载页面内容
    dir：存放路径
    fileName：文件名称
    conf_dic：内容解析配置对象
    '''
    def _pre_content(self, dir, fileName, conf_dic):
        f_html = open(dir+ "\\" + fileName + ".html", 'rb')
        html_byte = f_html.read()
        chardit = chardet.detect(html_byte)
        html_str = html_byte.decode(chardit['encoding'])
        begin = html_str.find(conf_dic['content_begin'])
        end = html_str.find("</div>", begin)
        content = html_str[begin:end]
        f_html.close()
        f_txt = open(dir + "\\" + fileName + ".html", 'w')
        f_txt.truncate()
        f_txt.write(content)
        f_txt.close()
    '''
    下载html页面所有附件信息
    html_url：包含文件的url路径
    title：标题
    file_svae_dir：存放路径
    '''
    def _down_page_atts(self, html_url, title, file_svae_dir):
        html = self._get_page_html(html_url)
        soup = BeautifulSoup(html, "lxml")
        all = soup.find_all(target="_blank")
        parsePage = PageParse()
        for sublink in all:
            href = sublink.get('href')
            if href is None:
                continue

            if parsePage.check_url_type(href) == 'file':
                # 创建文件夹，存储该html的附件
                #print("file==="+href)
                if not os.path.exists(file_svae_dir):
                    os.mkdirs(file_svae_dir)
                index = href.rfind('/')
                s_title = href[index + 1:]
                #url_set,doc_list = parsePage.parse_full_urls([href])
                #print("== "+href)
                #print("===="+url_set)
                #print("====" + doc_list)
                self.down_load_attach(href, file_svae_dir, s_title,'0')

    '''
    根据url获取页面内容
    url：页面路径
    '''
    def _get_page_html(self,url):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        response = urllib.request.urlopen(url)
        html = response.read()
        return html