import requests
from bs4 import BeautifulSoup
import time
import random
from mongodb_product_tracker import MongoDBHandler

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

# Fonction pour scraper les produits d'une page de boutique Amazon
def scrape_amazon_store_page(store_url):
    headers = {"User-Agent": get_random_user_agent()}
    random_delay()  # Ajouter un délai pour éviter les blocages
    try:
        response = requests.get(store_url, headers=headers)
        response.raise_for_status()  # Vérifier si le code de statut est 200
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de la page de la boutique : {e}")
        return []

    if response.status_code == 200:
        print("Page trouvée.")
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            products = []

            # Localiser les conteneurs des produits
            product_containers = soup.find_all("div", class_="s-main-slot s-result-list s-search-results sg-row")
            if not product_containers:
                print("Aucun produit trouvé sur la page.")
                return []

            for product in product_containers:
                # Extraire le titre du produit
                title_element = product.find("span", class_="a-size-base-plus")
                title = title_element.text.strip() if title_element else "Titre non trouvé"

                # Extraire le prix du produit
                price_whole = product.find("span", class_="a-price-whole")
                price_fraction = product.find("span", class_="a-price-fraction")
                price = f"{price_whole.text.strip()}{price_fraction.text.strip()} €" if price_whole and price_fraction else "Prix non trouvé"

                # Extraire le lien vers le produit
                link_element = product.find("a", class_="a-link-normal")
                product_url = f"https://www.amazon.fr{link_element['href']}" if link_element else "Lien non trouvé"

                # Ajouter les informations extraites au tableau des produits
                products.append({
                    "title": title,
                    "price": price,
                    "url": product_url
                })

            return products
        except Exception as e:
            print(f"Erreur lors de l'analyse du contenu de la page : {e}")
            return []
    else:
        print(f"Erreur lors de la récupération de la page. Code d'état : {response.status_code}")
        return []

# Fonction pour scraper les détails d'un produit à partir de son ASIN
def scrape_product_details_from_url(asin):
    url = f"https://www.amazon.fr/dp/{asin}"
    headers = {"User-Agent": get_random_user_agent()}

    random_delay()
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Vérifier si le code de statut est 200
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de la page pour l'ASIN {asin} : {e}")
        return None

    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            price_whole = soup.find("span", class_="a-price-whole")
            price_fraction = soup.find("span", class_="a-price-fraction")
            price = f"{price_whole.text.strip()}{price_fraction.text.strip()} €" if price_whole and price_fraction else None
            return price
        except Exception as e:
            print(f"Erreur lors de l'analyse du produit pour l'ASIN {asin}: {e}")
            return None
    else:
        print(f"Échec de la récupération de la page pour l'ASIN {asin}. Code d'état : {response.status_code}.")
        return None

# Fonction pour scraper les produits d'une recherche
def scrape_product(db_handler, collection_name, product_name):
    url = f"https://www.amazon.fr/s?k={product_name}"
    headers = {"User-Agent": get_random_user_agent()}

    random_delay()
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Vérifier si le code de statut est 200
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de la page de recherche pour {product_name}: {e}")
        return

    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.text, "html.parser")
            product_containers = soup.find_all("div", class_="s-main-slot s-result-list s-search-results sg-row")

            if not product_containers:
                print(f"Aucun produit trouvé pour {product_name}.")
                return

            for product in product_containers[0].find_all("div", {"data-component-type": "s-search-result"}):
                title_element = product.find("a", class_="a-link-normal s-no-outline")
                title = title_element.find("img")["alt"] if title_element and title_element.find("img") else "Titre non trouvé"

                price_whole = product.find("span", class_="a-price-whole")
                price_fraction = product.find("span", class_="a-price-fraction")
                price = f"{price_whole.text.strip()}{price_fraction.text.strip()} €" if price_whole and price_fraction else None

                product_link = title_element["href"] if title_element else None
                product_url = f"https://www.amazon.fr{product_link}" if product_link else None

                asin = product_url.split("/dp/")[1].split("/")[0] if product_url and "/dp/" in product_url else None

                if asin and price:
                    if db_handler.is_product_in_db(collection_name, asin):
                        db_handler.update_product_price(collection_name, asin, price)
                    else:
                        db_handler.insert_product_data(collection_name, asin, title, price, product_url)
        except Exception as e:
            print(f"Erreur lors de l'analyse des produits pour {product_name}: {e}")
    else:
        print(f"Échec de la récupération de la page pour {product_name}. Code d'état : {response.status_code}.")

# Fonction principale pour gérer le scraping
def main():
    db_handler = MongoDBHandler()

    # for product_name in products_to_scrape:
    #     scrape_product(db_handler, product_name, product_name)

    # print("Traitement terminé.")

if __name__ == "__main__":
    store_url = "https://www.amazon.fr/stores/page/D88E2FF3-48B1-4191-986D-9C4100149487"
    products = scrape_amazon_store_page(store_url)

    if products:
        for product in products:
            print(f"Titre : {product['title']}")
            print(f"Prix : {product['price']}")
            print(f"Lien : {product['url']}")
            print("-" * 40)
    else:
        print("Aucun produit trouvé ou erreur dans le scraping.")
