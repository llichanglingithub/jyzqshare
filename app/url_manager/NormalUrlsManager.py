#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
20200521 licl created

URL管理器，从主页面入口下返回的所有其他url管理
'''

from config.ConfigUtils import ConfigUtils

class NormalUrlsManager():
    '''
    构造函数
    初始化一个空的集合，用来存储子连接
    '''
    def __init__(self):
        self.urls_set = set()

    '''
    获取所有子页面的url完整连接
    '''
    def get_urls(self):
        return self.urls_set
    '''
    新增一个连接到url管理器中
    '''
    def add_url(self,url):
        self.urls_set.add(url)

    '''
       新增一个集合与原来的url管理器做并集
       '''
    def add_url(self, add_urls_set):
        self.urls_set = self.urls_set.union(add_urls_set)
    '''
    从url管理器中删除链接 这里使用discard方法，不使用remove
    '''
    def remove_url(self,url):
        self.urls_set.discard(url)
    '''
    添加文档列表
    '''
    def add_document(self,documnet_list):
        self.documnet_list = documnet_list
    '''
    返回所有的文档
    '''
    def get_all_document(self):
        return self.documnet_list