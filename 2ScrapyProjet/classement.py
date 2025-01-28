import scrapy

class TransfermarktPlayersSpider(scrapy.Spider):
    name = "players"
    start_urls = ["https://www.transfermarkt.fr/uefa-champions-league/marktwerte/pokalwettbewerb/CL/pos//detailpos/0/altersklasse/alle"]

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    def parse(self, response):
        # Cibler toutes les lignes du tableau
        rows = response.xpath('//tr[@class="odd"] | //tr[@class="even"]')

        for row in rows:
            # Extraire le rang
            rank = row.xpath('.//td[@class="zentriert"]/text()').get()
            
            # Extraire le nom du joueur et son lien
            player_name = row.xpath('.//td[@class="hauptlink"]/a/text()').get()
            player_link = row.xpath('.//td[@class="hauptlink"]/a/@href').get()
            
            # Extraire le poste
            position = row.xpath('.//td[@class="hauptlink"]/following-sibling::td[1]/text()').get()
            
            # Extraire le pays du joueur
            country_flag = row.xpath('.//td[@class="zentriert"]/following-sibling::td[1]/img/@title').get()
            
            # Extraire l'âge du joueur
            age = row.xpath('.//td[@class="zentriert"]/following-sibling::td[2]/text()').get()
            
            # Extraire le club et le lien vers le club
            club = row.xpath('.//td[@class="zentriert"]/following-sibling::td[3]//a/@title').get()
            club_link = row.xpath('.//td[@class="zentriert"]/following-sibling::td[3]//a/@href').get()
            
            # Extraire la valeur marchande
            market_value = row.xpath('.//td[@class="rechts hauptlink"]/a/text()').get()

            # Yield les données extraites
            yield {
                'rank': rank.strip() if rank else None,
                'player_name': player_name.strip() if player_name else None,
                'player_link': response.urljoin(player_link) if player_link else None,
                'position': position.strip() if position else None,
                'country_flag': country_flag.strip() if country_flag else None,
                'age': age.strip() if age else None,
                'club': club.strip() if club else None,
                'club_link': response.urljoin(club_link) if club_link else None,
                'market_value': market_value.strip() if market_value else None
            }
