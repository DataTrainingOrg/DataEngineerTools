=============
Data Engineer
=============

Cours données dans le cadre du OUAP-4314 : Data Engineering sur la récupération de données WEB et l'intégration dans un flux de stockage basé sur MongoDB.

Github
------

Si vous ne disposez pas déjà d'un compte `Github <https://github.com>`_, il faut en créer un.

Forkez (avec le bouton ``Fork`` en haut à droite) ce projet. Il contient toutes les ressources nécessaires pour ce cours. Vous pourrez ajouter des notes, modifier le code, et pousser votre projet final directement pour que l'on puisse l'évaluer.

Pour commencer à travailler il vous faut cloner le projet dans votre répertoire (local) de travail : 

.. code-block:: bash

  $:~/> cd <WORKDIR>
  $:~/<WORKDIR> > git clone https://github.com/<GITHUB_NAME>/esiee_lectures
  $:~/<WORKDIR> > ls
  esiee_lectures
  $:~/<WORKDIR> > cd esiee_lectures/Data\ Engineer/
  $:~/<WORKDIR>/esiee_lectures/Data Engineer> ls
  Dockerfile  Evaluation	Introduction  Mongo  README.rst  requirements.txt  Scrapy
  
Docker
------

Afin de pouvoir travailler dans les meilleurs conditions, nous allons travailler à partir de la technologie Docker. Docker est une technologie de conteneurs utilisés par les DevOps pour permettre un déploiement plus simple et plus rapide. Par rapport à des machines virtuelles, Docker est plus léger.

.. image:: Introduction/images/docker-vm-container.png

Pour créer l'image utilisée dans le projet : 

.. code-block:: bash

  > docker build -t image_OUAP  .

A partir de cette image, on peut créer une instance (conteneur) dans lequel on va travailler: 

.. code-block:: bash

  > docker run -it --name conteneur_OUAP -v <WORKDIR>/esiee_lectures/Data\ Engineer/:/home/dev/code/ image_OUAP
 
Il n'est pas rare de lancer plusieurs conteneurs instanciés à partir de la même image. Contrairement à une machine virtuelle, docker utilise la même base et les mêmes composants pour tous ces conteneurs et donc réduire l'impact mémoire de ces derniers.

Dans ce cours nous allons utiliser MongoDB. Normalement il est installé par défaut sur toutes les machines. Si toutefois, il ne l'était pas ou si vous souhaitez travailler dans un autre environnment il faut envisager d'utiliser un conteneur Mongo.

.. code-block:: bash

  docker run --name mon-mongo -v <STOCKAGE_DIRECTORY>:/data/db -p 27017:27017 -d mongo
   
Consignes
---------
  
L'ensemble des exercices présents dans les différents cours doivent être placés dans des fichiers Python séparés (et commentés) dans le dossier ``Evaluation``. 

Les fichiers Python doivent être nommés de la façon suivante : ``<PARTIE>_Exercice<NO_EXERCICE>.py`` 

Par exemple : ``Introduction_Exercice2.py`` 

Le projet doit être placé dans le dossier ``Evaluation/Projet`` avec la totalité du code de l'application. Vous devez aussi remplir les fichiers README.rst correspondants, ce qui permet de faire une documentation élémentaire.

Il est conseillé de travailler en local lors de chaque séance, puis de pusher son travail en fin de séance sur le repository Github.

.. code-block:: bash
  
   > git add .
   > git commit -m "message explicatif"
   > git push origin master
   
Au début de la séance suivante, on récupère les éventuelles modifications apportées entre temps avec  :
 
.. code-block:: bash
  
   > git pull

Si vous travaillez sur une machine locale différente, il faut recloner le projet. 
