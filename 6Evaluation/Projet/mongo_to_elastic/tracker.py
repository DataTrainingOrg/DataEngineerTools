import os
import pymongo
from elasticsearch import Elasticsearch
import time
from bson import ObjectId

print("Démarrage de mongo-tracker...", flush=True)

# Chargement des variables d'environnement
MONGO_HOST = os.getenv("MONGO_HOST", "mongo1")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_REPLICA_SET = os.getenv("MONGO_REPLICA_SET", "rs0")
MONGO_DB = os.getenv("MONGO_DB", "test")

ELASTIC_HOST = os.getenv("ELASTIC_HOST", "elasticsearch")
ELASTIC_PORT = os.getenv("ELASTIC_PORT", "9200")

# Connexion à MongoDB
try:
    print("Connexion à MongoDB...", flush=True)
    mongo_uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/?directConnection=true&serverSelectionTimeoutMS=2000&replicaSet={MONGO_REPLICA_SET}"
    client = pymongo.MongoClient(mongo_uri)
    client.admin.command('ping')  # Test de la connexion
    print("Connexion à MongoDB réussie!", flush=True)
except pymongo.errors.ConnectionFailure as e:
    print("Erreur de connexion à MongoDB:", e, flush=True)
    exit(1)

# Connexion à Elasticsearch
while True:
    try:
        print("Connexion à Elasticsearch...", flush=True)
        es = Elasticsearch([f"http://{ELASTIC_HOST}:{ELASTIC_PORT}"])
        if es.ping():
            print("Connexion à Elasticsearch réussie!", flush=True)
            break
        else:
            raise Exception("Elasticsearch ne répond pas")
    except Exception as e:
        print(f"Erreur de connexion à Elasticsearch: {e}", flush=True)
        time.sleep(5)  # Réessaie toutes les 5 secondes

# Connexion à la base MongoDB
db = client[MONGO_DB]

# Fonction pour convertir les ObjectId en chaînes
def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {key: convert_objectid(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_objectid(item) for item in obj]
    else:
        return obj

# Pipeline pour écouter tous les changements
pipeline = [{'$match': {'operationType': {'$in': ['insert', 'update', 'delete']}}}]

print("Avant db.watch()", flush=True)

# Surveiller les changements et les envoyer à Elasticsearch
with db.watch(pipeline) as stream:
    for change in stream:
        print("Changement détecté:", change, flush=True)

        # Extraire les informations du changement
        operation = change["operationType"]
        collection_name = change["ns"]["coll"]
        document_id = change["documentKey"]["_id"]

        index_name = f"mongo-{collection_name}"  # Crée un index basé sur la collection

        if operation == "insert":
            document = change["fullDocument"]
            document = convert_objectid(document)  # Convertir les ObjectId en chaîne
            # Retirer le champ _id du document, il sera passé dans les paramètres
            document.pop('_id', None)
            es.index(index=index_name, id=str(document_id), document=document)
            print(f"✅ INSERT: Document ajouté à Elasticsearch ({index_name}/{document_id})", flush=True)

        elif operation == "update":
            update_fields = change.get("updateDescription", {}).get("updatedFields", {})
            if update_fields:
                update_fields = convert_objectid(update_fields)  # Convertir les ObjectId en chaîne
                es.update(index=index_name, id=str(document_id), body={"doc": update_fields})
                print(f"✅ UPDATE: Document mis à jour dans Elasticsearch ({index_name}/{document_id})", flush=True)

        elif operation == "delete":
            es.delete(index=index_name, id=str(document_id), ignore=[404])
            print(f"✅ DELETE: Document supprimé de Elasticsearch ({index_name}/{document_id})", flush=True)
