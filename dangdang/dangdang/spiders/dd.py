# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from dangdang.items import DangdangItem

class DdSpider(CrawlSpider):
    name = 'dd'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://bang.dangdang.com/books/bestsellers']

    rules = (
        Rule(LinkExtractor(allow='/books/bestsellers/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = DangdangItem()
        item['kind'] = response.xpath("//div[@class='layout_location']/span[last()]/text()").extract_first()
        allitem = response.css('.bang_list.clearfix.bang_list_mode>li')
        for i in allitem:
            item['name'] = i.css('.name>a').xpath('./@title').extract_first()
            item['link'] = i.css('.name>a').xpath('./@href').extract_first()
            item['comment'] = i.css('.star>a::text').extract_first()
            item['satisfaction'] = i.css('.tuijian::text').extract_first()
            item['price'] = i.xpath("//div[@class='price']/p[1]/span[@class='price_n']/text()").extract_first()
            yield item

