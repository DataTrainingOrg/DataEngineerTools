from datetime import datetime

# Ajouter ou mettre à jour un produit par URL
from datetime import datetime

def add_or_update_products(collection, products, theme=None):
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

    for product in products:
        # Récupération des valeurs avec None par défaut si elles ne sont pas fournies
        asin = product.get("asin")
        name = product.get("name", None)
        url = product.get("url", None)
        price = product.get("price", None)
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
