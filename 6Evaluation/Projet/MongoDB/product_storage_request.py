from pymongo import MongoClient
from datetime import datetime

# Connexion à MongoDB
def connect_to_mongo(collection_name):
    """
    Établit la connexion à MongoDB et retourne la collection demandée.
    """
    client = MongoClient("mongodb://root:rootpassword@localhost:27017/admin?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.3")
    db = client["amazon_scrapping"]
    return db[collection_name]

# Fonction pour ajouter un produit à la base product_scrapping_url
def add_product_from_url(asin, name, price):
    """
    Ajoute un produit à la collection 'product_scrapping_url'.

    Args:
        asin (str): Identifiant unique du produit (ASIN).
        name (str): Nom du produit.
        price (float): Prix initial du produit.

    Returns:
        dict: Résultat de l'opération.
    """
    collection = connect_to_mongo("product_scrapping_url")

    product = {
        "asin": asin,
        "name": name,
        "price_history": [{"price": price, "timestamp": datetime.utcnow()}],
    }

    result = collection.update_one(
        {"asin": asin},
        {"$set": {"name": name}, "$push": {"price_history": product["price_history"][0]}},
        upsert=True,
    )
    return {"success": result.modified_count > 0 or result.upserted_id is not None}

# Fonction pour mettre à jour l'historique de prix d'un produit
def update_price_history(asin, new_price):
    """
    Met à jour l'historique de prix d'un produit existant.

    Args:
        asin (str): Identifiant unique du produit (ASIN).
        new_price (float): Nouveau prix du produit.

    Returns:
        dict: Résultat de l'opération.
    """
    collection = connect_to_mongo("product_scrapping_url")
    result = collection.update_one(
        {"asin": asin},
        {"$push": {"price_history": {"price": new_price, "timestamp": datetime.utcnow()}}},
    )
    return {"success": result.modified_count > 0}

# Fonction pour ajouter des produits à partir d'un thème
def add_products_from_theme(theme, products):
    """
    Ajoute une sous-base pour un thème et y stocke les produits.

    Args:
        theme (str): Nom du thème.
        products (list): Liste de produits au format [{'asin': str, 'name': str, 'price': float}].

    Returns:
        dict: Résultat de l'opération.
    """
    collection = connect_to_mongo("product_scrapping_theme")

    theme_data = {
        "theme": theme,
        "products": [
            {
                "asin": product["asin"],
                "name": product["name"],
                "price_history": [{"price": product["price"], "timestamp": datetime.utcnow()}],
            }
            for product in products
        ],
        "updated_at": datetime.utcnow(),
    }

    result = collection.update_one(
        {"theme": theme},
        {"$set": {"products": theme_data["products"], "updated_at": theme_data["updated_at"]}},
        upsert=True,
    )
    return {"success": result.modified_count > 0 or result.upserted_id is not None}


def sync_theme_products(theme_name, new_products):
    collection = connect_to_mongo("product_scrapping_theme")
    now = datetime.utcnow()

    theme = collection.find_one({"theme": theme_name})

    if theme:
        existing_products = {p["asin"]: p for p in theme["products"]}

        for product in new_products:
            asin = product["asin"]
            price = product["price"]
            name = product["name"]

            if asin in existing_products:
                existing_product = existing_products[asin]

                # Vérifier uniquement les deux derniers éléments de la liste
                if len(existing_product["price_history"]) < 2 or not (
                    existing_product["price_history"][-1]["price"] == price
                    and existing_product["price_history"][-1]["timestamp"] == now
                ) and not (
                    existing_product["price_history"][-2]["price"] == price
                    and existing_product["price_history"][-2]["timestamp"] == now
                ):
                    # Ajouter une nouvelle entrée si elle est différente des deux dernières
                    existing_product["price_history"].append({"price": price, "timestamp": now})

            else:
                existing_products[asin] = {
                    "asin": asin,
                    "name": name,
                    "price_history": [{"price": price, "timestamp": now}]
                }

        collection.update_one(
            {"theme": theme_name},
            {
                "$set": {
                    "products": list(existing_products.values()),
                    "updated_at": now
                }
            }
        )
    else:
        products = [
            {
                "asin": product["asin"],
                "name": product["name"],
                "price_history": [{"price": product["price"], "timestamp": now}]
            }
            for product in new_products
        ]
        collection.insert_one({
            "theme": theme_name,
            "products": products,
            "updated_at": now
        })
