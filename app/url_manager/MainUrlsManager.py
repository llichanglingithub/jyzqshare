#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
20200521 licl created

URL管理器，管理需要爬取数据的url和相关的解析配置
由于每个web界面解析算法随着web的升级不断改变，将其抽象为配置的方式，方便今后维护
'''

from config.ConfigUtils import ConfigUtils
import os

class MainUrlsManager():
    """
    urls为一个双层结构的字典类型
    key表示爬取的网页名称
    value表示爬取的网页的相关配置的字典类型
    """
    def __init__(self):
        self.config_init()
    '''
    从配置文件中获取配置信息并存储到当前对象中
    '''
    def config_init(self):
        #定义一个空的字典用来存储从配置文件获取的配置信息
        urls_dict = {}
        #定义一个空的列表，用来获取配置文件中的所有配置块（section）
        conf_list = []
        #实例化配置工具类
        rootPath = os.path.abspath(os.path.dirname(__file__)).split('jyzqshare')[0]
        config_utils = ConfigUtils(rootPath + 'jyzqshare/config/config_urls.ini')
        #获取所有配置块
        conf_list = config_utils.read_section_items(config_utils.cfgpath)
        self.conf_list = conf_list
        #循环获取配置块配置信息
        for s_item in conf_list:
            item_config = config_utils.pretty_sectodic(s_item)
            urls_dict[s_item] = item_config
        self.urls_dict = urls_dict



#测试
'''
urls_manager = MainUrlsManager()
print(urls_manager.conf_list)
print(urls_manager.urls_dict)
print(urls_manager.urls_dict['szjys_gg']['down_load_dir'])
'''




