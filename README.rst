=============
Data Engineer
=============

Cours donné dans le cadre du OUAP-4314 : Data Engineering sur la récupération de données WEB et l'intégration dans un flux de stockage basé sur MongoDB.

Github
------

Si vous ne disposez pas déjà d'un compte `Github <https://github.com>`_, il faut en créer un.

Forkez (avec le bouton ``Fork`` en haut à droite) ce projet. Il contient toutes les ressources nécessaires pour ce cours. Vous pourrez ajouter des notes, modifier le code, et pousser votre projet final directement pour que l'on puisse l'évaluer.

Pour commencer à travailler il vous faut cloner le projet dans votre répertoire (local) de travail : 

.. code-block:: bash

  $:~/> cd <WORKDIR>
  $:~/<WORKDIR> > git clone https://github.com/<GITHUB_NAME>/OUAP-4314
  $:~/<WORKDIR> > ls
  esiee_lectures
  $:~/<WORKDIR> > cd OUAP-4314/
  $:~/<WORKDIR>/OUAP-4314> ls
  Dockerfile  Evaluation	Introduction  Mongo  README.rst  requirements.txt  Scrapy
  
  
Si au fil du temps j'ai besoin de modifier le contenu en temps réel vous pouvez garder votre projet à jour en ajoutant ces quelques commandes :

.. code-block:: bash

  $:~/> cd <WORKDIR>
  $:~/<WORKDIR> > cd OUAP-4314/
  $:~/<WORKDIR>/OUAP-4314>git remote add upstream https://github.com/rcourivaud/OUAP-4314
  $:~/<WORKDIR>/OUAP-4314>git fetch upstream

Maintenant pour mettre à jour le projet :

  $:~/<WORKDIR>/OUAP-4314>git pull upstream master
  
Docker
------

Afin de pouvoir travailler dans les meilleurs conditions, nous allons travailler à partir de la technologie Docker. Docker est une technologie de conteneurs utilisés par les DevOps pour permettre un déploiement plus simple et plus rapide. Par rapport à des machines virtuelles, Docker est plus léger.

.. image:: Introduction/images/docker-vm-container.png

Créer une image
...............

Pour créer l'image utilisée dans le projet, on utilise le ``Dockerfile`` présent dans le répertoire (jeter un oeil à ce fichier pour comprendre les composants utilisés)  : 

.. code-block:: bash

  > docker build -t image_ouap  .
  
  Sending build context to Docker daemon  26.97MB
  Step 1/6 : FROM python:3
   ---> c1e459c00dc3
  Step 2/6 : RUN mkdir /home/dev/ && mkdir /home/dev/code/
   ---> Running in 7b1a56c8f507
   ---> 456761cb01d3
  Removing intermediate container 7b1a56c8f507
  Step 3/6 : WORKDIR /home/dev/code/
   ---> abcb9015d45c
  Removing intermediate container a5bc16f1b985
  Step 4/6 : COPY . .
   ---> 6ad3d3ab3d27
  Removing intermediate container 4c98a0951342
  Step 5/6 : RUN pip install --no-cache-dir -r requirements.txt
   ---> Running in b6646ab9dd67
  Collecting beautifulsoup4==4.6.0 (from -r requirements.txt (line 1))
    Downloading beautifulsoup4-4.6.0-py3-none-any.whl (86kB)
  Collecting Flask==0.12.2 (from -r requirements.txt (line 2))
    Downloading Flask-0.12.2-py2.py3-none-any.whl (83kB)
  ...
  Step 6/6 : CMD /bin/bash
   ---> Running in a77c1a7b0f08
   ---> f5da69f1f76c
  Removing intermediate container a77c1a7b0f08
  Successfully built f5da69f1f76c

L'opération se termine correctement si ``Successfully built`` est affiché. La chaîne alphanumérique qui suit permet d'identifier l'image sans ambiguité.

Créer un conteneur
..................

A partir de cette image, on peut créer une instance (conteneur) dans lequel on va travailler (on remplacera ``<WORKDIR>`` par son propre répertoire de travail) : 

.. code-block:: bash

  > docker run -it --name conteneur_ouap -v <WORKDIR>/esiee_lectures/Data\ Engineer/:/home/dev/code/ image_ouap
  
  root@a74861d489f5:/home/dev/code# python
  Python 3.6.4 (default, Dec 21 2017, 01:35:12) 
  [GCC 4.9.2] on linux
  Type "help", "copyright", "credits" or "license" for more information.
  >>> 

Le prompt ``#`` est celui du conteneur dans lequel on est ``root``. On peut alors lancer les commandes incluses dans le conteneur(ici l'interpréteur Python). 
 
.. note::

  Il n'est pas rare de lancer plusieurs conteneurs instanciés à partir de la même image. Contrairement à une machine virtuelle, docker utilise la même base et les mêmes composants pour tous ces conteneurs et donc réduire l'impact mémoire de ces derniers.
  
MongoDB
.......

Dans ce cours nous allons utiliser MongoDB. Normalement il est installé par défaut sur toutes les machines. Si toutefois, il ne l'était pas ou si vous souhaitez travailler dans un autre environnment, il faut envisager de lancer un conteneur Mongo en parallèle.

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
