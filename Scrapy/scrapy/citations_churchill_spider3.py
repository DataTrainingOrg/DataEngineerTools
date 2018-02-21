# citations_churchill_spider3.py

import scrapy

class ChurchillQuotesSpider(scrapy.Spider):
    name = "citations de Churchill"
    start_urls = ["http://evene.lefigaro.fr/citations/winston-churchill",]

    def parse(self, response):
        for cit in response.xpath('//article'):
            text_value = cit.xpath('div[@class="figsco__quote__text"]/a/text()').extract_first()
            if text_value:
                text_value = text_value.replace('“', '').replace('”', '')
            author_value = cit.xpath('div/div[@class="figsco__fake__col-9"]/a/text()').extract_first()
            yield { 'text' : text_value,
                    'author' : author_value }

        xpath_expression = '//li[@class="figsco__evene__search__pager last"]/a/@href'
        next_page = response.xpath(xpath_expression).extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


# <li class="figsco__evene__search__pager last"><a href="/citations/winston-churchill?page=2" title="Aller à la page suivante" rel="next" class="active">›</a></li>