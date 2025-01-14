from apscheduler.schedulers.background import BackgroundScheduler
import time
from MongoDB.website_request import check_and_execute_tasks


# Planification avec APScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(check_and_execute_tasks, 'interval', heures=1)  # Vérifie toutes les heures
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
