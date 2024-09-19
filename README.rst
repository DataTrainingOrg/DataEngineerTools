=============
Data Engineer
=============

Cours donné dans le cadre de l'unité Data Engineering de E4. Le but du cours est de maîtriser les bases de la Data
Engineering à travers un projet de récupération de données WEB, l'intégration dans un flux de stockage basé sur des
bases de données et leur exploitation sur l'interface d'une web app.

Github
------

Si vous ne disposez pas déjà d'un compte `Github <https://github.com>`_, il faut en créer un.

Forkez (avec le bouton ``Fork`` en haut à droite) ce projet. Il contient toutes les ressources nécessaires pour ce
cours. Vous pourrez ajouter des notes, modifier le code, et pousser votre projet final directement pour que l'on puisse
l'évaluer.

Pour commencer à travailler il vous faut cloner le projet dans votre répertoire (local) de travail : 

.. code-block:: bash

  $:~/> cd <WORKDIR>
  $:~/<WORKDIR> > git clone https://github.com/DataTrainingOrg/DataEngineerTools.git
  $:~/<WORKDIR> > cd DataEngineerTools/
  
Si au fil du temps j'ai besoin de modifier le contenu en temps réel vous pouvez garder votre projet à jour en ajoutant
ces quelques commandes :

.. code-block:: bash

  $:~/> cd <WORKDIR>
  $:~/<WORKDIR>cd DataEngineerTools/
  $:~/<WORKDIR>/DataEngineerTools> git remote add basestream https://github.com/DataTrainingOrg/DataEngineerTools
  $:~/<WORKDIR>/DataEngineerTools> git fetch basestream

Maintenant pour mettre à jour le projet :

.. code-block:: bash

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
