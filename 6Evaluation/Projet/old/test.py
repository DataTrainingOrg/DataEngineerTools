import requests
from bs4 import BeautifulSoup
import time
import random

# URL de la page Amazon à scraper
url = "https://www.amazon.fr/s?k=processeur"  # Remplace "produit" par le terme recherché

# User-Agent pour IE6
headers = {
    "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"
}

# Fonction pour ajouter un délai aléatoire
def random_delay():
    delay = random.uniform(2, 5)  # Délai aléatoire entre 2 et 5 secondes
    time.sleep(delay)

# Envoi de la requête
response = requests.get(url, headers=headers)

# Vérification de la réponse
if response.status_code == 200:
    print("Page fetched successfully!")
    # print(response.text[:5000])

    # Parser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Trouver le titre principal de la page
    page_title = soup.title.text if soup.title else "Titre de la page non trouvé"
    print(f"Titre de la page : {page_title}\n")

    # Trouver les conteneurs principaux des produits
    product_containers = soup.find_all("div", class_="s-main-slot s-result-list s-search-results sg-row")

    if product_containers:
        print(f"{len(product_containers)} conteneur(s) de produits trouvé(s).\n")

        # Parcourir les produits dans le premier conteneur trouvé
        for product in product_containers[0].find_all("div", {"data-component-type": "s-search-result"}):
            # Ajouter un délai aléatoire avant de traiter chaque produit
            random_delay()

            # Extraire le titre
            title_element = product.find("a", class_="a-link-normal s-no-outline")

            # Extraire l'attribut 'alt' de l'image
            title = title_element.find("img")["alt"] if title_element and title_element.find("img") else "Titre non trouvé"

            # Extraire le prix
            price_whole = product.find("span", class_="a-price-whole")
            price_fraction = product.find("span", class_="a-price-fraction")
            if price_whole and price_fraction:
                price = f"{price_whole.text.strip()}{price_fraction.text.strip()} €"
            else:
                price = "Prix non trouvé"

            # Extraire l'ancien prix (si disponible)
            old_price_section = product.find("div", class_="a-section aok-inline-block")
            if old_price_section:
                old_price = old_price_section.find("span", class_="a-price a-text-price")
                if old_price:
                    old_price_value = old_price.find("span", class_="a-offscreen")
                    if old_price_value:
                        old_price = old_price_value.text.strip()
                    else:
                        old_price = "Ancien prix non disponible"
                else:
                    old_price = "Ancien prix non disponible"
            else:
                old_price = "Ancien prix non disponible"

            # Afficher les informations du produit
            print(f"Produit : {title}")
            print(f"Prix : {price}")
            print(f"Ancien Prix : {old_price}")
            print("-" * 40)
    else:
        print("Aucun produit trouvé dans la page.")
else:
    print(f"Failed to fetch page. Status code: {response.status_code}")
