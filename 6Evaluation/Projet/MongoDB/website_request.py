from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import time

# Connexion à MongoDB
def connect_to_mongo():
    """
    Établit la connexion à MongoDB et retourne la collection.
    """
    client = MongoClient("mongodb://root:rootpassword@localhost:27017/admin")
    db = client["amazon_scrapping"]
    return db["scrapping_tasks"]

# Fonction pour ajouter une tâche
def add_task_to_db(task_type, task_value, interval_hours,page_number):
    """
    Ajoute une tâche dans la collection MongoDB.

    Args:
        task_type (str): Type de tâche ('link' ou 'theme').
        task_value (str): Valeur associée (URL ou thème).
        interval_hours (int): Intervalle en heures entre deux exécutions.

    Returns:
        dict: Résultat de l'opération, incluant l'identifiant du document inséré.
    """
    collection = connect_to_mongo()

    if task_type not in ["link", "theme"]:
        return {"error": "Le type doit être 'link' ou 'theme'."}

    if not isinstance(interval_hours, int) or interval_hours <= 0:
        return {"error": "L'intervalle doit être un entier positif."}

    task_document = {
        "type": task_type,
        "value": task_value,
        "interval_hours": interval_hours,
        "last_executed": None,  # Pas encore exécuté
        "created_at": datetime.utcnow()
    }

    result = collection.insert_one(task_document)
    return {"success": True, "inserted_id": str(result.inserted_id)}

# Fonction pour exécuter la tâche de scrapping
def perform_scrapping(task):
    """
    Logique pour effectuer le scrapping pour une tâche donnée.

    Args:
        task (dict): Détails de la tâche.
    """
    print(f"Scrapping for {task['value']} (Type: {task['type']})")
    # Ajoute ici la logique de scrapping réelle

# Fonction principale vérifiant les tâches à exécuter
def check_and_execute_tasks():
    """
    Vérifie les tâches stockées dans la base de données et exécute celles qui sont prêtes.
    """
    collection = connect_to_mongo()
    now = datetime.utcnow()

    tasks = collection.find()
    for task in tasks:
        last_executed = datetime.fromisoformat(task["last_executed"]) if task.get("last_executed") else None
        interval = timedelta(minutes=task["interval_hours"])
        #/!\ remetttre heure et pas laisser min
        if not last_executed or now - last_executed >= interval:
            perform_scrapping(task)

            # Mettre à jour le champ "last_executed" dans MongoDB
            collection.update_one(
                {"_id": task["_id"]},
                {"$set": {"last_executed": now.isoformat()}}
            )

# Planification avec APScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(check_and_execute_tasks, 'interval', minutes=1)  # Vérifie toutes les minutes
scheduler.start()

# Application principale
if __name__ == "__main__":
    print("Scheduler is running. Press Ctrl+C to exit.")

    # # Ajout d'exemples de tâches
    # print(add_task_to_db("link", "https://example.com2", 1,null))
    # print(add_task_to_db("theme", "machine learning2", 1,1))

    try:
        while True:
            time.sleep(1)  # Maintient l'application active
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
