# Utiliser l'image officielle MongoDB
FROM mongo:latest

# Créer un répertoire pour la clé de sécurité
RUN mkdir -p /MongoDB/mongodb-keyfile

# Générer une clé aléatoire pour le replica set
RUN openssl rand -base64 756 > /MongoDB/mongodb-keyfile/mongodb-key && \
    chmod 600 /MongoDB/mongodb-keyfile/mongodb-key && \
    chown mongodb:mongodb /MongoDB/mongodb-keyfile/mongodb-key


# Exposer le port par défaut de MongoDB
EXPOSE 27017

# Exposer la clé pour la persistance
VOLUME ["/MongoDB/mongodb-keyfile"]

# Commande pour démarrer MongoDB avec Replica Set et clé de sécurité
CMD ["mongod", "--replSet", "rs0", "--bind_ip_all", "--keyFile", "/MongoDB/mongodb-keyfile/mongodb-key"]
