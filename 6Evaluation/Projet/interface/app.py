from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
from elasticsearch import Elasticsearch
from bson import ObjectId
import time
from dotenv import load_dotenv

app = Flask(__name__)

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()  # Cela charge les variables d'environnement à partir de .env

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
links_collection = db['links']

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

# Route pour la page d'accueil (suivi des liens)
@app.route('/')
def home():
    return redirect(url_for('track'))

# Route pour le suivi des liens
@app.route('/track', methods=['GET', 'POST'])
def track():
    if request.method == 'POST':
        link = request.form.get('link')
        if link:
            # Enregistrer le lien dans MongoDB
            link_data = {'link': link, 'clicks': 0}
            result = links_collection.insert_one(link_data)
            # Indexer le lien dans Elasticsearch
            es.index(index='links', id=str(result.inserted_id), document=link_data)
            return render_template('track.html', message="Lien ajouté avec succès !")
    return render_template('track.html')

# Route pour la recherche des liens
@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            # Rechercher dans Elasticsearch
            search_results = es.search(index='links', body={'query': {'match': {'link': query}}})
            for hit in search_results['hits']['hits']:
                results.append(hit['_source']['link'])
    return render_template('search.html', results=results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')