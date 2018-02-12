=============
Data Engineer
=============

Cours données dans le cadre du OUAP-4314 : Data Engineering sur la récupération de données WEB et l'intégration dans un flux de stockage basé sur MongoDB.

Dans un premier temps , pour suivre au mieux ce cours, je vous propose de ``forker`` ce projet afin de pouvoir le modifier comme bon vous semble. Vous pourrez rajouter des notes, modifier le code, et pousser votre projet final directement pour que l'on puisse le corriger.

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







