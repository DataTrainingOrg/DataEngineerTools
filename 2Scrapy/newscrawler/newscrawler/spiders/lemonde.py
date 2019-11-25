# -*- coding: utf-8 -*-
import scrapy


class LemondeSpider(scrapy.Spider):
    name = 'lemonde'
    allowed_domains = ['lemonde.fr']
    start_urls = ['http://lemonde.fr/']

    def parse(self, response):
        pass
