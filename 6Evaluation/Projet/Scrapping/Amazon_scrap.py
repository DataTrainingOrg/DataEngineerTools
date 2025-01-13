import requests
from bs4 import BeautifulSoup
import time
import random


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


# Fonction pour scraper les détails d'un produit via son URL spécifique (ASIN)
def scrape_product_details_from_url(url):
    headers = {"User-Agent": get_random_user_agent()}

    random_delay()  # Ajouter un délai aléatoire entre les requêtes

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"Page fetch réussie pour l'url {url} avec User-Agent: {headers['User-Agent']}")

        # Parser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extraire le prix
        price_whole = soup.find("span", class_="a-price-whole")
        price_fraction = soup.find("span", class_="a-price-fraction")
        price = f"{price_whole.text.strip()}{price_fraction.text.strip()} €" if price_whole and price_fraction else "Prix non trouvé"

        # Extraire le nom du produit
        title_element = soup.find("span", id="productTitle")
        product_name = title_element.text.strip() if title_element else "Nom du produit non trouvé"

        # Extraire l'ASIN (souvent stocké dans les meta ou l'URL)
        asin_element = soup.find("input", attrs={"id": "ASIN"})
        asin = asin_element["value"] if asin_element else "ASIN non trouvé"

        # Retourner les informations récupérées
        return {
            "product_name": product_name,
            "price": price,
            "asin": asin
        }
    else:
        print(f"Échec de la récupération de la page pour l'url {url}. Code d'état : {response.status_code}.")
        return None
def scrape_price_from_asin(asin):
    url = f"https://www.amazon.fr/dp/{asin}"
    headers = {"User-Agent": get_random_user_agent()}

    random_delay()  # Ajouter un délai aléatoire entre les requêtes

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"Page fetch réussie pour l'ASIN {asin} avec User-Agent: {headers['User-Agent']}")

        # Parser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extraire le prix
        price_whole = soup.find("span", class_="a-price-whole")
        price_fraction = soup.find("span", class_="a-price-fraction")
        price = f"{price_whole.text.strip()}{price_fraction.text.strip()} €" if price_whole and price_fraction else "Prix non trouvé"

        # Retourner le prix récupéré
        return price
    else:
        print(f"Échec de la récupération de la page pour l'ASIN {asin}. Code d'état : {response.status_code}.")
        return None


# Fonction pour scraper un produit par son nom de catégorie
def scrape_product_by_name(product_name):
    url = f"https://www.amazon.fr/s?k={product_name}"  # Construire l'URL de recherche
    headers = {"User-Agent": get_random_user_agent()}

    random_delay()  # Ajouter un délai aléatoire entre les requêtes

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"Page fetch réussie pour {product_name} avec User-Agent: {headers['User-Agent']}")

        # Parser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Trouver les conteneurs de produits
        product_containers = soup.find_all("div", {"data-component-type": "s-search-result"})
        if product_containers:
            results = []
            for product in product_containers:
                # Extraire le titre du produit
                title_element = product.find("a", class_="a-link-normal s-no-outline")
                title = title_element.find("img")["alt"] if title_element and title_element.find("img") else "Titre non trouvé"
                # Extraire le prix
                price_whole = product.find("span", class_="a-price-whole")
                price_fraction = product.find("span", class_="a-price-fraction")
                price = f"{price_whole.text.strip()}{price_fraction.text.strip()} €" if price_whole and price_fraction else "Prix non trouvé"

                # Extraire l'ASIN
                asin = product["data-asin"] if "data-asin" in product.attrs else "ASIN non trouvé"

                # Ajouter les détails du produit à la liste des résultats
                r={
                    "product_name": title,
                    "price": price,
                    "asin": asin
                }
                results.append(r)
            return results
        else:
            print(f"Aucun produit trouvé pour {product_name}.")
            return []
    else:
        print(f"Échec de la récupération de la page pour {product_name}. Code d'état : {response.status_code}.")
        return []

# Fonction pour compter le nombre de produits sur une page de recherche Amazon
def count_products_on_page(product_name):
    url = f"https://www.amazon.fr/s?k={product_name}"  # Construire l'URL de recherche
    headers = {"User-Agent": get_random_user_agent()}

    random_delay()  # Ajouter un délai aléatoire entre les requêtes

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"Page fetch réussie pour {product_name} avec User-Agent: {headers['User-Agent']}")

        # Parser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Trouver les conteneurs de produits
        product_containers = soup.find_all("div", {"data-component-type": "s-search-result"})
        
        # Retourner le nombre de produits trouvés
        return len(product_containers)
    else:
        print(f"Échec de la récupération de la page pour {product_name}. Code d'état : {response.status_code}.")
        return 0


# Fonction pour scraper les détails d'un produit, y compris l'image, via son URL
def scrape_product_details_with_image(url):
    headers = {"User-Agent": get_random_user_agent()}
    random_delay()  # Ajouter un délai aléatoire entre les requêtes

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(f"Page fetch réussie pour l'url {url} avec User-Agent: {headers['User-Agent']}")

        # Parser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extraire le prix
        price_whole = soup.find("span", class_="a-price-whole")
        price_fraction = soup.find("span", class_="a-price-fraction")
        price = f"{price_whole.text.strip()}{price_fraction.text.strip()} €" if price_whole and price_fraction else "Prix non trouvé"

        # Extraire le nom du produit
        title_element = soup.find("span", id="productTitle")
        product_name = title_element.text.strip() if title_element else "Nom du produit non trouvé"

        # Extraire l'ASIN
        asin_element = soup.find("input", attrs={"id": "ASIN"})
        asin = asin_element["value"] if asin_element else "ASIN non trouvé"

        # Extraire l'URL de l'image
        image_element = soup.find("img", id="landingImage")
        image_url = image_element["src"] if image_element else "Image non trouvée"

        # Retourner les informations récupérées
        return {
            "product_name": product_name,
            "price": price,
            "asin": asin,
            "image_url": image_url
        }
    else:
        print(f"Échec de la récupération de la page pour l'url {url}. Code d'état : {response.status_code}.")
        return None

