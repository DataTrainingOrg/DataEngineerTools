import requests
from bs4 import BeautifulSoup
import random
import time

# URL de la page à tester
url = "https://www.amazon.fr/s?k=processeur"

# Liste de User-Agents à tester
user_agents = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 4.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows 98)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows 2000)",
]

# Fonction pour tester un User-Agent
def test_user_agent(user_agent):
    headers = {
        "User-Agent": user_agent
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # Vérifiez si un élément attendu est présent dans la page (par exemple, des produits)
            product_containers = soup.find_all("div", {"data-component-type": "s-search-result"})
            if product_containers:
                return True, len(product_containers)
            else:
                return False, 0
        else:
            return False, 0
    except Exception as e:
        print(f"Erreur avec User-Agent {user_agent} : {e}")
        return False, 0

# Tester chaque User-Agent
for user_agent in user_agents:
    print(f"Test du User-Agent : {user_agent}")
    success, product_count = test_user_agent(user_agent)
    if success:
        print(f"✅ Données récupérées avec succès. Produits trouvés : {product_count}")
    else:
        print("❌ Échec de la récupération des données.")
    # Pause aléatoire entre les requêtes pour éviter d'être bloqué
    time.sleep(random.uniform(1, 3))
