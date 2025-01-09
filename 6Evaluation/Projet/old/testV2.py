import requests
import random
import time
from bs4 import BeautifulSoup

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

# Fonction pour scraper les informations du produit à partir du HTML
def scrape_product_details(html):
    soup = BeautifulSoup(html, "html.parser")
    
    # Récupérer tous les éléments <li> correspondant aux produits
    product_items = soup.find_all("li", class_="ProductGridItem__itemOuter__KUtvv")
    
    product_details = []
    
    for item in product_items:
        # Extraction du nom du produit
        title_element = item.find("a", class_="Title__title__z5HRm")
        title = title_element.text.strip() if title_element else "Titre non trouvé"
        
        # Extraction du prix du produit
        price_whole = item.find("span", class_="Price__whole__mQGs5")
        price_fraction = item.find("span", class_="Price__fractional__wJiJp")
        price = f"{price_whole.text.strip()},{price_fraction.text.strip()} €" if price_whole and price_fraction else "Prix non trouvé"
        
        # Extraction de l'URL du produit
        product_link_element = item.find("a", class_="Overlay__overlay__LloCU")
        product_url = f"https://www.amazon.fr{product_link_element['href']}" if product_link_element else "URL non trouvée"
        
        # Extraction de l'évaluation du produit
        rating_element = item.find("span", class_="ProductGridItem__rating--short__nRK4h")
        rating = rating_element.text.strip() if rating_element else "Note non trouvée"
        
        # Extraction du nombre de commentaires
        review_count_element = item.find("span", class_="ProductGridItem__reviewCount__laMDa")
        review_count = review_count_element.text.strip() if review_count_element else "Nombre de commentaires non trouvé"
        
        # Ajouter les détails du produit à la liste
        product_details.append({
            "title": title,
            "price": price,
            "url": product_url,
            "rating": rating,
            "review_count": review_count
        })
    
    return product_details

# Fonction pour récupérer le HTML d'une page
def get_html(url):
    headers = {"User-Agent": get_random_user_agent()}
    random_delay()  # Ajouter un délai pour éviter les blocages

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Vérifier si le code de statut est 200
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de la page : {e}")
        return None

def save_html_to_file(html, filename):
    """
    Sauvegarde le contenu HTML dans un fichier.
    
    :param html: Le contenu HTML à sauvegarder
    :param filename: Le nom du fichier où enregistrer le contenu HTML
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html)
        print(f"Le fichier a été sauvegardé sous : {filename}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du fichier : {e}")


# Exemple d'utilisation
url = "https://www.amazon.fr/stores/page/D88E2FF3-48B1-4191-986D-9C4100149487"  # Exemple d'URL de recherche
html = get_html(url)
save_html_to_file(html, "amazon_products.html")
# if html:
#     products = scrape_product_details(html)
#     for product in products:
#         print(f"Titre : {product['title']}")
#         print(f"Prix : {product['price']}")
#         print(f"URL : {product['url']}")
#         print(f"Note : {product['rating']}")
#         print(f"Nombre de commentaires : {product['review_count']}")
#         print("-" * 40)
