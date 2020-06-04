#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
20200521 licl created

文件操作工具类
'''
import os
import pathlib
import zipfile

class FileUtils():
    def __init__(self, parent_path):
        #判断文件目录是否存在
        file_dir = pathlib.Path(parent_path)
        if file_dir.exists():
            self.parent_path = parent_path
        else :
            raise Exception("文件路径不存在")
    '''
    遍历文件夹下的所有文件和文件夹，此处只需要返回文件列表
    parent_path：文件目录
    '''
    def get_file_list(self, parent_path):
        #文件列表
        files_result = []
        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        for root, dirs, files in os.walk(parent_path):
            # 遍历文件
            for f in files:
                files_result.append(os.path.join(root, f))
            # 遍历所有的文件夹
        return files_result
    '''
    将制定目录下的所有文件打包（zip包）
    pach_dir：文件目录
    package_file_name： 打包后的文件名
    '''
    def package_dir_zip(self, pach_dir, package_file_name):
        zip_file = zipfile.ZipFile(pach_dir+package_file_name+'.zip', 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(pach_dir):
            for filename in filenames:
                zip_file.write(os.path.join(dirpath, filename))
        zip_file.close()
        return zip_file

'''
file_utils = FileUtils('E:/licldestop/分享/python分享/爬虫文件路径/test/')
file_utils.package_dir_zip(file_utils.parent_path,'test')
'''
