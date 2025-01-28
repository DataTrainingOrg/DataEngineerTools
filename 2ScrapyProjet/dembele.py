import scrapy
import json

class TransfermarktPlayerSpider(scrapy.Spider):
    name = "player_info"
    start_urls = [
        "https://www.transfermarkt.fr/ousmane-dembele/profil/spieler/288230",
        "https://www.transfermarkt.fr/ousmane-dembele/leistungsdaten/spieler/288230/plus/0?saison=ges"  # Nouvelle page pour la performance de carrière
    ]

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    def parse(self, response):
        if response.url == self.start_urls[0]:
            # Extraire le nom du joueur depuis la balise tm-userbox
            player_name = response.xpath(
                '//tm-userbox/@page-title').get()  # Extrait l'attribut page-title qui contient le nom complet
            if player_name:
                player_name = player_name.split(" |")[0]  # Nettoyage du nom en retirant le texte supplémentaire "Profil du joueur"
            
            # Extraire les informations personnelles du joueur
            player_info = {
                "Nom": player_name,
                "Nom dans le pays d'origine": response.xpath(
                    '//span[text()="Nom dans le pays d\'origine:"]/following::span[@class="info-table__content info-table__content--bold"]/text()'
                ).get(),
                "Naissance (âge)": response.xpath(
                    '//span[text()="Naissance (âge):"]/following::span[@class="info-table__content info-table__content--bold"]/a/text()'
                ).get(),
                "Lieu de naissance": response.xpath(
                    '//span[text()="Lieu de naissance:"]/following::span[@class="info-table__content info-table__content--bold"]/span/text()'
                ).get(),
                "Taille": response.xpath(
                    '//span[text()="Taille:"]/following::span[@class="info-table__content info-table__content--bold"]/text()'
                ).get(),
                "Pied": response.xpath(
                    '//span[text()="Pied:"]/following::span[@class="info-table__content info-table__content--bold"]/text()'
                ).get(),
                "Membre depuis": response.xpath(
                    '//span[text()="Membre depuis:"]/following::span[@class="info-table__content info-table__content--bold"]/text()'
                ).get(),
                "Contrat jusqu’à": response.xpath(
                    '//span[text()="Contrat jusqu’à:"]/following::span[@class="info-table__content info-table__content--bold"]/text()'
                ).get(),
                "Équipementier": response.xpath(
                    '//span[text()="Équipementier:"]/following::span[@class="info-table__content info-table__content--bold"]/text()'
                ).get(),
                "Club actuel": response.xpath(
                    '//span[@class="info-table__content info-table__content--bold info-table__content--flex"]/a[@title]/text()'
                ).get()
            }

            # Nettoyage des données personnelles
            player_info = {
                key: (" ".join(value).strip() if isinstance(value, list) else value.strip()) 
                for key, value in player_info.items() if value and value.strip()
            }

            # Extraire les informations de la carrière nationale
            national_career = []
            for row in response.xpath('//div[@class="grid national-career__row"]'):
                career_info = {
                    "Numéro": row.xpath('.//div[contains(@class, "national-career__cell--green")]/text()').get()
                    or row.xpath('.//div[contains(@class, "national-career__cell--yellow")]/text()').get()
                    or row.xpath('.//div[contains(@class, "national-career__cell--red")]/text()').get(),
                    "Équipe nationale": row.xpath('.//div[@class="grid__cell grid__cell--club"]/a/text()').get(),
                    "Début": row.xpath('.//div[@class="grid__cell grid__cell--center"]/a/text()').get(),
                    "Matchs": row.xpath('.//div[@class="grid__cell grid__cell--center"][2]/a/text()').get(),
                    "Buts": row.xpath('.//div[@class="grid__cell grid__cell--center"][3]/a/text()').get()
                }

                national_career.append(career_info)

            # Nettoyage des données de carrière nationale
            national_career = [
                {key: (value.strip() if value else None) for key, value in career.items()} 
                for career in national_career
            ]

            yield {
                "Player Info": player_info,
                "National Career": national_career,
            }

        elif response.url == self.start_urls[1]:
            # Extraire les données de performance sur l'ensemble de la carrière
            career_performance = []

            for row in response.xpath('//table[@class="items"]/tbody/tr'):
                # Extraire les informations des colonnes
                competition_info = {
                    "Compétition": row.xpath('.//td[@class="hauptlink no-border-links"]/a/text()').get(),
                    "Matchs": row.xpath('.//td[@class="zentriert player-profile-performance-data"]/a/text()').get(),  # Nombre total de matchs
                    "Buts": row.xpath('.//td[@class="zentriert"][1]/text()').get(),  # Buts
                    "Passes décisives": row.xpath('.//td[@class="zentriert"][2]/text()').get(),  # Passes décisives
                    "Cartons jaunes": row.xpath('.//td[@class="zentriert"][3]/text()').get(),  # Cartons jaunes
                    "Cartons jaunes/rouges": row.xpath('.//td[@class="zentriert"][4]/text()').get(),  # Cartons jaunes/rouges
                    "Cartons rouges": row.xpath('.//td[@class="zentriert"][5]/text()').get(),  # Cartons rouges
                    "Minutes jouées": row.xpath('.//td[@class="rechts"]/text()').get()  # Minutes jouées
                }

                # Remplacer les `-` par `0` et supprimer les lignes avec des valeurs nulles
                competition_info = {key: (value if value != "-" else "0") for key, value in competition_info.items()}
                competition_info = {key: value for key, value in competition_info.items() if value not in [None, "null"]}

                # Si la ligne contient des données valides, l'ajouter à la liste
                if competition_info:
                    career_performance.append(competition_info)

            yield {
                "Career Performance": career_performance
            }
