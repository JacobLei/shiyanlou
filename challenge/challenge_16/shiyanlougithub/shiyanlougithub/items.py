# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShiyanlougithubItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class RepositoryItem(scrapy.Item):
    name = scrapy.Field()
    update_time = scrapy.Field()
