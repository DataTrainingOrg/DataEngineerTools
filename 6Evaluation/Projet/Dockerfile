# Utiliser l'image officielle de Python 3.10
FROM python:3.10-slim

# Créer un répertoire de travail
WORKDIR /app

# Copier tous les fichiers du projet dans l'image Docker
COPY . .

# Installer les dépendances système nécessaires (si besoin)
RUN apt-get update && apt-get install -y \
    # Ajoutez ici les bibliothèques système dont vous pourriez avoir besoin, si nécessaire
    && apt-get clean

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le script d'entrée et rendre le fichier exécutable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# CREER le fichier mongodb-keyfile/mongodb-key  dans le conteneur et lui attribuer les bonnes permissions
RUN openssl rand -base64 756 > /mongodb-keyfile
RUN chmod 600 /mongodb-keyfile && chown root:root /mongodb-keyfile



# Print the permissions of the key file to a log file
# Affiche directement dans les logs de build
RUN echo ls -l /mongodb-key || echo "Le fichier /mongodb-key n'existe pas ou il y a un problème de permissions."

# Exposer le port de l'application Dash
EXPOSE 8050

# Définir le script d'entrée comme commande par défaut
CMD ["/entrypoint.sh"]
