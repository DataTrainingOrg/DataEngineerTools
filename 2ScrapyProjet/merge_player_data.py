import json
import os

def merge_player_data():
    # Vérifier si les fichiers existent et ne sont pas vides
    if not os.path.exists('player_info.json') or os.path.getsize('player_info.json') == 0:
        print("Erreur : Le fichier 'player_info.json' est vide ou n'existe pas.")
        return

    if not os.path.exists('career_performance.json') or os.path.getsize('career_performance.json') == 0:
        print("Erreur : Le fichier 'career_performance.json' est vide ou n'existe pas.")
        return

    # Charger les deux fichiers JSON
    with open('player_info.json', 'r', encoding='utf-8') as f:
        player_info_list = json.load(f)
    
    with open('career_performance.json', 'r', encoding='utf-8') as f:
        career_performance_list = json.load(f)
    
    # Compter les IDs uniques dans les fichiers
    player_info_ids = {item['player_id'] for item in player_info_list}
    career_performance_ids = {item['player_id'] for item in career_performance_list}
    
    # Afficher le nombre d'IDs différents dans chaque fichier
    print(f"Nombre d'ID uniques dans player_info.json : {len(player_info_ids)}")
    print(f"Nombre d'ID uniques dans career_performance.json : {len(career_performance_ids)}")
    
    # Créer des dictionnaires pour un accès rapide par player_id
    player_info_dict = {item['player_id']: item['Player Info'] for item in player_info_list}
    career_performance_dict = {item['player_id']: item['Career Performance'] for item in career_performance_list}
    
    # Fusionner les deux listes de données
    merged_data = []
    for player_id in player_info_dict:
        # Récupérer les données du joueur et ses performances
        player_info = player_info_dict.get(player_id, {})
        career_performance = career_performance_dict.get(player_id, [])

        # Fusionner les données
        merged_player_data = {
            "player_id": player_id,
            "Player Info": player_info,
            "Career Performance": career_performance
        }
        
        # Ajouter à la liste fusionnée
        merged_data.append(merged_player_data)
    
    # Sauvegarder la fusion dans un nouveau fichier JSON
    with open('merged_player_data.json', 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)

    print(f"Fusion terminée, {len(merged_data)} joueurs ont été fusionnés.")

# Appel de la fonction pour réaliser la fusion
merge_player_data()
