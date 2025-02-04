from datetime import datetime

# Ajouter ou mettre à jour un produit par URL
def add_or_update_product_url(collection, asin, name, url, price, image_url):
    product = {
        "asin": asin,
        "name": name,
        "url": url,
        "theme": None,  # Thème est null pour un produit par URL
        "price_history": [{"price": price, "timestamp": datetime.utcnow()}],
        "image_url": image_url
    }
    result = collection.update_one(
        {"asin": asin},
        {
            "$set": {"name": name, "url": url, "theme": None, "image_url": image_url},
            "$push": {"price_history": {"price": price, "timestamp": datetime.utcnow()}}
        },
        upsert=True
    )
    return {"success": result.modified_count > 0 or result.upserted_id is not None}

# Ajouter ou mettre à jour un thème

def add_or_update_product_theme(collection, theme, products):
    for product in products:
        # Si un champ est manquant, il est ajouté avec la valeur None
        asin = product.get("asin")
        name = product.get("name", None)
        url = product.get("url", None)
        price = product.get("price", None)
        image_url = product.get("image_url", None)
        
        # Ajouter ou mettre à jour le produit via add_or_update_product_url
        result = add_or_update_product_url(
            collection,
            asin,
            name,
            url,
            price,
            image_url
        )
        
        # Une fois que le produit est ajouté ou mis à jour, on applique le thème
        if result["success"]:
            collection.update_one(
                {"asin": asin},
                {"$set": {"theme": theme}}
            )
    
    return {"success": True}

# Récupérer l'aperçu d'un produit par URL
def get_product_preview_by_url(collection, asin):
    product = collection.find_one({"asin": asin}, {"_id": 0, "name": 1, "image_url": 1, "theme": 1})
    return product if product else {"error": "Produit non trouvé"}

# Récupérer l'aperçu d'un thème
def get_product_preview_by_theme(collection, theme):
    theme_data = collection.find_one({"theme": theme}, {"_id": 0, "theme": 1, "products.name": 1, "products.image_url": 1})
    return theme_data if theme_data else {"error": "Thème non trouvé"}
