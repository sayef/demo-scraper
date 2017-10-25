# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import time
from scrapy.exceptions import DropItem


class NewsPipeline(object):
    def process_item(self, item, spider):
        return item

class BDNewsPipeline(object):
    # ids seen so far for duplicate checking
    def __init__(self):
        self.ids_seen = set()

    # Overridden : Checking duplicate items, whether already exists in db etc
    def process_item(self, item, spider):
        if item['news_content_id'] is not None:
            if self.item_exists(item['news_content_id']) is True:
                raise DropItem("Item %s already exists!" % item)
            elif item['news_content_id'] in self.ids_seen:
                raise DropItem("Item already found: %s" % item)
            else:
                line = json.dumps(dict(item)) + "\n"
                self.file.write(bytearray(line.encode('utf-8')))
                self.ids_seen.add(item['news_content_id'])
                return item
        else:
            raise DropItem("Item %id not found!")

    # Overridden : write items in a jsonline file
    def open_spider(self, spider):
        self.file = open('tech7-' + str(time.time()) + '.jl', 'wb')

    def close_spider(self, spider):
        self.file.close()

    # Need service implementation
    def item_exists(self, content_id):
        return False