import requests
from datetime import datetime

# URL de l'API Flask pour indexer un produit
url = 'http://localhost:5000/index_product'

# Liste de produits de test avec des noms détaillés et tes champs
products = [
    {
        "name": "Smartphone Galaxy X100",
        "url": "https://example.com/smartphone-galaxy-x100",
        "image_url": "https://example.com/images/smartphone-galaxy-x100.jpg",
        "theme": "Electronique",
        "price": 199.99
    },
    {
        "name": "Cafetière Expresso Pro 5000",
        "url": "https://example.com/cafetiere-expresso-pro-5000",
        "image_url": "https://example.com/images/cafetiere-expresso-pro-5000.jpg",
        "theme": "Cuisine",
        "price": 49.99
    },
    {
        "name": "Tondeuse à gazon Turbo 300",
        "url": "https://example.com/tondeuse-a-gazon-turbo-300",
        "image_url": "https://example.com/images/tondeuse-a-gazon-turbo-300.jpg",
        "theme": "Jardin",
        "price": 89.99
    },
    {
        "name": "Veste en cuir élégante",
        "url": "https://example.com/veste-en-cuir-elegante",
        "image_url": "https://example.com/images/veste-en-cuir-elegante.jpg",
        "theme": "Mode",
        "price": 69.99
    },
    {
        "name": "Montre fitness SmartTrack 2.0",
        "url": "https://example.com/montre-fitness-smarttrack-2-0",
        "image_url": "https://example.com/images/montre-fitness-smarttrack-2-0.jpg",
        "theme": "Fitness",
        "price": 129.99
    }
]

# Envoi des produits de test à l'API Flask
for product in products:
    # Création de la requête avec les champs et l'historique des prix
    update_data = {
        "$set": {
            "name": product["name"],
            "url": product["url"],
            "image_url": product["image_url"],
            "theme": product["theme"]
        },
        "$push": {
            "price_history": {
                "price": product["price"],
                "timestamp": datetime.utcnow().isoformat()  # Format de date pour MongoDB ou Elasticsearch
            }
        }
    }

    # Envoi de la requête POST à l'API Flask
    response = requests.post(url, json=update_data)
    if response.status_code == 201:
        print(f"Produit '{product['name']}' indexé avec succès!")
    else:
        print(f"Erreur lors de l'indexation du produit '{product['name']}': {response.status_code} - {response.text}")
