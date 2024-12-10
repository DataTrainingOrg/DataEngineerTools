import scrapy


class LemondeSpider(scrapy.Spider):
    name = "lemonde"
    allowed_domains = ["lemonde.fr"]
    start_urls = ["https://lemonde.fr"]

    def parse(self, response):
        title = response.css('title::text').extract_first()
        all_links = {
            name: response.urljoin(url) for name, url in zip(
                response.css("#nav-markup .Nav__item")[3].css("a::text").extract(),
                response.css("#nav-markup .Nav__item")[3].css("a::attr(href)").extract())
        }
        yield {
            "title": title,
            "all_links": all_links
        }