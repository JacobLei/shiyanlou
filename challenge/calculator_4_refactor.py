#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import csv
from  multiprocessing import Process, Queue, Lock

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


# 税后工资计算类
class IncomeTaxCalculator(object):
    
    # 计算每个人的应纳税额
    def calc(self, id, salary):
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

    # 输出 CSV 文件函数
    def export(self, default='csv'):
        with open(args.o, 'w') as f:
            for a, b in userdata:
                csv.writer(f).writerow(cal(a, b))


if __name__ == '__main__':
#    income = IncomeTaxCalculator()
#    income.export()
    queue = Queue()
    queue2 = Queue()
    lock = Lock()
    process1 = Process(target=UserData().read_users_data())
    process1.start()
    process1.join()
    process2 = Process(target=IncomeTaxCalculator().calc_for_all_userdata())
    process2.start()
    process2.join()
    process3 = Process(target=IncomeTaxCalculator().export())
    process3.start()  
    process3.join()
#    print(queue2.get()) 
