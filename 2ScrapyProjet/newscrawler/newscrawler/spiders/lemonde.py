import scrapy


class LemondeSpider(scrapy.Spider):
    name = "lemonde"
    allowed_domains = ["lemonde.fr"]
    start_urls = ["https://lemonde.fr"]

    def parse(self, response):
        pass
