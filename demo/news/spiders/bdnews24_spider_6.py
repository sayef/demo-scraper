import scrapy
import re
import time
import hashlib


# run command: scrapy crawl bdnews24_6 -o bdnews24_6.jl -a category=technology
class Tech6Spider(scrapy.Spider):
    name = "bdnews24_6"

    # start_urls = [
    #     'http://bdnews24.com',
    # ]

    def start_requests(self):
        url = 'http://bdnews24.com/'
        category = getattr(self, 'category', None)
        # print('CATEGORY:' + category)
        # if category is not None:
        #    url = url + category + '/all' + category + 'news/'
        request = scrapy.Request(url, self.parse)
        request.meta['category'] = category
        yield request

    def parse(self, response):
        for news in response.css('div.core > div.submenu > ul.submenu > li'):
            # category = news.css('a > span:nth-child(1)::text').extract_first().strip()
            next_page = news.css('a::attr(href)').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                request = scrapy.Request(next_page, callback=self.parse_category)
                request.meta['category'] = response.meta['category']
                yield request

    def parse_category(self, response):
        all_news_page = response.css('div[id="latest_news2"] a::attr(href)').extract_first()
        if all_news_page is not None:
            if response.meta['category'] == 'all' and all_news_page.find("all") >= 0:
                yield scrapy.Request(all_news_page, callback=self.parse_news_list)

            elif all_news_page.find("all" + response.meta['category'] + 'news', 0, len(all_news_page)) >= 0:
                yield scrapy.Request(all_news_page, callback=self.parse_news_list)

    def parse_news_list(self, response):
        # print("RESPONSE: " + response.url)
        for news in response.css('p[class="classForTagArticleTitle_21"] > a::attr(href)').extract():
            news_page = response.urljoin(news)
            print("RESPONSE: " + news_page)
            yield scrapy.Request(news_page, callback=self.parse_content)

        # next_page = response.css('li.next > a > span.takeNextData').extract_first()
        # if next_page is not None:

    def parse_content(self, response):

        news_publish_time = self.sanitize_content(
            response.css('div[id="article_notations"] > p:nth-child(1) > span:nth-child(2)::text').extract_first()),
        news_title = response.css('div[id="news-details-page"] > h1:nth-child(1)::text').extract_first(),
        news_images = response.css('div[id="gallery_slide_customize"] img::attr(src)').extract(),
        news_summary = response.css('div.article_lead_text > h5:nth-child(1)::text').extract_first(),
        news_details = self.concat_paragraph(response.css('div.article_body > * > p::text').extract())

        news_title = ''.join(news_title)
        news_publish_time = ''.join(news_publish_time)

        temp_content_id = response.url + news_title + news_publish_time
        content_id = hashlib.sha256(bytes(temp_content_id, "utf-8")).hexdigest()

        yield {
            'content_id': content_id,
            'news_title': news_details,
            'news_images': news_images,
            'news_summary': news_summary,
            'news_details': news_details
        }

    def concat_paragraph(self, str):
        return ' '.join(self.sanitize_content(x) for x in str)

    def sanitize_content(self, content):
        content = content.replace("\t", " ") # remove tab
        content = content.replace("\n", " ") # remove line feed
        content = content.replace("\r", " ") # remove carriage return
        # content = content.replace("\"", " ") # remove "
        content = content.strip() # strip leading and tailing space
        # content = re.sub("[^\x00-\x7F]+", " ", content) # remove unicode characters
        content = re.sub("\s+", " ", content) # remove multiple spaces
        return content