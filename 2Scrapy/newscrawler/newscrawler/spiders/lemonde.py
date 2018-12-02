# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import ArticleItem
class LemondeSpider(scrapy.Spider):
    name = "lemonde"
    allowed_domains = ["www.lemonde.fr"]
    start_urls = ['https://www.lemonde.fr']

    def parse(self, response):
        title = response.css('title::text').extract_first()
        all_links = {
            name:response.urljoin(url) for name, url in zip(
            response.css("#nav-markup .Nav__item")[3].css("a::text").extract(),
            response.css("#nav-markup .Nav__item")[3].css("a::attr(href)").extract())
        }
        for link in all_links.values():
            yield Request(link, callback=self.parse_category)

    def parse_category(self, response):
        for article in response.css(".fleuve")[0].css("article"):
            title = article.css("h3 a::text").extract_first()
            image = article.css("img::attr(data-src)").extract_first()
            description = article.css(".txt3::text").extract_first()
            #yield {
            #    "title":title,
            #    "image":image,
            #    "description":description
            #}

            yield ArticleItem(
                title=title,
                image=image,
                description=description
            )

    def clean_spaces(self, string):
        if string:
            return " ".join(string.split())
            
