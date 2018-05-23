# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import Request
from rentslam.items import RentslamItem
from scrapy.loader.processors import TakeFirst, Join


class AmsterdamInterhouseSpider(scrapy.Spider):
    name = "amsterdaminterhouse"
    allowed_domains = ["amsterdam.interhouse.nl"]
    start_urls = ["http://amsterdam.interhouse.nl/en/property_listing"]

    def parse(self, response):
        # All data must be extracted using XPATH queries
        # This path should return a list of urls that contain the information about the listings
        items = response.xpath('//a[@class="btn-cta"]/@href').extract()
        print("Items")
        print(items)
        for item in items:
            absolute_url = response.urljoin(item)
            yield Request(absolute_url, callback=self.parse_house)

    def parse_house(self, response):
        l = ItemLoader(item=RentslamItem(), response=response)

        # All data must be extracted using XPATH queries

        # Full url. Only the first image is required
        image_url = response.xpath('//img[@class="image"]').extract_first()
        url = response.url
        price = response.xpath('//tf[@class="bold"]').extract_first()
        bedrooms = response.xpath('//table[@class="specs"]/tbody[1]/tr[3]/td[1]').extract_first()
        size = response.xpath('//table[@class="specs"]/tbody[1]/tr[4]/td[1]').extract_first()
        address = response.xpath('//table[@class="specs"]/tbody[1]/tr[1]/td[1]').extract_first()
        text = response.xpath('//p[@class="hightlightText"]').extract_first()
        city = response.xpath('//div[@class="left"]/h1[1]').extract_first()
        furnishing = response.xpath('//table[@class="specs"]/tbody[1]/tr[6]/td[1]').extract_first()
        contact_email_address = response.xpath('//div[@class="address"]/p[2]/a[1]').extract_first()
        contact_phone_number = response.xpath('//div[@class="address"]/p[2]').extract_first()
        # postcode = response.xpath("").extract_first()

        # Url of the website (HTTP version)
        contact_info = "http://amsterdam.interhouse.nl"

        # Full url. Only the first image is required
        l.add_value("ImageUrl", image_url)

        # Full url
        l.add_value("Url", url)

        # Price must not include currency symbol, dot or comma. Decimals must be filtered out. Example: € 1.348,77 --> 1348
        l.add_value("Price", price)

        # Number
        l.add_value("Bedrooms", bedrooms)

        # Size must include only the number. Things like "m2" must be filtered out. Example: 90 m2 --> 90
        l.add_value("Size", size)
        # The address must contain the street name and the house number (if it is present). It must not contain the city name or the postcode
        l.add_value("Address", address)

        # This is the description of the listing
        l.add_value("Text", text)

        l.add_value("ContactEmailAddress", contact_email_address)

        l.add_value("ContactPhoneNumber", contact_phone_number)

        l.add_value("ContactInfo", contact_info)

        l.add_value("Postcode", None)

        l.add_value("Furnishing", furnishing)

        # Name of the city.
        l.add_value("City", city)

        print('URL: ' + url)

        return l.load_item()