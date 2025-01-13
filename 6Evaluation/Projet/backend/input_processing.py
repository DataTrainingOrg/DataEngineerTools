import re

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

