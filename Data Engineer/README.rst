=============
Data Engineer
=============

Cours données dans le cadre du OUAP-4314 : Data Engineering sur la récupération de données WEB et l'intégration dans un flux de stockage basé sur MongoDB.

Dans un premier temps , pour suivre au mieux ce cours, je vous propose de ``forker`` ce projet afin de pouvoir le modifier comme bon vous semble. Vous pourrez rajouter des notes, modifier le code, et pousser votre projet final directement pour que l'on puisse le corriger.

Dans un deuxième temps, afin de pouvoir travailler dans les meilleurs conditions, nous allons travailler à partir de la technologie Docker.

Pour déployer le conteneur MongoDB : 

.. code-block:: bash

  docker run --name mon-mongo -v <VOTRE_REPERTOIRE_DE_STOCKAGE>:/data/db -p 27017:27017 -d mongo








