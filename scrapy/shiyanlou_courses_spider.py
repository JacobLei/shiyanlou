# -*- coding:utf-8 -*-
import scrapy
import re

class ShiyanlouCoursesSpider(scrapy.Spider):
    """ 所有 scrapy 爬虫需要写一个 Spider 类，这个类要继承 scrapy.Spider类。
    在这个类中定义要请求的网站和链接、如何从返回的网页提取数据等等。
    """
    # 爬虫标识符，在 scrapy 项目中可能会有多个爬虫， name 用于标识每个爬虫，
    # 不能相同
    name = 'shiyanlou-courses'

    ''' scrapy.Spider类已经有了一个默认的 start_requests 方法，我们只需要
    提供需要爬取的 start_urls,默认的 start_requests 方法会根据 start_urls
    生成 Request 对象。
    修改代码：去掉 start_requests方法，添加start_urls方法。


    def start_requests(self):
        """ 需要返回一个可迭代的对象，迭代的元素是'scrapy.Request'对象，
        可迭代对象可以是一个列表或者迭代器，这样 scrapy 就知道有哪些网页
        需要爬取了。'scrapy.Request'接受一个 url 参数和一个 callback 参数，
        url指明要爬取的网页，callback 是一个回调函数用于处理返回的网页，
        通常是一个提取数据的 parse 函数。
        """
        # 课程列表页面 url 模板
        url_tmp1 = 'https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}'
        # 所有要爬取的页面
        urls = (url_tmp1.format(i) for i in range(1,25))
        # 返回一个生成器，生成 Request 对象，生成器是可迭代对象
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    ''' 
    @property
    def start_urls(self):
        """ start_urls 需要返回一个可迭代对象，所以，可以把它写成一个列表、原组或者
        生成器，这里用的是生成器。
        """
        url_tmp1 = 'https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}'
        # 所有要爬取的页面
        return (url_tmp1.format(i) for i in range(1,25))


    def parse(self, response):
        """ 这个方法作为 'scrapy.Request' 的callback,在里面编写提取数据的代码。
        scrapy 中的下载器会下载'start_requests'中定义的每个'Request'并且将结果
        封装为一个response对象传入这个方法。
        """
        # 遍历每个课程的div.course-body
        for course in response.css('div.course-body'):
            # 使用 css 语法对每个 course 提取数据
            yield {
                    'name' : course.css('div.course-name::text').extract_first(),
                    'description' : course.css('div.course-desc::text').extract_first(),
                    'type' : course.css('div.course-footer span.pull-right::text').extract_first(default='Free'),
                    'students': course.xpath('.//span[contains(@class, "pull-left")]/text()[2]').re_first('[^\d]*(\d+)[^\d]*')

                    }
