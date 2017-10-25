# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class NewsItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    news_content_id = Field()
    news_title = Field()
    news_images = Field()
    news_summary = Field()
    news_details = Field()
    pass
