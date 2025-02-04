import os
from pymongo import MongoClient
from dotenv import load_dotenv
from mongo_requests.mongo import (
    add_or_update_product_url, add_or_update_product_theme,
    get_product_preview_by_url, get_product_preview_by_theme
)

# Charger les variables d'environnement depuis le répertoire racine du projet
print("Chargement des variables d'environnement...")
dotenv_path = load_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
    print(f".env chargé depuis : {dotenv_path}")
else:
    print("⚠️ Fichier .env introuvable !")

# Vérification des variables d'environnement
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_DB = os.getenv("MONGO_DB", "test")
MONGO_DB_TABLE = os.getenv("MONGO_DB_TABLE", "products")
MONGO_REPLICA_SET = os.getenv("MONGO_REPLICA_SET", "rs0")
print(f"Variables récupérées :")
print(f"  MONGO_HOST = {MONGO_HOST}")
print(f"  MONGO_PORT = {MONGO_PORT}")
print(f"  MONGO_DB = {MONGO_DB}")
print(f"  MONGO_DB_TABLE = {MONGO_DB_TABLE}")
print(f"  MONGO_REPLICA_SET = {MONGO_REPLICA_SET}")

# Connexion à la base de données
print("Connexion à MongoDB...")
try:
    # Construire l'URI MongoDB avec les informations du replica set et du timeout
    mongo_uri = f"mongodb://127.0.0.1:{MONGO_PORT}/?directConnection=true&serverSelectionTimeoutMS=10000&replicaSet={MONGO_REPLICA_SET}"
    print(f"Essai de connexion avec l'URI : {mongo_uri}")
    
    # Connexion avec MongoClient
    client = MongoClient(mongo_uri)
    print("Client MongoDB créé. Test de la connexion...")
# Accéder à la base de données
    db = client[MONGO_DB]
    print(f"Accès à la base de données '{MONGO_DB}'")
    # Vérification de la connexion
    server_info = client.server_info()  # Va lever une exception si la connexion échoue
    print(f"Connexion réussie au serveur MongoDB : {server_info}")
    
    

    # Accéder à la collection
    collection = db[MONGO_DB_TABLE]
    print(f"Accès à la collection '{MONGO_DB_TABLE}'")

except Exception as e:
    print(f"Erreur lors de la connexion à MongoDB : {e}")
    exit()

# Tester les fonctionnalités
print("Ajout d'un produit via URL...")
try:
    result_url = add_or_update_product_url(collection, "B07XJ8C8F5", "Produit 1", "http://example.com", 99.99, "http://image.com")
    print(f"Résultat ajout produit URL : {result_url}")
except Exception as e:
    print(f"Erreur lors de l'ajout du produit via URL : {e}")

print("Récupération d'un produit par URL...")
try:
    result_get_url = get_product_preview_by_url(collection, "B07XJ8C8F5")
    print(f"Résultat récupération produit URL : {result_get_url}")
except Exception as e:
    print(f"Erreur lors de la récupération du produit par URL : {e}")

print("Ajout d'un thème avec des produits...")
try:
    result_theme = add_or_update_product_theme(collection, "Tech", [
        {"asin": "B07XJ8C8F4", "name": "Produit 2", "price": 99.99, "image_url": "http://image.com"},
        {"asin": "B09ABC1234", "name": "Produit 3", "price": 129.99}
    ])
    print(f"Résultat ajout thème : {result_theme}")
except Exception as e:
    print(f"Erreur lors de l'ajout du thème avec des produits : {e}")

print("Récupération d'un thème avec ses produits...")
try:
    result_get_theme = get_product_preview_by_theme(collection, "Tech")
    print(f"Résultat récupération thème : {result_get_theme}")
except Exception as e:
    print(f"Erreur lors de la récupération du thème avec ses produits : {e}")
