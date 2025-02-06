from datetime import datetime, timedelta

def perform_scrapping_for_task(task):
    """Simule l'exécution d'une tâche de scraping."""
    print(f"Scraping effectué pour {task['name']}.")

def check_and_execute_tasks(tasks):
    """
    Vérifie les tâches stockées et exécute celles qui sont prêtes.

    Args:
        tasks (list): Liste des tâches (simule une collection MongoDB).
    """
    now = datetime.utcnow()
    print("Vérification des tâches...", flush=True)

    for task in tasks:
        last_executed = None

        if task.get("last_executed"):
            if isinstance(task["last_executed"], datetime):
                last_executed = task["last_executed"]
            elif isinstance(task["last_executed"], str):
                try:
                    last_executed = datetime.fromisoformat(task["last_executed"])
                except ValueError:
                    print(f"Format invalide pour last_executed: {task['last_executed']}")

        interval = timedelta(seconds=task["interval_hours"])

        # Vérifier si la tâche doit être exécutée
        if not last_executed or now - last_executed >= interval:
            print(f"Exécution de la tâche: {task['name']}", flush=True)
            perform_scrapping_for_task(task)

            # Mettre à jour la date d'exécution (simule une mise à jour en BDD)
            task["last_executed"] = now.isoformat()
            print(f"Tâche '{task['name']}' mise à jour avec last_executed = {task['last_executed']}")

# Simuler une liste de tâches
tasks_data = [
    {"name": "Tâche 1", "interval_hours": 10, "last_executed": None},
    {"name": "Tâche 2", "interval_hours": 5, "last_executed": (datetime.utcnow() - timedelta(seconds=6)).isoformat()},
    {"name": "Tâche 3", "interval_hours": 20, "last_executed": datetime.utcnow().isoformat()},
]

# Tester la fonction
check_and_execute_tasks(tasks_data)

now = datetime.utcnow()
print(now)
print(timedelta(seconds=5))  # Affiche 0:00:05

print(now-timedelta(seconds=5))  # Affiche 2021-09-29 14:45:45.123456