from datetime import datetime, timedelta


def add_or_update_products(collection, products, URL, theme=None):
    """
    Ajoute ou met à jour un ou plusieurs produits dans la base de données.
    
    Args:
        collection: Collection MongoDB où stocker les produits.
        products (list): Liste de dictionnaires représentant les produits.
        theme (str, optional): Thème à associer à tous les produits (peut être None).

    Returns:
        dict: Indique si l'opération a réussi.
    """
    if not isinstance(products, list):
        products = [products]  # Permet d'accepter un seul produit sous forme de dict
    print("URL",URL,flush=True)
    print("theme",theme,flush=True)
    for product in products:
        # Récupération des valeurs avec None par défaut si elles ne sont pas fournies
        asin = product.get("asin")
        name = product.get("name", None)
        if theme == None:
            url = URL
        else:
            url = product.get("url", None)
        price = product.get("price", None) or "Prix non trouvé"
        image_url = product.get("image_url", None)

        # Création du document produit
        update_data = {
            "$set": {
                "name": name,
                "url": url,
                "image_url": image_url,
                "theme": theme
            },
            "$push": {
                "price_history": {"price": price, "timestamp": datetime.utcnow()}
            }
        }

        # Ajout ou mise à jour dans MongoDB
        result = collection.update_one(
            {"asin": asin},
            update_data,
            upsert=True
        )

    return {"success": True}

# Récupérer l'aperçu d'un produit par son ASIN
def get_product_preview_by_url(collection, asin):
    product = collection.find_one(
        {"asin": asin}, 
        {"_id": 0, "asin": 1, "name": 1, "url": 1, "theme": 1, "price_history": 1, "image_url": 1}
    )
    return product if product else {"error": "Produit non trouvé"}

# Récupérer l'aperçu d'un produit par thème
def get_product_preview_by_theme(collection, theme):
    theme_data = collection.find_one(
        {"theme": theme},
        {"_id": 0, "theme": 1, "products.name": 1, "products.image_url": 1, "products.price": 1, "products.price_history": 1}
    )
    return theme_data if theme_data else {"error": "Thème non trouvé"}


def delete_product(collection, asin):
    """
    Supprime un produit de la base de données par son ASIN.

    Args:
        collection: Collection MongoDB contenant les produits.
        asin (str): ASIN du produit à supprimer.

    Returns:
        dict: Indique si l'opération a réussi.
    """
    result = collection.delete_one({"asin": asin})
    if result.deleted_count:
        return {"success": True}
    else:
        return {"success": False, "message": "Produit non trouvé"}
    

def delete_theme(collection, theme):
    """
    Supprime un thème et tous les produits associés de la base de données.

    Args:
        collection: Collection MongoDB contenant les produits.
        theme (str): Thème à supprimer.

    Returns:
        dict: Indique si l'opération a réussi.
    """
    result = collection.delete_many({"theme": theme})
    if result.deleted_count:
        return {"success": True}
    else:
        return {"success": False, "message": "Thème non trouvé"}

def get_all_themes(collection):
    """
    Récupère la liste de tous les thèmes présents dans la base de données.

    Args:
        collection: Collection MongoDB contenant les produits.

    Returns:
        list: Liste des thèmes.
    """
    themes = collection.distinct("theme")
    return themes


def add_new_track_to_db(collection, theme, URL, delay):
    """
    Ajoute un nouveau tracking dans la collection MongoDB.

    Args:
        collection: Collection MongoDB contenant les trackings.
        theme (str): Thème du tracking.
        URL (str): URL du tracking.
        delay (int): temps entre 2 scrap en heure.

    Returns:
        dict: Résultat de l'opération, incluant l'identifiant du document inséré.
    """
    print("Ajout d'un nouveau tracking dans la base de données",flush=True)
    print("theme",theme,flush=True)
    print("URL",URL,flush=True)
    print("delay",delay,flush=True)

    # Construction du document à insérer
    tracking_document = {
        "theme": theme,
        "URL": URL,
        "interval_hours": delay,
        "created_at": datetime.utcnow(),  # Date et heure de création
        "last_executed": datetime.utcnow()  # Dernière mise à jour
    }

    # Insertion dans la base de données
    result = collection.insert_one(tracking_document)
    
    return {"success": True, "inserted_id": str(result.inserted_id)}


