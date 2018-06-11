# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import RepositoryItem


class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'

    @property
    def start_urls(self):
        url_temp = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_temp.format(i) for i in range(1, 5))

    def parse(self, response):
        for repository in response.css('li.col-12'):
            item = RepositoryItem({
                'name' : repository.xpath('.//div[contains(@class,"d-inline-block")]/h3/a/text()').re_first('[^\w]*(.*)'),
                'update_time' : repository.xpath('.//relative-time/@datetime').extract_first()
                })
            yield item
