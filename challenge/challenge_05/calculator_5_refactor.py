#!/usr/bin/env python3

import sys
import csv
import getopt
import queue
from collections import namedtuple
from multiprocessing import Process, Queue 
from configparser import ConfigParser
from datetime import datetime

IncomeTaxQuickLookupItem = namedtuple(
    'IncomeTaxQuickLookupItem',
    ['start_point', 'tax_rate', 'quick_subtractor']
    )

INCOME_TAX_START_POINT = 3500

INCOME_TAX_QUICK_LOOKUP_TABLE = [
    IncomeTaxQuickLookupItem(80000, 0.45, 13505),
    IncomeTaxQuickLookupItem(55000, 0.35, 5505),
    IncomeTaxQuickLookupItem(35000, 0.30, 2755),
    IncomeTaxQuickLookupItem(9000, 0.25, 1005),
    IncomeTaxQuickLookupItem(4500, 0.20, 555),
    IncomeTaxQuickLookupItem(1500, 0.10, 105),
    IncomeTaxQuickLookupItem(0, 0.03, 0)
]

q_user = Queue()
q_result = Queue()

class Args(object):
    
    def __init__(self):
        self.options = self._options()

    def _options(self):
        try:
            opts, _ = getopt.getopt(sys.argv[1:], 'hC:c:d:o:', ['help'])
        except getopt.GetoptError:
            print('Parameter Error')
            exit()
        options = dict(opts)
        if len(options) == 1 and ('-h' in options or '--help' in options):
            print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
            exit()
        return options

    
    def _value_after_option(self, option):
        value = self.options.get(option)
        if value is None and option != '-C':
            print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
            exit()
        return value

    @property
    def cityname(self):
        return self._value_after_option('-C')

    @property
    def config_path(self):
        return self._value_after_option('-c')

    @property
    def userdata_path(self):
        return self._value_after_option('-d')

    @property
    def export_path(self):
        return self._value_after_option('-o')

args = Args()

class Config(object):

    def __init__(self):
        self.config = self._read_config() 
        

    def _read_config(self):
        cityname = args.cityname.upper()
        config_path = args.config_path
        config_file = ConfigParser()
        config_file.read(config_path)
        lists_header = config_file.sections()
        if cityname in lists_header:
           items = config_file.items(cityname)
        else:
           items = config_file.items('DEFAULT')
        config = {}
        for line in items:
            key, value = line[0], line[1]
            try:
                config[key] = float(value)
            except ValueError:
                print('Parameter Error')
                exit()
        return config

    def _get_config(self, key):
        try:
            return self.config[key]
        except KeyError:
            print('config Error')
            exit()

    @property
    def social_insurance_baseline_low(self):
        return self._get_config('jishul')

    @property
    def social_insurance_baseline_high(self):
        return self._get_config('jishuh')

    @property
    def social_insurance_total_rate(self):
        return sum([
            self._get_config('yanglao'),
            self._get_config('yiliao'),
            self._get_config('shiye'),
            self._get_config('gongshang'),
            self._get_config('shengyu'),
            self._get_config('gongjijin')
        ])

config = Config()

class Userdata(Process):
    
    def _read_userdata(self):
        userdata_path = args.userdata_path
        with open(userdata_path) as f:
            for line in f.readlines():
                empolyee_id, income_string = line.strip().split(',')
                try:
                    income = int(income_string)
                except ValueError:
                    print('Parameter Error')
                    exit()
                yield (empolyee_id, income)

    def run(self):
        for data in self._read_userdata():
            q_user.put(data)

class IncomeTaxCalulator(Process):

    @staticmethod
    def calc_social_insurance_money(income):
        low = config.social_insurance_baseline_low
        high = config.social_insurance_baseline_high
        total_rate = config.social_insurance_total_rate
        if income < low:
            return low * total_rate
        if income > high:
            return high * total_rate
        return income * total_rate

    @classmethod
    def calc_income_and_remain(cls, income):
        social_insurance_money = cls.calc_social_insurance_money(income)
        real_income = income - social_insurance_money
        taxable_part = real_income - INCOME_TAX_START_POINT
        if taxable_part <= 0:
            return '0.00', '{:.2f}'.format(real_income)
        for item in INCOME_TAX_QUICK_LOOKUP_TABLE:
            if taxable_part > item.start_point:
                tax = taxable_part * item.tax_rate - item.quick_subtractor
                return '{:.2f}'.format(tax), '{:.2f}'.format(real_income - tax)

    def calc_for_all_userdata(self):
        while True:
            try:
                employee_id, income = q_user.get(timeout=1)
            except queue.Empty:
                return
            data = [employee_id, income]
            social_insurance_money = '{:.2f}'.format(self.calc_social_insurance_money(income))
            time = datetime.utcnow()
            tax, remain = self.calc_income_and_remain(income)
            time = datetime.strftime(datetime.utcnow(), '%Y-%m-%d %H:%M:%S')
            data = data + [social_insurance_money, tax, remain, time]
            yield data

    def run(self):
        for data in self.calc_for_all_userdata():
            q_result.put(data)

class Exporter(Process):

    def run(self):
        with open(args.export_path, 'w', newline='') as f:
            while True:
                try:
                    data = q_result.get(timeout=1)
                except queue.Empty:
                    return
                csv.writer(f).writerow(data)

if __name__ == '__main__':
    workers = [Userdata(), IncomeTaxCalulator(), Exporter()]
    for worker in workers:
        worker.run()
