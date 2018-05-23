# Instructions

The job consists of scraping real estate listings from a website using Scrapy 1.5.0.

This is the page: http://www.haagen-partners.nl/huurwoningen/?city=Amsterdam

In this project there are two spiders already defined:

* www.principlevastgoed.nl: this spider is provided as an example. It contains comments to explain how the work needs to be done. It is recommended to run this spider to see how the output is generated.
* www.haagen-partners.nl: this spider is another example.

### Requirements

- Only use xpath queries to extract the information.
- Do not change the names of the items to be extracted.
- Do not generate a new spider. Instead, use the files provided.
- Please use the scrapy project provided in this folder. You don't need to create a new scrapy project.
- Do not modify any of the other files provided, only the spiders requested.
- Please take a look at the example before starting.

### Deliverables

There is only one file you need to deliver, the file that contains the spider. This file must contain all necesary code to extract the information requested.
In order to validate the spider, I will execute 

> scrapy crawl [spider] -o result.json

The result file must contain the scraped items in the format of the file `example_result.json` provided as the result of the example spider
