# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LeboncoinItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()

if __name__ == "__main__":
    lbc_item = LeboncoinItem(title="Drone DJI", price="100€")
    print(type(lbc_item))
    dict_item = dict(lbc_item)
    print(type(dict_item))
    print(dict_item)
