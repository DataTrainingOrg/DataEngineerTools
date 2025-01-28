import scrapy


class TransfermarktNewsSpider(scrapy.Spider):
    name = "actualite"
    start_urls = ["https://www.transfermarkt.fr/"]

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    def parse(self, response):
        # Cibler chaque élément de type "swiper-slide"
        for slide in response.xpath('//div[contains(@class, "swiper-slide")]'):
            # Extraire le titre de la news
            title = slide.xpath('.//div[@class="news-big-headline"]/text()').get()
            
            # Extraire la catégorie (e.g., "LIGUE 1")
            category = slide.xpath('.//div[@class="newsSubline"]/span[@class="text"]/text()').get()
            
            # Extraire le lien vers l'article
            link = slide.xpath('.//a[@class="newsslider-hauptlink"]/@href').get()
            
            # Extraire l'image associée
            image = slide.xpath('.//div[contains(@class, "slider-foto")]/@style').re_first(r'url\((.+)\)')

            yield {
                'title': title.strip() if title else None,
                'category': category.strip() if category else None,
                'link': response.urljoin(link) if link else None,
                'image': image.strip() if image else None,
            }
