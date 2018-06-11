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
            repository_url =  'https://github.com' + repository.xpath('.//a/@href').extract_first()
            request = scrapy.Request(repository_url, callback=self.parse_other)
            request.meta['item'] = item
            yield request

    def parse_other(self, response):
        item = response.meta['item']
        item['commits'] = response.xpath('(//li//span[contains(@class,"num")])[1]/text()').re_first('[^\d]*(\d*)[^\d]*')
        item['branches'] = response.xpath('(//li//span[contains(@class,"num")])[2]/text()').re_first('[^\d]*(\d*)[^\d]*')
        item['releases'] = response.xpath('(//li//span[contains(@class,"num")])[3]/text()').re_first('[^\d]*(\d*)[^\d]*')
        return item

