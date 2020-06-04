#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
20200521 licl created

配置文件配置信息操作封装类
'''

import configparser
import os

class ConfigUtils():

    #构造方法
    def __init__(self, cfgpath):
        self.conf = configparser.ConfigParser()
        print("配置文件路径："+cfgpath)
        self.cfgpath = cfgpath

    #检查是否存在配置项section
    def check_section(self, section):
        try:
            self.conf.items(section)
        except Exception:
            print(">> 无此section，请核对[%s]" % section)
            return None
        return True

    # 读取ini，并获取所有的section名
    def read_section_items(self, cfgpath):
        if not os.path.isfile(cfgpath):
            print(">> 无此文件，请核对路径[%s]" % cfgpath)
            return None
        self.cfgpath = cfgpath
        self.conf.read(cfgpath, encoding="utf-8")
        return self.conf.sections()

    # 读取一个section，list里面对象是元祖
    def read_one_section(self, section):
        try:
            item = self.conf.items(section)
        except Exception:
            print(">> 无此section，请核对[%s]" % section)
            return None
        return item

    # 读取一个section到字典中
    def pretty_sectodic(self, section):
        if not self.check_section(section):
            return None
        res = {}
        for key, val in self.conf.items(section):
            res[key] = val
        return res

    # 读取所有section到字典中
    def pretty_secstodic(self):
        res_1 = {}
        res_2 = {}
        sections = self.conf.sections()
        for sec in sections:
            for key, val in self.conf.items(sec):
                res_2[key] = val
            res_1[sec] = res_2.copy()
            res_2.clear()
        return res_1

    # 删除一个 section中的一个item（以键值KEY为标识）
    def remove_item(self, section, key):
        if not self.check_section(section):
            return
        self.conf.remove_option(section, key)
        self._action_operate('w')
    # 删除整个section这一项
    def remove_section(self, section):
        if not self.check_section(section):
            return
        self.conf.remove_section(section)
        self._action_operate('w')
    # 添加一个section
    def add_section(self, section):
        self.conf.add_section(section)
        self._action_operate('a')
    # 往section添加key和value
    def add_item(self, section, key, value):
        if not self.check_section(section):
            return
        self.conf.set(section, key, value)
        self._action_operate('a')

    # 执行write写入, remove和set方法并没有真正的修改ini文件内容，只有当执行conf.write()方法的时候，才会修改ini文件内容
    def _action_operate(self, mode):
        if mode == 'r+':
            self.conf.write(open(self.cfgpath, "r+", encoding="utf-8"))  # 修改模式
        elif mode == 'w':
            self.conf.write(open(self.cfgpath, "w"))  # 删除原文件重新写入
        elif mode == 'a':
            self.conf.write(open(self.cfgpath, "a"))