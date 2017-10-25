import scrapy


# run command: scrapy crawl bdnews24_5 -o bdnews24_5.jl
# This will get all news links that has the page /all[category] ie science/allscience
class Tech5Spider(scrapy.Spider):
    name = "bdnews24_5"
    start_urls = [
        'http://bdnews24.com',
    ]

    def parse(self, response):
        for news in response.css('div.core > div.submenu > ul.submenu > li'):
            category = news.css('a > span:nth-child(1)::text').extract_first().strip()
            next_page = news.css('a::attr(href)').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse_content)

    def parse_content(self, response):
        all_news_page = response.css('div[id="latest_news2"] a::attr(href)').extract_first()
        if all_news_page is not None:
            if all_news_page.find("all", 0, len(all_news_page)) >= 0:
                yield {
                    'all_news_url': all_news_page
                }
