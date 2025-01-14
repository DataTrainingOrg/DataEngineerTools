from pymongo import MongoClient
from datetime import datetime, timedelta
from MongoDB.product_storage_request import add_product_from_url,add_products_from_theme,update_price_history,sync_theme_products
from Scrapping.Amazon_scrap import scrape_product_details_from_url,scrape_product_by_name,scrape_price_from_asin
# Connexion à MongoDB
def connect_to_mongo(table):
    """
    Établit la connexion à MongoDB et retourne la collection.
    """
    client = MongoClient("mongodb://root:rootpassword@mongodb:27017/admin")
    db = client["amazon_scrapping"]
    return db[table]

# Fonction pour ajouter une tâche
def add_task_to_db(task_type, task_value, interval_hours):
    """
    Ajoute une tâche dans la collection MongoDB.

    Args:
        task_type (str): Type de tâche ('link' ou 'theme').
        task_value (str): Valeur associée (URL ou thème).
        interval_hours (int): Intervalle en heures entre deux exécutions.

    Returns:
        dict: Résultat de l'opération, incluant l'identifiant du document inséré.
    """
    collection = connect_to_mongo("scrapping_tasks")

    if task_type not in ["link", "theme"]:
        return {"error": "Le type doit être 'link' ou 'theme'."}

    if not isinstance(interval_hours, int) or interval_hours <= 0:
        return {"error": "L'intervalle doit être un entier positif."}

    task_document = {
        "type": task_type,
        "value": task_value,
        "interval_hours": interval_hours,
        "asin": None,
        "last_executed": datetime.utcnow(),  # Pas encore exécuté
        "created_at": datetime.utcnow()
    }
    asin,error=perform_scrapping(task_document,first=True)
    print(error)
    task_document["asin"]=asin
    result = collection.insert_one(task_document)
    return {"success": True, "inserted_id": str(result.inserted_id)}

# Fonction pour exécuter la tâche de scrapping
def perform_scrapping(task,first=False):
    """
    Logique pour effectuer le scrapping pour une tâche donnée.

    Args:
        task (dict): Détails de la tâche.
    """
    print(f"Scrapping for {task['value']} (Type: {task['type']})")
    # logique de scrapping réelle
    task_type,task_value=task["type"], task["value"]
    if first:
        if task_type == "link":
            print("scrapping link")
            val=scrape_product_details_from_url(task_value)
            if val is not None:
                asin,name,price =val["asin"],val["name"],val["price"]
                add_product_from_url(asin,name,price)
                return asin,{"success": "Scrapping réussi"}
            else:
                return asin,{"error": "Erreur lors du scrapping"}
            
        elif task_type == "theme":
            print("scrapping theme")
            products=scrape_product_by_name(task_value)
            if products is not None:
                add_products_from_theme(task_value,products)
                return None,{"success": "Scrapping réussi"}
            else:
                return None,{"error": "Erreur lors du scrapping"}
    else:
        if task_type == "link":
            asin=task["asin"]
            price=scrape_price_from_asin(asin)
            update_price_history(asin,price)
        elif task_type == "theme":
            products=scrape_product_by_name(task_value)
            if products is not None:
                sync_theme_products(task_value,products)
            

# Fonction principale vérifiant les tâches à exécuter
def check_and_execute_tasks():
    """
    Vérifie les tâches stockées dans la base de données et exécute celles qui sont prêtes.
    """
    collection = connect_to_mongo("scrapping_tasks")
    now = datetime.utcnow()

    tasks = collection.find()
    for task in tasks:
        last_executed = None
        if task.get("last_executed"):
            # Vérifier si last_executed est déjà un objet datetime
            if isinstance(task["last_executed"], datetime):
                last_executed = task["last_executed"]
            elif isinstance(task["last_executed"], str):
                # Convertir la chaîne en datetime
                last_executed = datetime.fromisoformat(task["last_executed"])
            else:
                print(f"Valeur inattendue pour last_executed: {task['last_executed']}")

        interval = timedelta(minutes=task["interval_hours"])
        #/!\ remetttre heure et pas laisser min
        if not last_executed or now - last_executed >= interval:
            perform_scrapping(task)

            # Mettre à jour le champ "last_executed" dans MongoDB
            collection.update_one(
                {"_id": task["_id"]},
                {"$set": {"last_executed": now.isoformat()}}
            )



