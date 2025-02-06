from flask import Flask, render_template, request, redirect, url_for,render_template_string,jsonify
import os
import pymongo
from elasticsearch import Elasticsearch
from bson import ObjectId
import time
import sys
import os

# Ajouter le dossier shared au PATH pour permettre l'import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared')))
from function import is_url, is_amazon_url, clean_text,del_sponsor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scrapping')))
from scrapping_script import scrape_product_details_with_image,scrape_products_info

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../mongo_requests')))
from mongo import add_or_update_products,add_new_track_to_db


app = Flask(__name__)

# Charger les variables d'environnement depuis le fichier .env

# Chargement des variables d'environnement
MONGO_HOST = os.getenv("MONGO_HOST", "mongo1")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_REPLICA_SET = os.getenv("MONGO_REPLICA_SET", "rs0")
MONGO_DB = os.getenv("MONGO_DB", "amazon_web_scraper")
MONGO_DB_TABLE = os.getenv("MONGO_DB_TABLE", "products")
MONGO_DB_TABLE_TRACKER = os.getenv("MONGO_DB_TABLE_TRACKER", "track_list")

ELASTIC_HOST = os.getenv("ELASTIC_HOST", "elasticsearch")
ELASTIC_PORT = os.getenv("ELASTIC_PORT", "9200")



# Connexion à MongoDB
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

app = Flask(__name__)

datas=[]
themeName = None
URL = None
# Route pour la page d'accueil (suivi des liens)
@app.route('/')
def home():
    datas.clear()
    return redirect(url_for('track'))

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

# Route pour la recherche des liens
@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            # Rechercher dans Elasticsearch (ou autre base de données)
            # À implémenter selon ton besoin
            results.append(query)  # Exemple d'ajout de la recherche
    return render_template('search.html', results=results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
