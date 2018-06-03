#!/usr/bin/env python3

import sys
from collections import namedtuple

IncomeTaxQuickLookupItem = namedtuple(
    'IncomeTaxQuickLookupItem',
    ['start_point', 'tax_rate', 'quick_subtractor']
    )

INCOME_TAX_START_POINT = 3500

def calc_income_tax(income):
    taxable_part = income -INCOME_TAX_START_POINT 
    if taxable_part <= 0:
        return '0.00'
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
            return '{:.2f}'.format(result) 

def main():
    if len(sys.argv) != 2:
        print('Parameter Error')
        exit()
    try:
        income = int(sys.argv[1])
    except ValueError:
        print('Parameter Error')
        exit()
    print(calc_income_tax(income))

if __name__ == '__main__':
    main()
