#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import datetime
from url_manager.MainUrlsManager import MainUrlsManager
from  url_manager.NormalUrlsManager import NormalUrlsManager
from parse.PageParse import PageParse
from download.Downloader import Downloader
from service.AttentionPush import AttentionPush
from tools.FileUtils import FileUtils

'''
20200522 licl created

应用入口

'''

if __name__ == '__main__':
    #rootPath  = os.path.abspath(os.path.dirname(__file__)).split('jyzqshare')[0]
    #print(rootPath)
    #根据配置文件获取主页面配置信息
    mainPageUrls = MainUrlsManager()
    #子页面url管理器
    normalUrls = NormalUrlsManager()
    #print(mainPageUrls.urls_dict['shjys-gg'])
    #获取连接列表
    pageParse = PageParse()
    attention_push = AttentionPush()
    date = datetime.datetime.now().strftime('%Y%m%d')
    for page_conf in mainPageUrls.urls_dict:
        url_list,doc_list = pageParse.parse_main_page(mainPageUrls.urls_dict[page_conf])
        normalUrls.add_url(url_list)
        normalUrls.add_document(doc_list)
        #print(normalUrls.get_urls())
        #print(normalUrls.get_all_document())
        downloader = Downloader(mainPageUrls.urls_dict[page_conf])
        for doc in doc_list:
            mail_content = ''
            file_dir = downloader.conf_obj['down_load_dir'] + "\\" + date + '\\'+ doc['title']
            if pageParse.check_url_type(doc['href']) == 'file':
                #附件下载
                downloader.down_load_attach(doc['href'],downloader.conf_obj['down_load_dir'],doc['title'], '1')
                mail_content = '<p>详见附件</>'
            elif pageParse.check_url_type(doc['href']) == 'html':
                #html内容及其中的附件下载
                downloader.down_load_page(doc['href'],downloader.conf_obj['down_load_dir'],doc['title'])
                file_list = FileUtils(file_dir)

                with open(file_dir+ '\\' + doc['title'] + '.html') as lines:
                    line_content = lines.readlines()
                    mail_content = ''.join(line_content)
            file_list = FileUtils(file_dir)
            atts = file_list.get_file_list(file_list.parent_path)
            attention_push.send_attention_mail(doc['title'], mail_content, atts, 'file_h')


    #print(pageParse.page_document_list)
    #print(normalUrls.get_urls())


