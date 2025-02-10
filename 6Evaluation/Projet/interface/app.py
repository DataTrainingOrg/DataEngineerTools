from flask import Flask, render_template, request, redirect, url_for, render_template_string, jsonify
import os
import pymongo
from elasticsearch import Elasticsearch
from bson import ObjectId
import time
import sys
from flask_cors import CORS

# Ajouter le dossier shared au PATH pour permettre l'import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared')))
from function import is_url, is_amazon_url, clean_text, del_sponsor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scrapping')))
from scrapping_script import scrape_product_details_with_image, scrape_products_info

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../mongo_requests')))
from mongo import add_or_update_products, add_new_track_to_db


# Initialisation de l'application Flask
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Autoriser toutes les origines (peut être restreint)

# Charger les variables d'environnement depuis le fichier .env
# Chargement des variables d'environnement
MONGO_HOST = os.getenv("MONGO_HOST", "mongo1")
MONGO_HOST = "localhost"
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_REPLICA_SET = os.getenv("MONGO_REPLICA_SET", "rs0")
MONGO_DB = os.getenv("MONGO_DB", "amazon_web_scraper")
MONGO_DB_TABLE = os.getenv("MONGO_DB_TABLE", "products")
MONGO_DB_TABLE_TRACKER = os.getenv("MONGO_DB_TABLE_TRACKER", "track_list")

ELASTIC_HOST = os.getenv("ELASTIC_HOST", "elasticsearch")
ELASTIC_HOST = "localhost"
ELASTIC_PORT = os.getenv("ELASTIC_PORT", "9200")

# Connexion à MongoDB et Elasticsearch après l'initialisation de Flask
client = None
es = None

# Connexion à MongoDB
def connect_mongo():
    while True:
        try:
            print("Connexion à MongoDB...", flush=True)
            mongo_uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/?directConnection=true&serverSelectionTimeoutMS=2000&replicaSet={MONGO_REPLICA_SET}"
            client = pymongo.MongoClient(mongo_uri)
            client.admin.command('ping')  # Test de la connexion
            print("Connexion à MongoDB réussie!", flush=True)
            break
        except pymongo.errors.ConnectionFailure as e:
            print("Erreur de connexion à MongoDB:", e, flush=True)
            time.sleep(5)
    return client

# Connexion à Elasticsearch
def connect_elastic():
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
    return es

# Connexion à la base MongoDB
client = connect_mongo()
es = connect_elastic()

# Connexion aux collections MongoDB
db = client[MONGO_DB]
links_collection = db[MONGO_DB_TABLE]
track_collection = db[MONGO_DB_TABLE_TRACKER]

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


datas = []
themeName = None
URL = None

# Route pour la page d'accueil (suivi des liens)
@app.route('/')
def home():
    datas.clear()
    return redirect(url_for('track'))

# Route pour vérifier la connexion à MongoDB et Elasticsearch
@app.route('/check_connections', methods=['GET'])
def check_connections():
    try:
        # Vérifier la connexion MongoDB
        client.admin.command('ping')  # Si cela passe, MongoDB est connecté
        mongo_status = True
    except pymongo.errors.ConnectionFailure:
        mongo_status = False

    try:
        # Vérifier la connexion Elasticsearch
        if es.ping():
            elastic_status = True
        else:
            elastic_status = False
    except Exception:
        elastic_status = False

    return jsonify({
        'mongo': mongo_status,
        'elastic': elastic_status
    })


# Route pour le suivi des liens
@app.route('/track', methods=['GET', 'POST'])
def track():
    global datas
    global themeName
    global URL
    if request.method == 'POST':
        action = request.form.get('action')
        
        link = request.form.get('link')
        if action == 'search':
            message = validate_link(link)
            print(link,flush=True)
            if message == 'amazon':
                data = scrape_product_details_with_image(link)
                themeName=None
                URL = link
                if data.get('asin') and not any(d['asin'] == data['asin'] for d in datas):
                    datas.append(data)
                    return render_template('track.html', users=datas, show_track_button=True)
                else: 
                    return render_template('track.html', users=datas, message="Produit déjà ajouté", show_track_button=False)

            elif message == 'theme':
                URL = None
                result = scrape_products_info(clean_text(link))
                
                nb = result['count']
                clean_datas = del_sponsor(result['products']) 
                datas = clean_datas[0]
                nb -= clean_datas[1]
                clean = clean_text(link) 
                themeName = clean[0]
                return render_template('track.html', users=datas, message=str(nb)+" produits trouvés ", show_track_button=True)

            elif message == 'link':
                return render_template('track.html', users=datas, message="Lien amazon non reconnu", show_track_button=False)
            else:
                return render_template('track.html', users=datas, message="Erreur", show_track_button=False)

        if action == 'track':
            list_data = datas.copy()
            datas.clear()   
            add_or_update_products(links_collection, list_data,URL, theme=themeName)
            delay = request.form.get('delay')
            print(delay,flush=True)
            add_new_track_to_db(track_collection, themeName, URL, int(delay))
            return render_template('track.html', message='Lancement du tracking effectué !', show_track_button=True)

    return render_template('track.html', show_track_button=False)

@app.route('/delete_product', methods=['POST'])
def delete_product():
    data = request.get_json()  # Récupérer les données envoyées via AJAX
    asin = data.get('asin')  # Extraire l'ASIN du produit à supprimer

    # Vérifier si l'ASIN est présent dans la liste
    global datas
    product_to_delete = next((d for d in datas if d['asin'] == asin), None)

    if product_to_delete:
        # Si le produit existe, le supprimer de la liste
        datas = [d for d in datas if d['asin'] != asin]
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Produit non trouvé")

# Fonction de validation du lien
def validate_link(link):
    # Exemple de validation : vérifier si le lien contient "link"
    # Tu peux ajouter d'autres critères de validation ici
    if is_url(link):
        if is_amazon_url(link):
            return 'amazon'
        else:
            return 'link'
    else:
        return 'theme'

# Route pour la recherche des prouits trackés
@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('q', '').strip()
    products = get_products(query)
    
    # Générer la réponse JSON correcte
    results = [
        {
            'name': product["name"],
            'image_url': product["image_url"],
            'price': product["price"],
            'asin': product["asin"],
            'price_history': product["price_history"]  # Assurer qu'il reste un objet JSON
        }
        for product in products
    ]
    
    return jsonify(results)

@app.route('/product/<product_id>', methods=['GET'])
def product_details(product_id):
    products = get_products('')
    product = next((p for p in products if p["asin"] == product_id), None)
    
    if product:
        return jsonify({
            'name': product["name"],
            'image_url': product["image_url"],
            'price': product["price"],
            'price_history': product["price_history"]  # Assurer qu'il reste un objet JSON
        })
    else:
        return jsonify({'error': 'Produit non trouvé'}), 404

def get_products(query):
    """Recherche des produits avec auto-complétion et fuzzy matching"""
    if not query:
        return []

    try:
        payload = {
            "query": {
                "bool": {
                    "should": [
                        {"match": {"name": {"query": query, "fuzziness": "AUTO"}}},
                        {"match_phrase_prefix": {"name": query}}
                    ],
                    "minimum_should_match": 1
                }
            }
        }

        response = es.search(index="mongo-products", body=payload, size=10)

        products = []
        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            price_history = []

            # Récupérer price_history principal si présent
            if "price_history" in source:
                for item in source["price_history"]:
                    price_history.append({
                        "price": item["price"],
                        "timestamp": item["timestamp"]
                    })

            # Vérification des différents indices de price_history (price_history.1, price_history.2, ...)
            i = 1
            while f"price_history.{i}" in source:
                price_history.append({
                    "price": source[f"price_history.{i}"]["price"],
                    "timestamp": source[f"price_history.{i}"]["timestamp"]
                })
                i += 1

            # Extraire le dernier prix
            last_price = price_history[-1]["price"] if price_history else "Non disponible"

            products.append({
                "asin": source.get("asin", ""),
                "name": source.get("name", "Nom inconnu"),
                "image_url": source.get("image_url", ""),
                "price": f"{last_price} €" if isinstance(last_price, (int, float)) else last_price,
                "url": source.get("url", "#"),
                "price_history": price_history  # Conserver l'historique des prix sous forme d'objet JSON
            })
        return products
    except Exception as e:
        print(f"⚠️ Erreur Elasticsearch: {e}")
        return []

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
