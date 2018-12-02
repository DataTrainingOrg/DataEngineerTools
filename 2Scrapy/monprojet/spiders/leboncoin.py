# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from ..items import LeboncoinItem


class LeboncoinSpider(scrapy.Spider):
    name = "leboncoin"
    allowed_domains = ["leboncoin.fr"]
    start_urls = ['http://leboncoin.fr/']

    def parse(self, response):
        title = response.css('title::text').extract_first()
        all_links = [response.urljoin(url) for url in response.css(".mapNav li a::attr(href)").extract()]
        for link in all_links:
            yield Request(link, callback=self.parse_region)

    def parse_region(self, response):
        for item in response.css(".tabsContent li .item_infos"):
            title = item.css(".item_title::text").extract_first()
            price = item.css(".item_price::text").extract_first()
            yield LeboncoinItem(price=price, title=title)