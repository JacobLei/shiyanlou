#!/usr/bin/env python3

import sys

class Config(object):
    def __init__(self, configfile):
        self._config = {}
        with open(configfile, 'r') as file:
            for line in file:
                key_value = line.replace(' ', '').strip().split('=') # Here can be impoved
                try:
                    self._config[key_value[0]] = float(key_value[1])
                except ValueError:
                    print('Parameter Error')
    def get_config_keylist(self):
        return list(self._config.keys())
    def get_config_value(self, key):
        return self._config[key]

class UserData(object):
    def __init__(self, userdatafile):
        self._userdatafile = {}
        self._premium = 0
        with open(userdatafile, 'r') as file:
            for line in file:
                key_value = line.split(',')
                try:
                    self._userdatafile[key_value[0]] = int(key_value[1])
                except ValueError:
                    print('Parameter Error')
    def get_userdata_idlist(self):
        return list(self._userdatafile.keys())
    def get_userdata_salary(self, key):
        return self._userdatafile[key]
    def dumptofile(self, outputfile):
        with open(outputfile, 'a') as file:
            for key, value in self._userdatafile.items():
                file.write(key + ',' + str(value) + '\n')
    # 各项社会保险费
    def cal_premium(self, salary, config):
        jishul = config._config_value('JiShuL')
        jishuh = config._config_value('JiShuH')
        yanglao = config._config_value('YangLao')
        yiliao = config._config_value('YiLiao')
        shiye = config._config_value('ShiYe')
        gongshang = config._config_value('GongShang')
        shengyu = config._config_value('ShengYu')
        gongjijin = config._config_value('GongJiJin') 
        ratio = (yanglao + yiliao + shiye + gongshang + shengyu + gongjijin)
        if salary < jishul:
            return jishul * ratio
        elif salary > jishuh:
            return jishuh * ratio
        else:          
            return salary * ratio
    def cal_start(self):
        return 3500
    # 应纳税所得额
    def cal_taxable_income(self, salary, premium):
        return salary - premium - cal_start()
    # 计算每个人的应纳税额
    def cal_rate_menoy(self, salary):
        taxable_income = cal_taxable_income(salary)        
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
    def calculator(self, staffid):
        config = Config(sys.argv[1])
        self._premium = cal_premium(self._userdatafile[staffid], config)
        self._rate_menoy = cal_rate_menoy(self._userdatafile[staffid])


if __name__ == '__main__':
    config = Config(sys.argv[1])
    keylist = config.get_config_keylist()
    for key in keylist:
        print('{:.2f}'.format(config.get_config_value(key)))
    
    userdata = UserData(sys.argv[2])
    idlist = userdata.get_userdata_idlist()
    for key in idlist:
        print('{:.2f}'.format(userdata.get_userdata_salary(key)))
    userdata.dumptofile(sys.argv[3]) 
'''
def cal_premium(salary):
    return salary * (0.08 + 0.02 + 0.005 + 0.06)

def cal_start():
    return 3500

# 应纳税所得额
def cal_taxable_income(salary):
    return salary - cal_premium(salary) - cal_start()



# 计算每个人的应纳税额
def cal_rate_menoy(salary):
    taxable_income = cal_taxable_income(salary)        

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

def calculator():
    staffs = {}
    try:
        if len(sys.argv) < 2:
            raise ValueError()
    except ValueError:
        print('Parameter Error')
    for arg in sys.argv[1:]:
        arg_split = arg.split(':')
        try:    
            staffs[arg_split[0]] = int(arg_split[1])
        except ValueError:
            print('Parameter Error')
    for key, value in staffs.items():
        print('{}:{:.2f}'.format(key, value - cal_premium(value) - cal_rate_menoy(value)))
    
if __name__ == '__main__':
    calculator()
'''
