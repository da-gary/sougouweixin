# -*- coding: utf-8 -*-
import scrapy


class SgwxSpider(scrapy.Spider):
    name = 'sgwx'
    allowed_domains = ['weixin.sougou.com','mp.weixin.qq.com']
    start_urls = ['https://weixin.sogou.com/']
    # start_urls = ['https://weixin.sogou.com/weixin?query=Python&type=2&page=1&ie=utf8']

    def parse(self, response):
        # print(response.text)
        urls = response.xpath('//h3/a/@href').getall()
        # print(urls)
        for url in urls:
            yield scrapy.Request(url,callback=self.parse_info,dont_filter=False)

    def parse_info(self,response):
        title = response.xpath('//div[@id="img-content"]/h2/text()').get().strip()
        author = response.xpath('//div[@id="img-content"]//a[@id="js_name"]/text()').get().strip()
        pub_time = response.xpath('//div[@id="img-content"]//em/text()').get()
        content = response.xpath('//div[@class="rich_media_content "]//p//text()').getall()
        print(title,author,pub_time,content)
