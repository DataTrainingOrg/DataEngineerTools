from pymongo import MongoClient
from datetime import datetime

class MongoDBHandler:
    def __init__(self, connection_string="mongodb://root:rootpassword@localhost:27017/admin", database_name="product_tracker"):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def insert_product_data(self, collection_name, asin, title, price, product_url):
        collection = self.get_collection(collection_name)
        document = {
            "_id": asin,
            "title": title,
            "price": price,
            "time": datetime.utcnow(),
            "url": product_url,
        }
        try:
            collection.insert_one(document)
            print(f"Produit {title} inséré avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'insertion du produit : {e}")

    def update_product_title(self, collection_name, asin, new_title):
        collection = self.get_collection(collection_name)
        try:
            result = collection.update_one({"_id": asin}, {"$set": {"title": new_title}})
            if result.matched_count > 0:
                print(f"Titre du produit avec ASIN {asin} mis à jour avec succès.")
            else:
                print(f"Aucun produit trouvé avec l'ASIN {asin}.")
        except Exception as e:
            print(f"Erreur lors de la mise à jour du titre : {e}")

    def update_product_price(self, collection_name, asin, new_price):
        collection = self.get_collection(collection_name)
        price_update = {
            "price": new_price,
            "date": datetime.utcnow(),
        }
        try:
            result = collection.update_one(
                {"_id": asin},
                {
                    "$push": {"price_history": price_update},
                    "$set": {"price": new_price},
                },
            )
            if result.matched_count > 0:
                print(f"Prix pour le produit {asin} mis à jour avec succès.")
            else:
                print(f"Aucun produit trouvé avec l'ASIN {asin}.")
        except Exception as e:
            print(f"Erreur lors de la mise à jour du prix : {e}")

    def is_product_in_db(self, collection_name, asin):
        collection = self.get_collection(collection_name)
        return collection.find_one({"_id": asin}) is not None

    def get_product_data(self, collection_name, asin):
        collection = self.get_collection(collection_name)
        product = collection.find_one({"_id": asin})
        if product:
            print(f"Produit trouvé : {product['title']}")
            print(f"Prix actuel : {product['price']}")
            print(f"Historique des prix : {product.get('price_history', [])}")
        else:
            print(f"Produit avec ASIN {asin} non trouvé.")

    def get_price_history(self, collection_name, asin):
        collection = self.get_collection(collection_name)
        product = collection.find_one({"_id": asin})
        if product:
            print(f"Historique des prix pour {product['title']} (ASIN: {asin}):")
            for entry in product.get("price_history", []):
                print(f"Prix : {entry['price']} - Date : {entry['date']}")
        else:
            print(f"Produit avec ASIN {asin} non trouvé.")

    def get_all_products(self, collection_name):
        collection = self.get_collection(collection_name)
        products = collection.find()
        for product in products:
            print(f"ASIN : {product['_id']} - Titre : {product['title']} - Prix actuel : {product['price']}")

    def reset_collection(self, collection_name):
        collection = self.get_collection(collection_name)
        result = collection.delete_many({})
        return result.deleted_count

    def reset_all(self):
        collections = self.db.list_collection_names()
        for collection in collections:
            self.db.drop_collection(collection)
        return collections
