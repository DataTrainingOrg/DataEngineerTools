import re

def is_url(input_value):
    """
    Vérifie si l'entrée utilisateur est un lien valide (autre qu'Amazon).

    Parameters:
        input_value (str): La valeur entrée par l'utilisateur.

    Returns:
        bool: True si c'est un lien valide et non un lien Amazon, False sinon.
    """
    url_regex = re.compile(
        r'^(https?:\/\/)?'  # Protocole (http ou https) facultatif
        r'([a-z0-9.-]+\.)?[a-z0-9.-]+\.[a-z]{2,10}'  # Domaine (ex: example.com, sub.example.co.uk)
        r'(:\d+)?'  # Port facultatif (ex: :8080)
        r'(\/[^\s]*)?$',  # Chemin facultatif après le domaine
        re.IGNORECASE  # Insensible à la casse
    )

    if not input_value or not url_regex.match(input_value):
        return False

   

    return True




def is_amazon_url(input_value):
    """
    Détermine si l'entrée utilisateur est un lien Amazon valide ou un mot clé.

    Parameters:
        input_value (str): La valeur entrée par l'utilisateur.

    Returns:
        str: "Lien Amazon" si l'entrée est un lien Amazon valide, "Mot clé" sinon.
    """
    # Expression régulière pour détecter les liens Amazon
    amazon_url_regex = re.compile(
        r'^(https?:\/\/)?(www\.)?amazon\.[a-z]{2,3}(\/\S*)?$'  # Lien Amazon
    )

    if amazon_url_regex.match(input_value):
        return True
    return False



def clean_text(text):
    """
    Remplace les espaces par des tirets et supprime les caractères spéciaux d'une chaîne de caractères,
    tout en identifiant les caractères non autorisés.

    Parameters:
        text (str): La chaîne de caractères à traiter.

    Returns:
        tuple: La chaîne nettoyée et une chaîne des caractères supprimés, séparés par des espaces.
    """
    if not isinstance(text, str):
        raise ValueError("Le paramètre 'text' doit être une chaîne de caractères.")
    
    # Remplacer les espaces par des tirets
    text = text.replace(" ", "-")
    
    # Trouver tous les caractères non autorisés
    invalid_chars = re.findall(r'[^a-zA-Z0-9\-]', text)  
    
    # Supprimer les caractères non autorisés
    cleaned_text = re.sub(r'[^a-zA-Z0-9\-]', '', text)  

    # Convertir la liste des caractères non autorisés en une chaîne unique
    invalid_chars_str = " ".join(sorted(set(invalid_chars)))  # Tri et suppression des doublons
    
    return cleaned_text, invalid_chars_str

def del_sponsor(products):
    """
    Supprime les éléments de la liste dont le contenu est sponsorisé.
    Recherche des produits contenant l'un des mots-clés dans leur nom.
    
    :param products: Liste des produits à filtrer
    :return: La liste filtrée et le nombre d'éléments supprimés
    """
    # Liste de mots-clés à rechercher dans les noms des produits
    keywords = ["publicité sponsorisée", "promotion spéciale", "sponsorisée", "contenu sponsorisé", "offre sponsorisée", "pub", "publicité", "sponsorship"]
    
    count = 0
    print("Avant :", products)

    # Filtrer les produits en excluant ceux qui contiennent l'un des mots-clés
    filtered_products = [
        product for product in products 
        if not any(keyword in product.get("name", "").strip().lower() for keyword in keywords)
    ]
    
    # Calculer le nombre d'éléments supprimés
    count = len(products) - len(filtered_products)
    
    # Retourner la nouvelle liste et le nombre d'éléments supprimés
    print("Après suppression, nombre d'éléments supprimés :", count)
    print(filtered_products)
    
    return filtered_products, count
