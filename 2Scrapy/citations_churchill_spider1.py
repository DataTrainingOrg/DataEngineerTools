import scrapy

class ChurchillQuotesSpider(scrapy.Spider):
    name = "citations_de_churchill"
    start_urls = ["http://evene.lefigaro.fr/citations/winston-churchill"]

    def parse(self, response):
        for cit in response.xpath('//div[@class="figsco__quote__text"]'):
            text_value = cit.xpath('a/text()').extract_first()  # Citation
            if text_value:
                text_value = text_value.replace('“', '').replace('”', '')

            # Accéder au parent pour récupérer l'auteur
            autor = cit.xpath(
                '../div[@class="figsco__quote__from figsco__row"]'
                '//div[@class="figsco__fake__col-9"]/a/text()'
            ).extract_first()

            yield {
                'text': text_value,
                'autor': autor
            }


