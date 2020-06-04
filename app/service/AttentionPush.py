#!/usr/bin/python3
# -*- coding: utf-8 -*-


'''
    20200521 licl created
    关注内容邮件推送服务
'''
import os
from config.ConfigUtils import ConfigUtils
from tools.SendMailTools import SendMailUtils

class AttentionPush():

    #实例化，获取推送配置
    def __init__(self):
        rootPath = os.path.abspath(os.path.dirname(__file__)).split('jyzqshare')[0]
        config_utils = ConfigUtils(rootPath + 'jyzqshare/config/attention.ini')
        self._conf_obj = config_utils
    '''
        根据标题判断是否是关注的信息，若有人关注该信息，通过邮件的方式推送
        title：标题
    '''
    def send_attention_mail(self, title,body,atts,mail_flag):
        conf_list = self._conf_obj.read_section_items(self._conf_obj.cfgpath)
        for conf in conf_list:
            conf_dic = self._conf_obj.pretty_sectodic(conf)
            keywords = conf_dic['keyworks'].split(',')
            for keyword in keywords:
                if title.find(keyword) >= 0:
                    mail_utils = SendMailUtils()
                    #mail_utils.init_mail_service()
                    mail_utils.receivers = receivers = conf_dic['emails']
                    mail_utils.send_mail(mail_flag, title, body, atts)


#conf = AttentionPush()
#conf.send_attention_mail('test科创板asdfjl','ttt',[],'text')