import scrapy


# run command: scrapy crawl bdnews24_4 -o bdnews24_4.jl
# this will create tech4.jl containing all submenus and their hyperlink
class Tech4Spider(scrapy.Spider):
    name = "bdnews24_4"
    start_urls = [
        'http://bdnews24.com',
    ]

    def parse(self, response):
        for list in response.css('div.core > div.submenu > ul.submenu > li'):
            yield {
                'link': response.urljoin(list.css('a::attr(href)').extract_first()),
                'text': list.css('a > span:nth-child(1)::text').extract_first().strip(),
            }