# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem
import pymongo

class TextPipeline(object):

    def process_item(self, item, spider):
        if item['title']:
            item["title"] = clean_spaces(item["title"])
            return item
        else:
            raise DropItem("Missing title in %s" % item)


def clean_spaces(string):
    if string:
        return " ".join(string.split())


class MongoPipeline(object):

    collection_name = 'scrapy_items'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient()
        self.db = self.client["lemonde"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item