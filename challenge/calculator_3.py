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
    
    # 各项社会保险费
    def calc_premium(self, salary):
        jishul = Config().config['JiShuL']
        jishuh = Config().config['JiShuH']
        yanglao = Config().config['YangLao']
        yiliao = Config().config['YiLiao']
        shiye = Config().config['ShiYe']
        gongshang = Config().config['GongShang']
        shengyu = Config().config['ShengYu']
        gongjijin = Config().config['GongJiJin'] 
        ratio = (yanglao + yiliao + shiye + gongshang + shengyu + gongjijin)
        if salary < jishul:
            return jishul * ratio
        elif salary > jishuh:
            return jishuh * ratio
        else:          
            return salary * ratio
    # 起征点
    def calc_start(self):
        return 3500

    # 应纳税所得额
    def calc_taxable_income(self, salary, premium):
        return salary - premium - self.calc_start()
    
    # 计算每个人的应纳税额
    def calc_rate_menoy(self, salary, premium):
        taxable_income = self.calc_taxable_income(salary, premium)        
        if taxable_income <= 1500:
            rate = 0.03 # 税率
            deduction = 0 # 速算扣除数
        elif taxable_income <= 4500:
            rate = 0.1
            deduction = 105
        elif taxable_income <= 9000:
            rate = 0.2
            deduction = 555
        elif taxable_income <= 35000:
            rate = 0.25
            deduction = 1005
        elif taxable_income <= 55000:
            rate = 0.3
            deduction = 2755
        elif taxable_income <= 80000:
            rate = 0.35
            deduction = 5505
        else:
            rate = 0.45
            deduction= 13505
        rate_menoy = taxable_income * rate - deduction # 应纳税额
        if rate_menoy < 0:
            rate_menoy = 0.00
        return rate_menoy
    
    # 计算每位员工的税后工资函数
    def calc_for_all_userdata(self):
        userdata = UserData().userdata
        resultlist = []
        for user in  userdata:
            premium = self.calc_premium(user[1])
            rate_menoy = self.calc_rate_menoy(user[1], premium)
            after_tax = user[1] - rate_menoy - premium
            result = (user[0], '{:.2f}'.format(user[1]), '{:.2f}'.format(premium), '{:.2f}'.format(rate_menoy), '{:.2f}'.format(after_tax))
            resultlist.append(result)
        return resultlist

    # 输出 CSV 文件函数
    def export(self, default='csv'):
        result = self.calc_for_all_userdata()
        print(result)
        with open(Args().outfile, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(result)


if __name__ == '__main__':
#    args = Args() 
#    print(args.configfile)
#    print(args.userdatafile)
#    print(args.outfile)
#    configdict = Config()
#    print(configdict.config)
#    userlist = UserData()
#    print(userlist.userdata)
    income = IncomeTaxCalculator()
    income.export()
    


