#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import csv

# 处理命令行参数类
class Args(object):

    def __init__(self):
        l = sys.argv[1:]
        try:
            self.c = l[l.index('-c')+1]
            self.d = l[l.index('-d')+1]
            self.o = l[l.index('-o')+1]
        except ValueError:
            print('Parameter Error')
            exit()

args = Args()

# 配置文件类
class Config(object):

    def __init__(self):
        self.config = self._read_config()

    def _read_config(self):
        config = {'s': 0}
        with open(args.c) as file:
            for line in file.readlines():
                l = line.split('=')
                try:
                    m, n = l[0].strip(), float(l[1].strip())
                except ValueError:
                    print('Parameter Error')
                    exit()
                if n > 1:
                    config[m] = n
                else:
                    config['s'] += n
        return config

config = Config().config

# 用户数据类
class UserData(object):

    def __init__(self):
        with open(args.d) as f:
            data = list(csv.reader(f))
        self.userdata = data

userdata = UserData().userdata

def cal(id, salary):
    try:
        salary = int(salary)
    except TypeError:
        print('Parameter Error')
    shebao = salary * config['s']
    if salary < config['JiShuL']:
        shebao = config['JiShuL'] * config['s']
    if salary > config['JiShuH']:
        shebao = config['JiShuH'] * config['s']
    tax_s = salary - shebao - 3500
    if tax_s <= 0:
        shuie = 0
    elif tax_s <= 1500:
        shuie = tax_s * 0.03 
    elif tax_s <= 4500:
        shuie = tax_s * 0.1 - 105   
    elif tax_s <= 9000:
        shuie = tax_s * 0.2 - 555
    elif tax_s <= 35000:
        shuie = tax_s * 0.25 - 1005
    elif tax_s <= 55000:
        shuie = tax_s * 0.3 - 2755
    elif tax_s <= 80000:
        shuie = tax_s * 0.35 - 5505
    else:
        shuie = tax_s * 0.45 - 13505
    after_tax = salary - shebao - shuie
    return [id, '{:.2f}'.format(salary), '{:.2f}'.format(shebao), '{:.2f}'.format(shuie), '{:.2f}'.format(after_tax)]

with open(args.o, 'w') as f:
    for a, b in userdata:
        csv.writer(f).writerow(cal(a, b))
'''
# 税后工资计算类
class IncomeTaxCalculator(object):
    
    # 各项社会保险费 
    def calc_premium(self, salary):
        con = Config()
        ratio = 0
        jishul = con.config['JiShuL']
        jishuh = con.config['JiShuH']
        for value in con.config.values():
            ratio = ratio + value
        ratio = ratio - jishul - jishuh
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
        with open(Args().outfile, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(result)


if __name__ == '__main__':
    income = IncomeTaxCalculator()
    income.export()
'''
