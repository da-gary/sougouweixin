# -*- coding: utf-8 -*-
import scrapy
import re
from fake_useragent import UserAgent

class WxSpider(scrapy.Spider):
    name = 'wx'
    allowed_domains = ['weixin.sogou.com','weixin.qq.com']
    start_urls = ['https://weixin.sogou.com/weixin?query=Python&type=2&page=1&ie=utf8']

    def parse(self, response):
        # print(response.text)
        urls = response.xpath('//h3/a/@href').getall()
        for url in urls:
            # print(response.urljoin(url))
            yield scrapy.Request(response.urljoin(url), callback=self.parse_url)


    def parse_url(self, response):
        print(response.text)
        html = str(response.text)
        urls = re.findall(r"url \+= '(.+)';",html)
        new_url = ''
        for url in urls:
            new_url = new_url + url
        new_url = new_url.replace('http','https')
        print(new_url)
        yield scrapy.Request(new_url,callback=self.parse_info,dont_filter=False)
    def parse_info(self,response):
        title = response.xpath('//div[@id="img-content"]/h2/text()').get().strip()
        author = response.xpath('//div[@id="img-content"]//a[@id="js_name"]/text()').get().strip()
        pub_time = response.xpath('//div[@id="img-content"]//em/text()').get()
        content = ''.join(response.xpath('//div[@class="rich_media_content "]//p//text()').getall())
        print(title,author,pub_time,content)
