from datetime import datetime, timedelta
import sys
import os
import time
import pymongo

# Ajoute le répertoire mongo_requests
sys.path.append('../mongo_requests/')
from mongo import add_or_update_products

# Ajoute le répertoire scrapping
sys.path.append('../scrapping/')
from scrapping_script import scrape_products_info, scrape_product_details_with_image


def perform_scrapping_for_task(task, collection, product_collection):
    """
    Exécute le scrapping pour une tâche spécifique et met à jour la base de données.

    Args:
        collection: Collection MongoDB des tâches.
        task (dict): La tâche à exécuter.
        product_collection: Collection MongoDB pour stocker les produits scrappés.

    Returns:
        dict: Indique si l'opération a réussi.
    """
    now = datetime.utcnow()

    # Vérifier si c'est un thème ou une URL
    theme = task["theme"]
    url = task["URL"]

    if theme is not None:
        print(f"Lancement du scrapping pour le thème : {theme}")
        sys.stdout.flush()
        products_info = scrape_products_info(theme)  # Scrapping par thème
        products = products_info["products"]

    elif url is not None:
        print(f"Lancement du scrapping pour l'URL : {url}")
        sys.stdout.flush()
        product = scrape_product_details_with_image(url)  # Scrapping par URL
        products = [product] if product else []

    else:
        return {"error": "Aucun thème ni URL valide trouvé dans la tâche."}

    if not products:
        return {"error": "Aucun produit trouvé."}

    # Ajouter ou mettre à jour les produits dans la base de données
    result = add_or_update_products(product_collection, products, url, theme)

    # Mettre à jour la tâche avec l'heure d'exécution et de refresh
    collection.update_one(
        {"_id": task["_id"]},
        {"$set": {
            "last_executed": now.isoformat()
        }}
    )

    return result



def check_and_execute_tasks(collection,product_collection):
    """
    Vérifie les tâches stockées dans la base de données et exécute celles qui sont prêtes.

    Args:
        collection: Collection MongoDB contenant les tâches.
    """
    now = datetime.utcnow()
    tasks = collection.find()
    print("Vérification des tâches...", flush=True)
    sys.stdout.flush()
    for task in tasks:
        last_executed = None
        print("task",task,flush=True)
        sys.stdout.flush()
        
        last_executed_t = task["last_executed"]
        if last_executed_t:
            if isinstance(last_executed_t, datetime):
                last_executed = last_executed_t
            elif isinstance(last_executed_t, str):
                try:
                    last_executed = datetime.fromisoformat(last_executed_t)
                except ValueError:
                    print(f"Format invalide pour last_executed: {task['last_executed']}")
        
        interval = timedelta(hours=task["interval_hours"]) #/!\ interval en heures
        
        # Vérifier si la tâche doit être exécutée
        if not last_executed or now - last_executed >= interval:
            print("task",task,flush=True)
            sys.stdout.flush()
            perform_scrapping_for_task(task, collection, product_collection)

            collection.update_one(
                {"_id": task["_id"]},
                {"$set": {
                    "last_executed": datetime.utcnow()
                }}
            )


# Chargement des variables d'environnement
MONGO_HOST = os.getenv("MONGO_HOST", "mongo1")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_REPLICA_SET = os.getenv("MONGO_REPLICA_SET", "rs0")
MONGO_DB = os.getenv("MONGO_DB", "amazon_web_scraper")
MONGO_DB_TABLE_TRACKER = os.getenv("MONGO_DB_TABLE_TRACKER", "track_list")
MONGO_DB_TABLE = os.getenv("MONGO_DB_TABLE", "products")

# Connexion à MongoDB
while True:
    try:
        print("Task", flush=True)
        print("Connexion à MongoDB...", flush=True)
        mongo_uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/?directConnection=true&serverSelectionTimeoutMS=2000&replicaSet={MONGO_REPLICA_SET}"
        client = pymongo.MongoClient(mongo_uri)
        client.admin.command('ping')  # Test de la connexion
        print("Connexion à MongoDB réussie!", flush=True)
        break
    except pymongo.errors.ConnectionFailure as e:
        print("Erreur de connexion à MongoDB:", e, flush=True)
        time.sleep(5)

db = client[MONGO_DB]
track_collection = db[MONGO_DB_TABLE_TRACKER]
product_collection = db[MONGO_DB_TABLE]


print("Boucle", flush=True)
# Application principale
if __name__ == "__main__":
    print("Scheduler is running. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(60)  # Maintient l'application active
            check_and_execute_tasks(track_collection,product_collection)
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")