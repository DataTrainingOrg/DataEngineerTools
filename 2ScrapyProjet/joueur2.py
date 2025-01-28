import scrapy
import json

class TransfermarktPlayerSpider(scrapy.Spider):
    name = "player_info"

    # Définir les URLs de base
    base_url1 = "https://www.transfermarkt.fr/ousmane-dembele/profil/spieler/"
    base_url2 = "https://www.transfermarkt.fr/ousmane-dembele/leistungsdaten/spieler/"

    # Paramètres pour l'agent utilisateur
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    # Listes pour stocker les informations dans les fichiers JSON séparés
    player_info_list = []
    career_performance_list = []

    def start_requests(self):
        # Générer une liste d'URLs pour les 100 premières pages (en partant de l'ID du joueur 1 à 100) pour les deux URLs
        for player_id in range(1, 10000):
            # Pour la première URL (player info)
            url_1 = f"{self.base_url1}{player_id}"
            yield scrapy.Request(url_1, callback=self.parse_player_info, meta={'player_id': player_id})

            # Pour la deuxième URL (career performance)
            url_2 = f"{self.base_url2}{player_id}/plus/0?saison=ges"
            yield scrapy.Request(url_2, callback=self.parse_career_performance, meta={'player_id': player_id})

    def parse_player_info(self, response):
        player_id = response.meta['player_id']

        # Extraire les informations personnelles du joueur
        player_info = {
            "Nom": response.xpath(
                '//tm-userbox/@page-title').get().split(" |")[0],
            "Nom dans le pays d\'origine": response.xpath(
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

        # Ajouter les informations du joueur à la liste
        self.player_info_list.append({
            "player_id": player_id,
            "Player Info": player_info
        })

    def parse_career_performance(self, response):
        player_id = response.meta['player_id']

        # Extraire les données de performance sur l'ensemble de la carrière
        career_performance = []

        for row in response.xpath('//table[@class="items"]/tbody/tr'):
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

            if competition_info:
                career_performance.append(competition_info)

        # Ajouter les données de carrière à la liste
        self.career_performance_list.append({
            "player_id": player_id,
            "Career Performance": career_performance
        })

        # Lorsque les deux informations sont récupérées, sauvegarder les données dans les fichiers JSON
        if self.player_info_list and self.career_performance_list:
          self.save_to_json()
          
        

    def save_to_json(self):
        # Enregistrer les informations des joueurs dans un fichier JSON
        with open('player_info.json', 'w', encoding='utf-8') as f:
            json.dump(self.player_info_list, f, ensure_ascii=False, indent=4)
    
        # Extraire les player_id distincts de player_info_list
        player_info_ids = set([item["player_id"] for item in self.player_info_list])
        print(f"Nombre de player_id distincts dans player_info.json: {len(player_info_ids)}")
    

        # Enregistrer les performances de carrière dans un fichier JSON
        with open('career_performance.json', 'w', encoding='utf-8') as f:
            json.dump(self.career_performance_list, f, ensure_ascii=False, indent=4)
    
        # Extraire les player_id distincts de career_performance_list
        career_performance_ids = set([item["player_id"] for item in self.career_performance_list])
        print(f"Nombre de player_id distincts dans career_performance.json: {len(career_performance_ids)}")
    
       
    
    


