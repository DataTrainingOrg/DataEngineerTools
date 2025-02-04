import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le répertoire racine du projet
dotenv_path = load_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
else:
    print("⚠️ Fichier .env introuvable !")

# Vérification des variables d'environnement
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_DB = os.getenv("MONGO_DB", "test")
MONGO_REPLICA_SET = os.getenv("MONGO_REPLICA_SET", "rs0")

print(f"Variables récupérées :")
print(f"  MONGO_HOST = {MONGO_HOST}")
print(f"  MONGO_PORT = {MONGO_PORT}")
print(f"  MONGO_DB = {MONGO_DB}")
print(f"  MONGO_REPLICA_SET = {MONGO_REPLICA_SET}")

# Connexion à la base de données
try:
    mongo_uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/?directConnection=true&serverSelectionTimeoutMS=10000&replicaSet={MONGO_REPLICA_SET}"
    client = MongoClient(mongo_uri)
    db = client[MONGO_DB]
    print(f"Connexion réussie à MongoDB sur {MONGO_HOST}:{MONGO_PORT}")
except Exception as e:
    print(f"❌ Échec de la connexion à MongoDB : {e}")
