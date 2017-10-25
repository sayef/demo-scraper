import scrapy


# run command: scrapy crawl bdnews24_1
# this will save a page named bdnews24.com.html
class Tech1Spider(scrapy.Spider):
    name = "bdnews24_1"

    def start_requests(self):
        urls = [
            'http://bdnews24.com',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[2]
        filename = '%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)