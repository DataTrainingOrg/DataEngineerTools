from pymongo import MongoClient
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_product_details_from_url(asin):
    url = f"https://www.amazon.fr/dp/{asin}"
    
    headers = {
        "User-Agent":     "Mozilla/4.0 (compatible; MSIE 6.0; Windows 2000)"# get_random_user_agent()
    }

    # Envoi de la requête avec un User-Agent aléatoire
    # random_delay()

    response = requests.get(url, headers=headers)

    # Vérification de la réponse
    if response.status_code == 200:
        print(f"Page fetch réussie pour l'ASIN {asin} avec User-Agent: {headers['User-Agent']}")

        # Parser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        
        price_whole = soup.find("span", class_="a-price-whole")
        price_fraction = soup.find("span", class_="a-price-fraction")
        price = f"{price_whole.text.strip()}{price_fraction.text.strip()} €" if price_whole and price_fraction else "Prix non trouvé"

        # Retourner les informations récupérées
        return price
    else:
        print(f"Échec de la récupération de la page pour l'ASIN {asin}. Code d'état : {response.status_code}.")
        return None
    

print(scrape_product_details("B0BBJ59WJ4"))