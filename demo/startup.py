from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from demo.news.spiders import bdnews24_spider_7


def main():
    configure_logging()
    runner = CrawlerRunner()
    runner.crawl(bdnews24_spider_7.Tech7Spider, category='technology')
    # runner.crawl()
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    # the script will block here until all crawling jobs are finished
    reactor.run()

if __name__ == '__main__':
    main()