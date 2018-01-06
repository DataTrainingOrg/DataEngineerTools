=======
MongoDB
=======

Introduction
------------

MongoDB est une base de données opensource codée en C++ basée sur un concept de stockage sous la forme de document au format JSON.
Le grand avantage de ce système est l'optimisation de la mémoire. Dans une base SQL chaque colonne doit être définie au préalable avec une empreinte mémoire et un type de donnée.
Dans une base MongoDB si le champs n'est pas présent, il n'apparait pas dans un document alors qu'en SQL la place mémoire est utilisée pour spécifié que la valeur est nulle.

Les avantages
^^^^^^^^^^^^^
* Optimisé pour le multi machine et réplication de données.
* Pas besoin de jointures
* Un index est créé sur chaque clé pour une rapidité de requêtes
* Un langage de requêtage aussi puissant que le SQL
* Optimisation de la mémoire 

Concepts basiques
-----------------

* Database : une database est un regroupement de collections. Chaque Database possède sont propre système de fichiers et sa propre authentification. Elle a le même rôle qu'une database en MySQL.
* Collection : une collection est un regroupement de documents. C'est une table en MySQL, la principale différence est qu'elle ne définie pas un schéma de données fixe. Les documents présents dans une collection n'ont pas forcément tous les mêmes champs.
* Document : un document est un objet JSON stocké sous la forme de plusieurs clés:valeurs. C'est l'équivalent d'une ligne dans une table SQL.
* Champ : Un champ est l'équivalent d'une colonne en SQL. Il permet de faire des requêtes.

.. code-block:: json
    {
        _id: ObjectId(7df78ad8902c)
        title: 'Student', 
        name: 'Lodbrok',
        firstname: 'Ragnar',
        grades: [	
            {
                field:'DRIOA5001',
                message: 'Very good job',
                dateCreated: new Date(2011,1,10,8,15),
                grade: A
            },
            {
                field:'DRIOB5001',
                message: 'Some mistakes',
                dateCreated: new Date(2017,1,1,7,45),
                grade: C
            }
        ]
    }

Identifiants
^^^^^^^^^^^^
Tous les documents possèdent un identifiant unique qui permet de retrouver très efficacement un document.
L'identifiant peut être spécifié lors de l'ajout d'un nouveau document (nom+prenom, adresse email, url, etc).
Dans le cas ou aucun identifiant n'est précisé MongoDB se charge d'en ajouter un, il est composé d'un nombre de 12 bytes au format hexadécimal : 

* Les 4 premiers bytes sont le timestamp de l'ajout du document
* Les 3 suivants correspondent à l'identifiant de la machine
* Les 2 suivants l'identifiant du processus 
* Les 3 derniers sont une valeur incrémentale

Installation
------------

Création d'un modèle de données
-------------------------------

La création d'un modèle de données clair et adapté est une tâche importante et primordiale. 
Ce modèle de données doit être réfléchie à court et long terme et doit prendre en compte la capacité de stockage et les besoins métiers.




