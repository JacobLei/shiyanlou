#!/usr/bin/env python3

import sys

class Config(object):
    def __init__(self, configfile):
        self._config = {}
        with open(configfile, 'r') as file:
            print('file', file)
#            print(file.read())
            for line in file:
                key_value = line.split('=')
                for key, value in key_value.items():
                    key.strip()
                    value.strip()
#                print('key_value:', key_value)
                try:
                    self._config[key_value[0]] = int(self._config[key_value[1]])
                except ValueError:
                    print('Parameter Error')
    def get_config_keylist(self):
        return list(self._config.keys())
    def get_config_value(self, key):
        return self._config[key]

if __name__ == '__main__':
    config = Config(sys.argv[1])
    keylist = config.get_config_keylist()
    print(keylist)
    for key in keylist:
        print('{:.2f}'.format(config.get_config_value(key)))
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
