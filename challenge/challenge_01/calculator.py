#!/usr/bin/env python3

import sys

premium = 0 # 各项社会保险费
start = 3500 #起征点 3500

# 确定输入参数有且只有一个，且为int型
if len(sys.argv) == 2:
    try:
        salary = int(sys.argv[1])
    except ValueError:
        print('Parameter Error')
        exit()
else:
    print('Parameter Error')
    exit()

taxable_income = salary - premium - start # 应纳税所得额

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

print('{:.2f}'.format(rate_menoy))
