#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import csv

# 处理命令行参数类
class Args(object):
    def __init__(self):
        self.args = sys.argv[1:]
        self.configfile = ''
        self.userdatafile = ''
        self.outfile = ''
        try:
            self.configfile = self.args[self.args.index('-c')+1]
            self.userdatafile = self.args[self.args.index('-d')+1]
            self.outfile = self.args[self.args.index('-o')+1]
        except:
            print('Args Error')


# 配置文件类
class Config(object):

    def __init__(self):
        self.config = self._read_config()

    def _read_config(self):
        config = {}
        with open(Args().configfile, 'r') as file:
            for line in file:
                key_value = line.replace(' ', '').strip().split('=') 
                try:
                   config[key_value[0]] = float(key_value[1])
                except ValueError:
                    print('Parameter Error')
        return config


# 用户数据类
class UserData(object):

    def __init__(self):
        self.userdata = self._read_users_data()

    def _read_users_data(self):
        userdata = []
        with open(Args().userdatafile, 'r') as file:
            for line in file:
                try:
                    line = list(line.strip().split(','))
                    userdata.append((line[0], int(line[1])))
                except:
                    print('Parameter Error')
        return userdata


# 税后工资计算类
class IncomeTaxCalculator(object):
    
    # 计算每位员工的税后工资函数
    def calc_for_all_userdata(self):
       

if __name__ == '__main__':
#    args = Args() 
#    print(args.configfile)
#    print(args.userdatafile)
#    print(args.outfile)
#    configdict = Config()
#    print(configdict.config)
    userlist = UserData()
    print(userlist.userdata)
