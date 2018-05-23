# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import Request
from rentslam.items import RentslamItem
from scrapy.loader.processors import TakeFirst, Join


class ExpatsAmsterdamSpider(scrapy.Spider):
    name = 'expatsamsterdam'
    allowed_domains = ['expats.amsterdam']
    start_urls = ['http://www.expats.amsterdam/city-area/amsterdam/?apt-type=all&apt-bedrooms=all&undefined=27&apt-price=all&apt-interior=either',
    'http://www.expats.amsterdam/city-area/amstelveen/?apt-type=all&apt-bedrooms=all&undefined=34&apt-price=all&apt-interior=either']

    def parse(self, response):
        #All data must be extracted using XPATH queries
        #This path should return a list of urls that contain the information about the listings
        items = response.xpath("").extract()
        for item in items:
            absolute_url = response.urljoin(item)
            yield Request(absolute_url, callback=self.parse_house)
            

    def parse_house(self, response):
        
        l = ItemLoader(item=RentslamItem(), response=response)

        #All data must be extracted using XPATH queries

        #Full url. Only the first image is required
        image_url = response.xpath('').extract_first()
        url = response.xpath('').extract_first()
        price = response.xpath('').extract_first()
        bedrooms = response.xpath('').extract_first()
        size = response.xpath('').extract_first()
        address = response.xpath('').extract_first()
        text = response.xpath('').extract_first()
        city = response.xpath('').extract_first()
        furnishing = response.xpath('').extract_first()
        contact_email_address = response.xpath('').extract_first()
        contact_phone_number = response.xpath('').extract_first()
        postcode = response.xpath('').extract_first()
        
        #Url of the website (HTTP version)
        contact_info = "http://www.expats.amsterdam"

        #Full url. Only the first image is required
        l.add_value('ImageUrl', image_url)
        
        #Full url
        l.add_value('Url', url)

        #Price must not include currency symbol, dot or comma. Decimals must be filtered out. Example: € 1.348,77 --> 1348
        l.add_value('Price', price)
        
        #Number
        l.add_value('Bedrooms', bedrooms)

        #Size must include only the number. Things like "m2" must be filtered out. Example: 90 m2 --> 90
        l.add_value('Size', size)
        #The address must contain the street name and the house number (if it is present). It must not contain the city name or the postcode
        l.add_value('Address', address)

        #This is the description of the listing
        l.add_value('Text', text)

        l.add_value('ContactEmailAddress', contact_email_address)

        l.add_value('ContactPhoneNumber', contact_phone_number)

        l.add_value('ContactInfo', contact_info)

        l.add_value('Postcode', postcode)

        l.add_value('Furnishing', furnishing)

        #Name of the city.
        l.add_value('City', city)

        return l.load_item()