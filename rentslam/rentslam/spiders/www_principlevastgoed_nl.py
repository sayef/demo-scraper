# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from rentslam.items import RentslamItem
from scrapy.loader.processors import TakeFirst, Join

class WwwPrinciplevastgoedNlSpider(scrapy.Spider):
    name = 'www.principlevastgoed.nl'
    allowed_domains = ['principlevastgoed.nl']
    start_urls = [
        'https://www.principlerealestate.nl/huurwoningen/?filter-sort-by=published&filter-sort-order=desc&filter-location=428',
        'https://www.principlerealestate.nl/huurwoningen/?filter-sort-by=published&filter-sort-order=desc&filter-location=497']

    def parse(self, response):
        
        #All data must be extracted using XPATH queries
        #This path should return a list of block of HTML code that contain the information about the listings
        items = response.xpath("//article[contains(@class,'property-row')]")
        for item in items:
             l = ItemLoader(item=RentslamItem(), response=response)

             #All data must be extracted using XPATH queries
             image_url = item.xpath('.//img/@src').extract_first()
             url = item.xpath('.//a/@href').extract_first()
             price = item.xpath('.//span[contains(@class,"property-row-meta-item-price")]/strong/text()').extract_first()
             bedrooms = item.xpath('.//span[contains(@class,"property-row-meta-item-beds")]/strong/text()').extract_first()
             size = item.xpath('.//span[contains(@class,"property-row-meta-item-area")]/strong/text()').extract_first()
             address = item.xpath('.//h2/a/text()').extract_first()
             text = item.xpath('.//div[@class="property-row-body"]/p/text()').extract_first()
             city = item.xpath('.//div[@class="property-row-location"]/a/text()').extract_first()

             #In this example there is no furnishing info, it can be left enpty
             #furnishing = item.xpath('').extract_first()
             

             #Full url. Only the first image is required
             l.add_value('ImageUrl', image_url)
             
             #Full url
             l.add_value('Url', url)

             #Price must not include currency symbol, dot or comma. Decimals must be filtered out. Example: € 1.348,77 --> 1348
             l.add_value('Price', price, Join(''), re=r'\d+')
             
             #Number
             l.add_value('Bedrooms', bedrooms)

             #Size must include only the number. Things like "m2" must be filtered out. Example: 90 m2 --> 90
             l.add_value('Size', size, TakeFirst(), re=r'\d+')
             #The address must contain the street name and the house number (if it is present). It must not contain the city name or the postcode
             l.add_value('Address', address)

             #This is the description of the listing
             l.add_value('Text', text)

             #You can copy th email address from the website here 
             l.add_value('ContactEmailAddress', 'info@principlerealestate.nl')

             #You can copy th phoen number from the website here
             l.add_value('ContactPhoneNumber', '085 - 273 67 30')

             #In this example there is no furnishing info, it can be left enpty
             #l.add_value('Furnishing', furnishing)

             #Name of the city. Sometimes it can have a literal value, like "Amsterdam", if the website only contains listings from amsterdam.
             l.add_value('City', city)

             yield l.load_item()


            
