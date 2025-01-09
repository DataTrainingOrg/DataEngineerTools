from pymongo import MongoClient
from datetime import datetime

def insert_product_data(db_name,asin, title, price,product_url):
    # Connexion à MongoDB (modifie les paramètres selon ton setup)
    client = MongoClient("mongodb://root:rootpassword@localhost:27017/admin")  # remplace par tes informations de connexion
    
    # Sélectionner la base de données
    db = client["product_tracker"]
    
    # Choisir la collection (par exemple "processeur")
    collection = db[db_name]  # Remplace "processeur" par la collection que tu veux

    # Créer un document avec les données à insérer
    document = {
        "_id": asin,  # ASIN comme identifiant unique
        "title": title,  # Titre du produit
        "price": price,  # Prix du produit
        "time": datetime.utcnow(),  # Heure actuelle (format UTC)
        "url": product_url,
        "need_update":False,
    }

    # Insérer le document dans la collection
    try:
        collection.insert_one(document)
        print(f"Produit {title} inséré avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'insertion du produit : {e}")


def update_product_title(db_name, asin, new_title):
    # Connexion à MongoDB
    client = MongoClient("mongodb://root:rootpassword@localhost:27017/admin")
    db = client["product_tracker"]
    collection = db[db_name]

    try:
        result = collection.update_one(
            {"_id": asin},
            {"$set": {"title": new_title}}
        )

        if result.matched_count > 0:
            print(f"Titre du produit avec ASIN {asin} mis à jour avec succès.")
        else:
            print(f"Aucun produit trouvé avec l'ASIN {asin}.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour du titre : {e}")

def is_product_in_db(db_name, asin):
    # Connexion à MongoDB
    client = MongoClient("mongodb://root:rootpassword@localhost:27017/admin")
    db = client["product_tracker"]
    collection = db[db_name]

    # Vérifier si le produit existe dans la base de données
    product = collection.find_one({"_id": asin})

    if product:
        return True
    else:
        return False

def update_product_price(db_name,asin, new_price):
    # Connexion à MongoDB (modifie les paramètres selon ton setup)
    client = MongoClient("mongodb://root:rootpassword@localhost:27017/admin")  # remplace par tes informations de connexion
    
    # Sélectionner la base de données
    db = client["product_tracker"]
    
    # Choisir la collection (par exemple "processeur")
    collection = db[db_name]  # Remplace "processeur" par la collection que tu veux

    # Créer l'objet de mise à jour avec la nouvelle date et prix
    current_time = datetime.utcnow()
    price_update = {
        "price": new_price,
        "date": current_time,
        "need_update":False
    }

    # Mettre à jour l'historique des prix
    try:
        result = collection.update_one(
            {"_id": asin},  # Chercher le produit par son ASIN
            {
                "$push": {
                    "price_history": price_update  # Ajouter le nouveau prix à l'historique
                },
                "$set": {
                    "price": new_price  # Mettre à jour le prix actuel du produit
                }
            }
        )
        
        if result.matched_count > 0:
            print(f"Prix pour le produit {asin} mis à jour avec succès.")
        else:
            print(f"Aucun produit trouvé avec l'ASIN {asin}.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour du prix : {e}")

def get_product_data(db_name, asin):
    # Connexion à MongoDB
    client = MongoClient("mongodb://root:rootpassword@localhost:27017/admin")
    db = client["product_tracker"]
    collection = db[db_name]  # Remplace par la collection appropriée

    # Récupérer le produit par son ASIN
    product = collection.find_one({"_id": asin})

    if product:
        print(f"Produit trouvé : {product['title']}")
        print(f"Prix actuel : {product['price']}")
        print(f"Historique des prix : {product['price_history']}")
    else:
        print(f"Produit avec ASIN {asin} non trouvé.")

def get_price_history(db_name, asin):
    # Connexion à MongoDB
    client = MongoClient("mongodb://root:rootpassword@localhost:27017/admin")
    db = client["product_tracker"]
    collection = db[db_name]

    product = collection.find_one({"_id": asin})

    if product:
        print(f"Historique des prix pour {product['title']} (ASIN: {asin}):")
        for entry in product["price_history"]:
            print(f"Prix : {entry['price']} - Date : {entry['date']}")
    else:
        print(f"Produit avec ASIN {asin} non trouvé.")

def product_exists(db_name, asin):
    # Connexion à MongoDB
    client = MongoClient("mongodb://root:rootpassword@localhost:27017/admin")
    db = client["product_tracker"]
    collection = db[db_name]

    product = collection.find_one({"_id": asin})

    if product:
        return True
    else:
        return False

def get_all_products(db_name):
    # Connexion à MongoDB
    client = MongoClient("mongodb://root:rootpassword@localhost:27017/admin")
    db = client["product_tracker"]
    collection = db[db_name]

    products = collection.find()

    if products:
        for product in products:
            print(f"ASIN : {product['_id']} - Titre : {product['title']} - Prix actuel : {product['price']}")
    else:
        print("Aucun produit trouvé.")

def turn_all_need_update_on(db_name):
    """
    Met à jour tous les documents de la collection pour passer le champ 'needs_update' à True.
    
    Args:
        db_name (str): Le nom de la collection MongoDB.
    
    Returns:
        int: Le nombre de documents mis à jour.
    """
    client = MongoClient("mongodb://root:rootpassword@localhost:27017/admin")
    db = client["product_tracker"]
    collection = db[db_name]
    
    # Met à jour tous les champs needs_update à True
    result = collection.update_many({}, {"$set": {"needs_update": True}})
    
    # Retourner le nombre de documents affectés
    return result.modified_count
    

def get_and_reset_needs_update(db_name):
    """
    Récupère tous les ASINs où 'needs_update = True' et réinitialise ce champ à False.
    
    Args:
        db_name (str): Le nom de la collection MongoDB.
    
    Returns:
        list: Liste des ASINs nécessitant une mise à jour.
    """
    client = MongoClient("mongodb://root:rootpassword@localhost:27017/admin")
    db = client["product_tracker"]
    collection = db[db_name]
    
    # Récupérer tous les produits ayant needs_update = True
    products_to_update = collection.find({"needs_update": True})
    
    # Extraire les ASINs dans une liste
    asin_list = [product["_id"] for product in products_to_update]
    
    # Réinitialiser needs_update à False pour tous ces produits
    collection.update_many({"needs_update": True}, {"$set": {"needs_update": False}})
    
    return asin_list

def reset_collection(db_name):
    """
    Supprime tous les documents de la collection spécifiée.
    
    Args:
        db_name (str): Le nom de la collection MongoDB.
    
    Returns:
        int: Le nombre de documents supprimés.
    """
    client = MongoClient("mongodb://root:rootpassword@localhost:27017/admin")
    db = client["product_tracker"]
    collection = db[db_name]
    
    # Supprimer tous les documents de la collection
    result = collection.delete_many({})
    
    # Retourner le nombre de documents supprimés
    return result.deleted_count

def restet_all():
    """
    Supprime toutes les collections de la base de données.
    
    Returns:
        int: Le nombre de collections supprimées.
    """
    client = MongoClient("mongodb://root:rootpassword@localhost:27017/admin")
    db = client["product_tracker"]
    
    # Supprimer toutes les collections de la base de données
    result = db.list_collection_names()
    for collection in result:
        db.drop_collection(collection)
    
    # Retourner les collections supprimées
    return result

