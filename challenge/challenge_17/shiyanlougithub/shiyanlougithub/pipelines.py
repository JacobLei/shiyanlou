# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from shiyanlougithub.models import Repository, engine
from datetime import datetime

def to_string(num):
    string = ''
    num1 = num.split(',')
    for i in range(len(num1)):
        string += num1[i]
    return string

class ShiyanlougithubPipeline(object):
    def process_item(self, item, spider):
        item['update_time'] = datetime.strptime(
            item['update_time'], '%Y-%m-%dT%H:%M:%SZ')
        item['commits'] = int(to_string(item['commits']))
        item['branches'] = int(to_string(item['branches']))
        item['releases'] = int(to_string(item['releases']))
        self.session.add(Repository(**item))
        return item

    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
