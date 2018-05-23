# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RentslamItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ImageUrl = scrapy.Field()
    Url = scrapy.Field()
    Price = scrapy.Field()
    Bedrooms = scrapy.Field()
    Size = scrapy.Field()
    Address = scrapy.Field()
    Text = scrapy.Field()
    ContactEmailAddress = scrapy.Field()
    ContactInfo = scrapy.Field()
    ContactPhoneNumber = scrapy.Field()
    Furnishing = scrapy.Field()
    Postcode = scrapy.Field()
    City = scrapy.Field()
