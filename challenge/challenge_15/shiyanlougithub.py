#-*- coding:utf-8 -*-

import scrapy

class ShiyanlouGithubSpider(scrapy.Spider):
    name = 'shiyanlou-github'

    @property
    def start_urls(self):
        url_tmp1 = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmp1.format(i) for i in range(1, 5))

    def parse(self, response):
        for respository in response.css('li.col-12'):
            yield {
                    'name' : respository.xpath('.//div[contains(@class,"d-inline-block")]/h3/a/text()').re_first('[^\w]*(.*)'), 
                    'update_time' : respository.xpath('.//relative-time/@datetime').extract_first()
                    }
