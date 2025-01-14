FROM python:3.10-slim

# Créer un répertoire de travail
WORKDIR /app

# Copier tous les fichiers du projet dans l'image Docker
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le script d'entrée et rendre le fichier exécutable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exposer le port de l'application Dash
EXPOSE 8050

# Définir le script d'entrée comme commande par défaut
CMD ["/entrypoint.sh"]
