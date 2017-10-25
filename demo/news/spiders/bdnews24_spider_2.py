import scrapy


# run command: scrapy crawl bdnews24_2
class Tech2Spider(scrapy.Spider):
    name = "bdnews24_2"
    start_urls = [
        'http://bdnews24.com',
    ]

    def parse(self, response):
        page = response.url.split("/")[2]
        filename = '%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)