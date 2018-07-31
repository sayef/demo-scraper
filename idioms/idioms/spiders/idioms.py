# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import Request
from scrapy.selector import Selector
from ..items import IdiomItem
from scrapy.loader.processors import TakeFirst, Join


class IdiomsSpider(scrapy.Spider):
    name = 'idioms'
    allowed_domains = ['theidioms.com']
    start_urls = ['https://www.theidioms.com/list/'] + ['https://www.theidioms.com/list/page/' + str(i) for i in range(2, 124)]

    def parse(self, response):
        items = response.xpath("//div[@class='new-list']//a/@href").extract()
        for item in items:
            absolute_url = response.urljoin(item)
            yield Request(absolute_url, callback=self.parse_house)

    def parse_house(self, response):

        l = ItemLoader(item=IdiomItem(), response=response)

        title = response.xpath("//div[@id='phrase']/p[position()=1]/strong/text()").extract_first()
        meaning = response.xpath("//div[@id='phrase']/ul[position()=1]/li/text()").extract()
        examples = [''.join(Selector(text=example).xpath("//text()").extract()) for example in response.xpath("//div[@id='phrase']/ol[position()=1]/li").extract()]

        #l.add_value('title', title)
        #l.add_value('meaning', meaning)
        l.add_value('examples', examples)
        #l.add_value('url', response.url)

        return l.load_item()
