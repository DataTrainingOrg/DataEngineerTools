import scrapy
from scrapy import Request


class LemondeSpider(scrapy.Spider):
    name = "lemondev2"
    allowed_domains = ["www.lemonde.fr"]
    start_urls = ['https://www.lemonde.fr']

    def parse(self, response):
        title = response.css('title::text').extract_first()
        all_links = {
            name:response.urljoin(url) for name, url in zip(
            response.css("#nav-markup .Nav__item")[3].css("a::text").extract(),
            response.css("#nav-markup .Nav__item")[3].css("a::attr(href)").extract())
        }
        yield {
            "title":title,
            "all_links":all_links
        }
        