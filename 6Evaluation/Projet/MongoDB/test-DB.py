from product_storage_request import (
    add_product_from_url,
    update_price_history,
    add_products_from_theme,
    sync_theme_products,
)
from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient("mongodb://root:rootpassword@localhost:27017/admin")
db = client["amazon_scrapping"]
url_collection = db["product_scrapping_url"]
theme_collection = db["product_scrapping_theme"]

# Nettoyage des collections pour les tests
url_collection.delete_many({})
theme_collection.delete_many({})

# Test 1 : Ajouter un produit via URL
print("Test 1: Ajouter un produit via URL")
add_product_from_url("B000123456", "Produit Test", 19.99)
product = url_collection.find_one({"asin": "B000123456"})
print("Produit ajouté :", product)

# Test 2 : Mettre à jour l'historique du prix pour un produit via URL
print("\nTest 2: Mise à jour de l'historique des prix")
update_price_history("B000123456", 20.99)
updated_product = url_collection.find_one({"asin": "B000123456"})
print("Produit après mise à jour :", updated_product)

# Test 3 : Ajouter des produits à partir d'un thème
print("\nTest 3: Ajouter des produits depuis un thème")
theme_data = [
    {"asin": "B000789101", "name": "Produit A", "price": 29.99},
    {"asin": "B000111213", "name": "Produit B", "price": 15.99},
]
add_products_from_theme("Thème Test", theme_data)
theme = theme_collection.find_one({"theme": "Thème Test"})
print("Thème ajouté :", theme)

# Test 4 : Synchroniser les produits pour un thème
print("\nTest 4: Synchronisation des produits d'un thème")
updated_theme_data = [
    {"asin": "B000789101", "name": "Produit A", "price": 30.99},  # Prix mis à jour
    {"asin": "B000141516", "name": "Produit C", "price": 12.49},  # Nouveau produit
]
sync_theme_products("Thème Test", updated_theme_data)
theme_after_sync = theme_collection.find_one({"theme": "Thème Test"})
print("Thème après synchronisation :", theme_after_sync)

# Affichage final des collections pour vérification
print("\n--- Vérification finale ---")
print("Collection URL :", list(url_collection.find()))
print("Collection Thèmes :", list(theme_collection.find()))
