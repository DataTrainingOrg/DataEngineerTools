=============
Data Engineer
=============

Cours données dans le cadre du OUAP-4314 : Data Engineering sur la récupération de données WEB et l'intégration dans un flux de stockage basé sur MongoDB.

Github
------

Si vous ne disposez pas déjà d'un compte `Github <https://github.com>`_, il faut en créer un.

Forkez (avec le bouton ``Fork`` en haut à droite) ce projet. Il contient toutes les ressources nécessaires pour ce cours. Vous pourrez ajouter des notes, modifier le code, et pousser votre projet final directement pour que l'on puisse l'évaluer.


Docker
------
Docker est une technologie de conteneurs utilisés par les DevOps pour permettre un déploiement plus simple et plus rapide. Par rapport à des machines virtuelles, Docker est plus léger.

.. image:: Introduction/images/docker-vm-container.png
Dans un deuxième temps, afin de pouvoir travailler dans les meilleurs conditions, nous allons travailler à partir de la technologie Docker.


Pour déployer le conteneur MongoDB : 

.. code-block:: bash

  docker run --name mon-mongo -v <STOCKAGE_DIRECTORY>:/data/db -p 27017:27017 -d mongo
  
Maintenant pour créer le container pour votre projet : 

.. code-block:: bash

  docker build -t <IMAGE_NAME> .
  docker run -it --name <CONTAINER_NAME> -v <PROJECT_DIRECTORY>:/home/dev/code/ <IMAGE_NAME>
  
  
L'ensemble des exercices présents dans les différents cours doivent être mis dans dans fichier Python séparés et commentés. Vous devrez pousser tous vos fichiers dans le dossier évaluation. Les fichiers Python doivent être nommés de la façon suivante : ``<PARTIE>_Exercice<NO_EXERCICE>.py`` 

Le projet doit être place dans le dossier projet avec le code de l'application Flask et de la spider Scrapy. 







