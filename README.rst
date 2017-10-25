A sample python project to demonstrate how to scrape using Scrapy
=======================

1. It's a step by step demo scraper project using Scrapy. I will show how to scrape news from a popular online news portal [https://bdnews24.com] from Bangladesh.
2. Go to demo/news/spiders and see the spiders. Commands to run the spiders will be found inside the files.
3. Spider ``bdnews24_spider_7.py`` can download the news on some category. Provide category in line number 10 of startup.py. If you want to scrape periodically you can make it a commandline tool using following commands and then run the command whenever you need.


### Commands:
1. clean    : ``python setup.py clean``
2. build    : ``python setup.py sdist``
      or      ``python setup.py bdist_wheel``
3. install  : ``cd dist/```
         &    ``pip install demo-x.x.x.tar.gz``
4. run      : ``demo``
5. uninstall: ``pip uninstall demo``
