# citations_churchill_spider1.py

import scrapy

class ChurchillQuotesSpider(scrapy.Spider):
    name = "citations de Churchill"
    start_urls = ["http://evene.lefigaro.fr/citations/winston-churchill",]

    def parse(self, response):
        # print('response =', response)
        # print(dir(response))
        # print(response.text)
        for cit in response.xpath('//div[@class="figsco__quote__text"]'):
            # print('###', cit)
            text_value = cit.xpath('a/text()').extract_first().replace('“', '').replace('”', '')
            yield { 'text' : text_value }

            