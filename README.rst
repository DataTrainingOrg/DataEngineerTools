=============
Data Engineer
=============

Cours donné dans le cadre du DRIO-4203C : Data Engineering sur la récupération de données WEB et l'intégration dans un flux de stockage basé sur des bases de données NoSQL.

Github
------

Si vous ne disposez pas déjà d'un compte `Github <https://github.com>`_, il faut en créer un.

Forkez (avec le bouton ``Fork`` en haut à droite) ce projet. Il contient toutes les ressources nécessaires pour ce cours. Vous pourrez ajouter des notes, modifier le code, et pousser votre projet final directement pour que l'on puisse l'évaluer.

Pour commencer à travailler il vous faut cloner le projet dans votre répertoire (local) de travail : 

.. code-block:: bash

  $:~/> cd <WORKDIR>
  $:~/<WORKDIR> > git clone https://github.com/<GITHUB_NAME>/DataEngineerTools
  $:~/<WORKDIR> > cd DataEngineerTools/
  $:~/<WORKDIR> > ls
  Dockerfile  Evaluation  Introduction  Mongo  Pipfile  Pipfile.lock  README.rst  Scrapy  requirements.txt
  
Si au fil du temps j'ai besoin de modifier le contenu en temps réel vous pouvez garder votre projet à jour en ajoutant ces quelques commandes :

.. code-block:: bash

  $:~/> cd <WORKDIR>
  $:~/<WORKDIR>cd DataEngineerTools/
  $:~/<WORKDIR>/DataEngineerTools>git remote add basestream https://github.com/rcourivaud/DataEngineerTools
  $:~/<WORKDIR>/DataEngineerTools>git fetch basestream

Maintenant pour mettre à jour le projet :

  $:~/<WORKDIR>/DataEngineerTools>git pull basestream master

Pipenv
------

Vous pouvez voir qu'il y a trois fichiers disponibles dans le dossier de travail :
- requirements.txt
- Pipfile
- Pipfile.lock

Le fichier requirements.txt permet de lister toutes les librairies dont vous aurez besoin pour lancer et exécuter votre projet. Cette méthode est assez ancienne, vous pouvez cependant utiliser : 

.. code-block:: bash

  > pip install -r requirements.txt


Pipenv est développé par @kennethreitz, un pilier dans la communauté de Python, vous pouvez accéder à la documentation de pipenv https://pipenv.readthedocs.io/en/latest/

Pour faire simple, Pipenv permet de créer un environnment virtuel propre pour votre projet. Toutes les librairies sont listées dans le fichier `Pipfile`.
Le Pipfile.lock référence les versions d'installation de toutes les librairies, un hash est aussi stocké permettant de vérifier la cohérence avec les librairies déclarées et celles installées. 

Pour installer pipenv : 

.. code-block:: bash

  > pip install pipenv


Pour installer l'environnment : 

.. code-block:: bash

  > pipenv install

Vous pouvez ensuite lancer un terminal à l'interieur de cet environnment:

.. code-block:: bash

  > pipenv shell

Si vous voulez installer de nouvelles librairies dont vous avez besoin pour votre projet : 

.. code-block:: bash

  > pipenv install <votre_librairie>

Docker
------

Afin de pouvoir travailler dans les meilleurs conditions, nous allons travailler à partir de la technologie Docker. Docker est une technologie de conteneurs utilisés par les DevOps pour permettre un déploiement plus simple et plus rapide. Par rapport à des machines virtuelles, Docker est plus léger.

.. image:: 1Introduction/images/docker-vm-container.png

Créer une image
...............

Pour créer l'image utilisée dans le projet, on utilise le ``Dockerfile`` présent dans le répertoire (jeter un oeil à ce fichier pour comprendre les composants utilisés)  : 


.. code-block::

  # Image de laquelle on part
  # Tous les packages présents dans cette images seront installés dans la nouvelle créée
  FROM python:3.6

  # On lance des commandes directement dans le conteneur
  # Ici pour créer des dossiers
  RUN mkdir /home/dev/ && mkdir /home/dev/code/

  # On place le répertoire de travail du conteneur
  WORKDIR /home/dev/code/

  # Proxies de l'esiee
  ENV http_proxy http://147.215.1.189:3128 
  ENV https_proxy http://147.215.1.189:3128

  # On copie l'ensemble des fichiers directement dans le dossier de travail du conteneur
  COPY . .
  # On install les dépendances via pipenv
  RUN  pip install --upgrade pip &&  pip install pipenv && pipenv install --skip-lock

  # On lance un notebook jupyter dans l'environnment de pipenv
  CMD ["pipenv", "run",  "jupyter", "notebook" ]
  #CMD ["/bin/bash"]



.. code-block:: bash

  > docker build -t image_drio  .
  
  Sending build context to Docker daemon  40.41MB
  Step 1/6 : FROM python:3
  ---> c1e459c00dc3
  Step 2/6 : RUN mkdir /home/dev/ && mkdir /home/dev/code/
  ---> Using cache
  ---> bd6089ebb2af
  Step 3/6 : WORKDIR /home/dev/code/
  ---> Using cache
  ---> 8ff86602b0bf
  Step 4/6 : COPY . .
  ---> 2d52f96d1b3a
  Step 5/6 : RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile
  ---> Running in 78c89f488e9d
  Collecting pipenv
    Downloading https://files.pythonhosted.org/packages/90/06/0008f53835495fbbf6e31ced9119b8f517e1271bdefcf0d04aaa9f28dbf4/pipenv-2018.10.13-py3-none-any.whl (5.2MB)
  Collecting certifi (from pipenv)
    Downloading https://files.pythonhosted.org/packages/56/9d/1d02dd80bc4cd955f98980f28c5ee2200e1209292d5f9e9cc8d030d18655/certifi-2018.10.15-py2.py3-none-any.whl (146kB)
  Requirement already satisfied: setuptools>=36.2.1 in /usr/local/lib/python3.6/site-packages (from pipenv)
  Collecting virtualenv (from pipenv)
    Downloading https://files.pythonhosted.org/packages/b6/30/96a02b2287098b23b875bc8c2f58071c35d2efe84f747b64d523721dc2b5/virtualenv-16.0.0-py2.py3-none-any.whl (1.9MB)
  Collecting virtualenv-clone>=0.2.5 (from pipenv)
    Downloading https://files.pythonhosted.org/packages/16/9d/6419a4f0fe4350db7fdc01e9d22e949779b6f2d2650e4884aa8aededc5ae/virtualenv_clone-0.4.0-py2.py3-none-any.whl
  Requirement already satisfied: pip>=9.0.1 in /usr/local/lib/python3.6/site-packages (from pipenv)
  Installing collected packages: certifi, virtualenv, virtualenv-clone, pipenv
  Successfully installed certifi-2018.10.15 pipenv-2018.10.13 virtualenv-16.0.0 virtualenv-clone-0.4.0
  You are using pip version 9.0.1, however version 18.1 is available.
  You should consider upgrading via the 'pip install --upgrade pip' command.
  Installing dependencies from Pipfile.lock (20e54e)…
  Removing intermediate container 78c89f488e9d
  ---> d2a07b746e6a
  Step 6/6 : CMD [ "/bin/bash" ]
  ---> Running in e8e235efe37a
  Removing intermediate container e8e235efe37a
  ---> 2dc8cdd64ecb
  Successfully built 2dc8cdd64ecb

L'opération se termine correctement si ``Successfully built`` est affiché. La chaîne alphanumérique qui suit permet d'identifier l'image sans ambiguité.

Créer un conteneur
..................

A partir de cette image, on peut créer une instance (conteneur) dans lequel on va travailler (on remplacera ``<WORKDIR>`` par son propre répertoire de travail) : 

.. code-block:: bash

  > docker run -it --name conteneur_drio -v `pwd`:/home/dev/code/ -p 8888:8888 image_drio
  
  root@a74861d489f5:/home/dev/code# python
  Python 3.6.4 (default, Dec 21 2017, 01:35:12) 
  [GCC 4.9.2] on linux
  Type "help", "copyright", "credits" or "license" for more information.
  >>> 

Le prompt ``#`` est celui du conteneur dans lequel on est ``root``. On peut alors lancer les commandes incluses dans le conteneur(ici l'interpréteur Python). 
 
.. note::

  Il n'est pas rare de lancer plusieurs conteneurs instanciés à partir de la même image. Contrairement à une machine virtuelle, docker utilise la même base et les mêmes composants pour tous ces conteneurs et donc réduire l'impact mémoire de ces derniers.

Pour revenir un peu sur la commande ``docker run -it --name conteneur_drio -v `pwd`:/home/dev/code/ image_drio`` 

- docker run : permet de lancer un conteneur à partir d'une image (ici image_drio)
- -it permet de passer en mode intéractif, ie: le terminal du conteneur prend la main sur le terminal de votre machine
- --name conteneur_drio donne un petit nom au conteneur pour pouvoir le trouver plus facilement 
- -v `pwd`:/home/dev/code/ permet de faire mapping entre le dossier à l'intérieur du conteneur et le dossier de votre machine, ie: tous les modifications de fichier dans votre conteneur ou sur votre machine se répercuteront respectivement sur votre machine et dans votre conteneur.
- image_drio est le nom de l'image à utiliser pour créer votre conteneur
  
MongoDB
.......

Dans ce cours nous allons aussi utiliser MongoDB. Normalement il est installé par défaut sur toutes les machines. Si toutefois, il ne l'était pas ou si vous souhaitez travailler dans un autre environnment, il faut envisager de lancer un conteneur Mongo en parallèle.

.. code-block:: bash

  docker run --name mon-mongo -v <STOCKAGE_DIRECTORY>:/data/db -p 27017:27017 -d mongo

Un nouveau paramètre dans cette commande: 
- -p permet de mapper les ports du conteneur avec le port de la machine qui l'heberge. 

Docker par défault crée des machines complètement indépendantes et fermées. C'est pour cela qu'il faut lui spécifier explicitement quand on veut ouvrir un dossier ou un port. 

Redis
.....

.. code-block:: bash

  docker run -d --name redis -p 6379:6379 redis
  
  
ElasticSearch
.....

.. code-block:: bash

  docker run -d -p 9200:9200 -p 9300:9300 --name elastic -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.5.1


Docker Compose
..............

Pour faciliter les développments, un fichier docker-compose est disponible. Il permet d'instancier toutes les bases de données et l'image principale. 


Pour le lancer 

.. code-block:: bash

  docker-compose up -d

Vous voyez toutes les machines se lancer. Allez voir dans le fichier `docker-compose.yml` 
   
Consignes
---------
  
L'ensemble des exercices présents dans les différents cours doivent être complétés directement dans les notebooks et mis à jours sur vos comptes Github respectifs. 

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
