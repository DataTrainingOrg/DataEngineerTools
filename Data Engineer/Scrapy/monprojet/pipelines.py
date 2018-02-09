# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import pymongo


class PricePipeline(object):

    def process_item(self, item, spider):
        if item['price']:
            item["price"] = int(item["price"].replace("€", "").replace(" ", "").strip())
            return item
        else:
            raise DropItem("Missing price in %s" % item)


class TextPipeline(object):

    def process_item(self, item, spider):
        if item['title']:
            item["title"] = clean_spaces(item["title"])
            item["price"] = clean_spaces(item["price"])
            return item
        else:
            raise DropItem("Missing title in %s" % item)


class MongoPipeline(object):

    collection_name = 'scrapy_items'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient()
        self.db = self.client["leboncoin"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item


def clean_spaces(string):
    if string:
        return " ".join(string.split())
