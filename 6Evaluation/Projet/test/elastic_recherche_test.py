import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from elasticsearch import Elasticsearch, ConnectionError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Autoriser toutes les origines (peut être restreint)

# Connexion à Elasticsearch
ELASTIC_HOST = os.getenv("ELASTIC_HOST", "127.0.0.1")  # Par défaut, localhost
ELASTIC_HOST ="127.0.0.1"
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
            'price': product["price"]
        }
        for product in products
    ]
    
    return jsonify(results)

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
            
            # Récupération du dernier prix
            last_price = source.get("price_history", [])
            price = last_price[-1]["price"] if last_price else "Non disponible"
            
            products.append({
                "asin": source.get("asin", ""),
                "name": source.get("name", "Nom inconnu"),
                "image_url": source.get("image_url", ""),
                "price": f"{price} €" if isinstance(price, (int, float)) else price,
                "url": source.get("url", "#")
            })
        
        return products
    except Exception as e:
        print(f"⚠️ Erreur Elasticsearch: {e}")
        return []

if __name__ == '__main__':
    app.run(debug=True)
