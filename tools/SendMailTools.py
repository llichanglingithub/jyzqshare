#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
20200521 licl created

发送邮件工具类
'''

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from config.ConfigUtils import ConfigUtils
from tools.FileUtils import FileUtils

class SendMailUtils():

    def __init__(self):
        self.init_mail_service()
    #实例化邮件发送
    def init_mail_service(self):
        mail_config_ini = ''
        rootPath = os.path.abspath(os.path.dirname(__file__)).split('jyzqshare')[0]
        config = ConfigUtils(rootPath + 'jyzqshare/config/sendmailconf.ini')
        secs = config.read_section_items(config.cfgpath)
        #获取邮件配置section中的相关配置
        #print(secs)
        #print(len(secs))
        if len(secs) >= 1:
            self.config_dictionary = config.pretty_sectodic(secs[0])
            self.receivers = self.config_dictionary['receivers']
            #print(self.config_dictionary)
        if self.config_dictionary is not None:
            # 实例化发件实例
            self.smtpObj = smtplib.SMTP()
        else :
            print('未获取到邮件发送服务器及发件用户名相关配置信息')
    '''
    设置收件人，不是用默认收件人
    receivers：收件人列表
    '''
    def set_receivers(self,receivers):
        self.receivers = receivers
    """
    发送邮件方法
    mail_flag 发送邮件类型
    text:一般文本邮件
    html: html邮件内容
    file_t:带附件的文本邮件
    file_h:带附件的html邮件
    """
    def send_mail(self,mail_flag, title, content, atts):
        receivers = self.receivers  # 接收邮件用户列表
        if mail_flag == 'text':
            self.message = MIMEText(content, 'plain', 'utf-8')
        elif mail_flag == 'html':
            self.message = MIMEText(content, 'html', 'utf-8')
        elif mail_flag == 'file_t':
            self.message = MIMEMultipart()
            self.message.attach(MIMEText(content, 'plain', 'utf-8'))
        elif mail_flag == 'file_h':
            self.message = MIMEMultipart()
            self.message.attach(MIMEText(content, 'html', 'utf-8'))
        else:
            pass
        #填充附件列表
        if mail_flag == 'file_h' or mail_flag == 'file_t':
            for att_file in atts:
                att_obj = MIMEText(open(att_file, 'rb').read(), 'base64', 'utf-8')
                att_obj["Content-Type"] = 'application/octet-stream'
                file_path = att_file.split('\\')
                file_name = file_path[len(file_path)-1]
                y_file_name = file_name
                file_name = Header(file_name, 'utf-8').encode()
                print(file_name + '====='+ str(file_name.find('.html')))
                if y_file_name.find('.html') < 0:
                    disposition = 'attachment; filename="'+file_name+'"'
                    att_obj["Content-Disposition"] = disposition
                    #print(att_obj)
                    self.message.attach(att_obj)

        # 设置发送人员和接收人员
        self.message['From'] = Header(self.config_dictionary['sender'], 'utf-8')
        self.message['To'] = Header(self.receivers, 'utf-8')
        subject = title
        self.message['Subject'] = Header(subject, 'utf-8')
        try:
            self.smtpObj.connect(self.config_dictionary['smtp_server'],self.config_dictionary['smtp_port'])  # 25 为 SMTP 端口号
            self.smtpObj.login(self.config_dictionary['sender'], self.config_dictionary['send_user_pwd'])  # 用户名密码
            self.smtpObj.sendmail(self.config_dictionary['sender'], receivers, self.message.as_string())
            print('发送邮件成功')
        except Exception as e:
            print(e)
            print("发送邮件失败")

'''
#测试一般邮件发送
utils = SendMailUtils()
utils.init_mail_service()
utils.send_mail('text',"测试邮件标题text",'测试邮件内容11--sss------------------',[])
'''

'''
#测试html邮件发送
utils = SendMailUtils()
utils.init_mail_service()
msg_content = """
<p>Python 邮件发送测试...</p>
<p><a href="http://www.baidu.com">这是一个链接</a></p>
"""
utils.send_mail('html',"测试邮件标题html",msg_content,[])
'''

'''
#测试带附件的html邮件发送
utils = SendMailUtils()
utils.init_mail_service()
atts = []
msg_content = """
<div class="allZoom">  <p style="text-align: center;">上证公告（基金）【2020】171号</p><p>　　为促进工银瑞信黄金交易型开放式证券投资基金(以下简称工银黄金，基金代码:518660)的市场流动性和平稳运行，根据《上海证券交易所上市基金流动性服务业务指引（2018年修订）》等相关规定，本所同意申万宏源证券有限公司自2020年5月29日起为工银黄金提供一般流动性服务。</p><p>　　特此公告。<br />&nbsp;</p><p>　　上海证券交易所</p><p>　　二〇二〇年五月二十九日</p>
"""
utils.send_mail('file_h',"测试邮件标题html-atts",msg_content,atts)
'''

'''
#测试待附件的文本邮件发送
utils = SendMailUtils()
utils.init_mail_service()
atts = ['E:/licldestop/分享/python分享/爬虫文件路径/test/test.xlsx','E:/licldestop/分享/python分享/爬虫文件路径/test/课程地址.txt']
msg_content = """
this is test for send mail att
测试段落
"""
utils.send_mail('file_t',"测试邮件标题html-atts",msg_content,atts)
'''

'''
# 测试发送一个目录下所有文件
utils = SendMailUtils()
utils.init_mail_service()
file_list = FileUtils('E:/licldestop/分享/python分享/爬虫文件路径/test/')
atts = file_list.get_file_list(file_list.parent_path)
msg_content = """
this is test for send mail att
测试段落
"""
utils.send_mail('file_t',"测试邮件标题html-atts",msg_content,atts)
'''
