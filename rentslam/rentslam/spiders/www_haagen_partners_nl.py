# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from rentslam.items import RentslamItem
from scrapy.loader.processors import TakeFirst, Join


class WwwHaagenPartnersNlSpider(CrawlSpider):
    name = 'www.haagen-partners.nl'
    allowed_domains = ['www.haagen-partners.nl']
    start_urls = ['http://www.haagen-partners.nl/huurwoningen/?city=Amsterdam']
    
    rules = (Rule(LinkExtractor(allow=('single-huurwoning'), deny=('bezichtigingsaanvraag'), process_value=lambda value: value + '/'), callback='parse_item', follow=True),)

    def parse_item(self, response):
        
        l = ItemLoader(item=RentslamItem(), response=response)

        #All data must be extracted using XPATH queries
        image_url = response.xpath('//*[@class="carousel-inner"]//@src').extract_first()
        url = response.url
        price = response.xpath('.//div[contains(@class,"aanbod-info-price")]/text()').extract_first()
        bedrooms = response.xpath('.//p[contains(@class,"aanbod-ifo-rooms")]/text()').extract_first()
        size = response.xpath('.//p[contains(@class,"aanbod-ifo-squarefeet")]/text()').extract_first()
        address = response.xpath('.//h1[contains(@class,"aanbod-ifo-street")]/text()').extract_first()
        text_list = response.xpath('.//div[contains(@class,"wpb_wrapper")]/text()').extract()
        text = (''.join(text_list)).strip()
        # Furnishing in Dutch Oplevering
        furnishing = response.xpath('.//p[contains(@class,"aanbod-ifo-furniture")]/text()').extract_first()
        
        #Full url (mandatory)
        l.add_value('ImageUrl', image_url)
        
        #Full url (mandatory)
        l.add_value('Url', url)

        #Price must not include currency symbol, dot or comma. Decimals must be filtered out. Example: € 1.348,77 --> 1348 (mandatory)
        l.add_value('Price', price, Join(''), re=r'\d+')
        
        #Number (if present). Bedrooms is "Slaapkamers" in Dutch
        l.add_value('Bedrooms', bedrooms, TakeFirst(), re=r'\d+')

        #Size must include only the number. Things like "m2" must be filtered out. Example: 90 m2 --> 90 (if present)
        l.add_value('Size', size, TakeFirst(), re=r'\d+')

        #The address must contain the street name (mandatory) and the house number (if it is present). It must not contain the city name or the postcode
        l.add_value('Address', address)

        #This is the description of the listing (if present)
        l.add_value('Text', text)

        #You can copy the email address from the website here (if present) 
        l.add_value('ContactEmailAddress', 'info@haagen-partners.nl')

        #You can copy the phone number from the website here (if present)
        l.add_value('ContactPhoneNumber', '+31 20 672 33 31')

        l.add_value('Furnishing', furnishing.replace('Oplevering:', '').strip())

        l.add_value('City', 'Amsterdam')

        yield l.load_item()

