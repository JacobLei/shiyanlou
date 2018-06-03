#!/usr/bin/env python3

import sys
from collections import namedtuple

IncomeTaxQuickLookupItem = namedtuple(
    'IncomeTaxQuickLookupItem',
    ['start_point', 'tax_rate', 'quick_subtractor']
    )

INCOME_TAX_START_POINT = 3500

SOCIAL_INSURANCE_MONRY_RATE = {
    'endowment_insurance' : 0.08,
    'medical_insurance' : 0.02,
    'unemployment_insurance' : 0.005,
    'employment_injury_insurance' : 0,
    'maternity_insurance' : 0,
    'public_accumulation_funds' : 0.06
    }

def calc_income_and_remain(income):
    social_insurance_money = income * sum(SOCIAL_INSURANCE_MONRY_RATE.values())
    real_income = income - social_insurance_money
    taxable_part = income -social_insurance_money -INCOME_TAX_START_POINT 
    if taxable_part <= 0:
        return '0.00', '{:.2f}'.format(real_income)
    income_tax_quick_lookup_table = [
        IncomeTaxQuickLookupItem(80000, 0.45, 13505),
        IncomeTaxQuickLookupItem(55000, 0.35, 5505),
        IncomeTaxQuickLookupItem(35000, 0.30, 2755),
        IncomeTaxQuickLookupItem(9000, 0.25, 1005),
        IncomeTaxQuickLookupItem(4500, 0.20, 555),
        IncomeTaxQuickLookupItem(1500, 0.10, 105),
        IncomeTaxQuickLookupItem(0, 0.03, 0)
    ]
    for item in income_tax_quick_lookup_table:
        if taxable_part > item.start_point:
            result = taxable_part * item.tax_rate - item.quick_subtractor
            return '{:.2f}'.format(result), '{:.2f}'.format(real_income-result) 

def main():
    if len(sys.argv) < 2:
        print('Parameter Error')
        exit()
    for item in sys.argv[1:]:
        number, income = item.split(':')
        try:
            income = int(income)
        except ValueError:
            print('Parameter Error')
            exit()
        _, remain = calc_income_and_remain(income)
        print('{}:{}'.format(number,remain))

if __name__ == '__main__':
    main()
