import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from elasticsearch import Elasticsearch, ConnectionError
from flask_cors import CORS

# Initialisation de l'application Flask
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Autoriser toutes les origines (peut être restreint)

# Connexion à Elasticsearch
ELASTIC_HOST = os.getenv("ELASTIC_HOST", "127.0.0.1")  # Par défaut, localhost
ELASTIC_HOST = "127.0.0.1"
ELASTIC_PORT = os.getenv("ELASTIC_PORT", "9200")

try:
    es = Elasticsearch([f"http://{ELASTIC_HOST}:{ELASTIC_PORT}"])
    if not es.ping():
        raise ConnectionError("Impossible de se connecter à Elasticsearch")
    print("✅ Connexion réussie à Elasticsearch")
except ConnectionError as e:
    print(f"❌ Erreur de connexion: {e}")

@app.route('/')
def index():
    return redirect(url_for('search'))

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
    app.run(debug=True)
