#-*- coding:utf-8 -*-

import scrapy
from datetime import datetime

class ShiyanlouGithubSpider(scrapy.Spider):
    name = 'shiyanlou-github'

    @property
    def start_urls(self):
        url_tmp1 = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmp1.format(i) for i in range(1, 5))

    def parse(self, response):
        for repository in response.xpath('//*[@id="user-repositories-list"]/ul/li'):
            yield {
                    'name' : repository.xpath('.//a/text()').extract_first().strip(),
                    'update_time' : datetime.strptime(repository.xpath('.//relative-time/@datetime').extract_first(), '%Y-%m-%dT%H:%M:%SZ')
                    }
