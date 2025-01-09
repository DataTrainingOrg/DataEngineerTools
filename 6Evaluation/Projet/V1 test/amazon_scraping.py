import requests
from bs4 import BeautifulSoup
import time
import random
from read_write_mongodb import *

# Liste des produits à surveiller
products_to_scrape = [
    "processeur",
    "carte_graphique",
    "carte_mere",
    "memoire_vive",
    "disque_dur",
    "boitier_pc"
]

# Liste des User-Agents fonctionnels
user_agents = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 4.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows 98)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows 2000)"
]

# Fonction pour ajouter un délai aléatoire
def random_delay():
    delay = random.uniform(2, 5)  # Délai aléatoire entre 2 et 5 secondes
    time.sleep(delay)

# Fonction pour sélectionner un User-Agent aléatoire
def get_random_user_agent():
    return random.choice(user_agents)


def scrape_product_details_from_url(asin):
    url = f"https://www.amazon.fr/dp/{asin}"
    
    headers = {
        "User-Agent": get_random_user_agent()
    }

    # Envoi de la requête avec un User-Agent aléatoire
    random_delay()

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




# Fonction pour scraper un produit spécifique
def scrape_product(product_name):
    url = f"https://www.amazon.fr/s?k={product_name}"  # Utiliser le nom du produit pour la recherche
    
    headers = {
        "User-Agent": get_random_user_agent()
    }

    # Envoi de la requête avec un User-Agent aléatoire
    random_delay()

    response = requests.get(url, headers=headers)

    # Vérification de la réponse
    if response.status_code == 200:
        print(f"Page fetched successfully for {product_name} with User-Agent: {headers['User-Agent']}")
        
        # Parser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Trouver les conteneurs des produits
        product_containers = soup.find_all("div", class_="s-main-slot s-result-list s-search-results sg-row")
        
        if product_containers:
            print(f"{len(product_containers)} conteneur(s) de produits trouvé(s) pour {product_name}.\n")
            
            # Parcourir les produits dans le premier conteneur
            for product in product_containers[0].find_all("div", {"data-component-type": "s-search-result"}):
                # Extraire le titre
                title_element = product.find("a", class_="a-link-normal s-no-outline")
                title = title_element.find("img")["alt"] if title_element and title_element.find("img") else "Titre non trouvé"

                # Extraire le prix
                price_whole = product.find("span", class_="a-price-whole")
                price_fraction = product.find("span", class_="a-price-fraction")
                price = f"{price_whole.text.strip()}{price_fraction.text.strip()} €" if price_whole and price_fraction else "Prix non trouvé"

                # Extraire l'ancien prix (si disponible)
                old_price_section = product.find("div", class_="a-section aok-inline-block")
                if old_price_section:
                    old_price = old_price_section.find("span", class_="a-price a-text-price")
                    old_price = old_price.find("span", class_="a-offscreen").text.strip() if old_price and old_price.find("span", class_="a-offscreen") else "Ancien prix non disponible"
                else:
                    old_price = "Ancien prix non disponible"

                # Extraire le lien vers le produit
                product_link = title_element["href"] if title_element else "Lien non disponible"
                product_url = f"https://www.amazon.fr{product_link}" if product_link != "Lien non disponible" else "Lien non disponible"

                # Extraire l'ASIN du produit (généralement présent dans l'URL)
                asin = product_url.split("/dp/")[1].split("/")[0] if "/dp/" in product_url else None
                
                # Afficher les informations du produit
                turn_all_need_update_on(product_name)
                print(f"Titre: {title}")
                if is_product_in_db(product_name, asin):
                    update_product_price(product_name, asin, price)
                else:
                    insert_product_data(product_name, asin, title, price, product_url)
                # print(f"Ancien Prix : {old_price}")
                print("-" * 40)
        else:
            print(f"Aucun produit trouvé pour {product_name}.")
    else:
        print(f"Échec de la récupération de la page pour {product_name}. Code d'état : {response.status_code}.")
    

# Scraper chaque produit de la liste
for product_name in products_to_scrape:
    scrape_product(product_name)
    # Scraper les produits hors liste
    print("traitement hors liste :\n")
    list_product=get_and_reset_needs_update(product_name)
    for product in list_product:
        prix=scrape_product_details_from_url(product)
        update_product_price(product_name, product, prix)
    print("done\n")
