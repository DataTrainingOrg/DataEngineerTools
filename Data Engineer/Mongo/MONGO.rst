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

Les types de données
^^^^^^^^^^^^^^^^^^^^

Une base de données MongoDB permet de stocker un grand volume de données hétérogènes sans imposer un modèle de données fixe pour tous les documents. Il est conseillé comme vu plus haut de bien définir la structure globale pour garder une cohérence tout au long des développements.

- Integer : entier relatif stocker sur 32 ou 64 bits. 
- Double : nombre décimal 
- String : chaine de caractère (encodée en utf-8)
- Booléen : True ou False 
- Object : sous-objets stocké au format JSON 
- Date : date au format UNIX 
- Array : stocker une liste d'élément au format atomique ou d'objets 

D'autres types sont disponibles et vous pouvez les trouver  # TODO: Ajouter lien

Installation
------------

L'installation peut se faire de plusieurs manières.
- Directement depuis les sources et ppa. Liens vers le tutorial https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
- Ou en instanciant un conteneur Docker. L'avantage de Docker est qu'il n'installe aucune dépendance sur votre machine et laisse son environnement propre. Lien vers le tutorial : https://hub.docker.com/_/mongo/

Le port par défaut de mongo est le 27017.

Connexion
---------
Pour se connecter à une base mongo deux solutions sont possibles. En ligne de commande ou via un gestionnaire de BDD comme Robo3T https://robomongo.org/ . Dans les deux cas, la syntaxe mongo est utilisée pour effectuer des requêtes. L'avantage de Robo3T est qu'il possède une interface permettant de visualiser très simplement les données.

Création d'un modèle de données
-------------------------------

La création d'un modèle de données clair et adapté est une tâche importante et primordiale. 
Ce modèle de données doit être réfléchie à court et long terme et doit prendre en compte la capacité de stockage et les besoins métiers.


# MERGE HERE 

Database
^^^^^^^^

Après votre connexion vous (si vous en avez le droit) vous pouvez afficher toutes les databases disponibles sur la base. 

.. code-block:: bash

    show dbs
    
Pour supprimer définitivement une database: 

.. code-block:: bash

    db.dropDatabase()
    show dbs
    
Comme vous pouvez le deviner cette commande est à utiliser avec précautions.

Collections
^^^^^^^^^^^

Les colections correspondent aux tables en SQL. Elles sont des sous-ensembles de database. Pour créer une collection il faut auparavant s'être référencé sur une database.

.. code-block:: bash

    show dbs
    use <YOUR_DB_NAME>
    db.createCollection(<YOUR_COLLECTION_NAME>)
    show collections
    
Comme pour les databases on peut vouloir supprimer définitivement une collection.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.drop()
    show collections
    
 
Documents
^^^^^^^^^

Insertion
*********

Un document est un sous-ensemble d'une collection qui est elle même une sous-partie d'une database. Pour insérer un document il faut donc se référencer sur une database et sur la collection souhaitée.

.. code-block:: bash

    use <YOUR_DB_NAME>
    show collections
    db.<YOUR_COLLECTION_NAME>.insert({
        firstname : "Thomas",
        lastname : "Shelby",
        position : "director",
        company : "Peaky Blinders"})
        
Si vous ne précisez pas d'identifiant unique, MongoDB se charge de le remplir avec les règles définies précédement. Une bonne pratique est de trouver une règle permettant de retrouver facilement et efficacement un document sans avoir à faire une requête complexe et obliger la base à rechercher dans ses champs. Une technique est de prendre le hash d'une combinaison des champs qui permet de créer une clé unique SHA128(firstname+lastname+position) par exemple.

.. code-block:: bash

    use <YOUR_DB_NAME>
    show collections
    db.<YOUR_COLLECTION_NAME>.insert({
        _id: ObjectId(7df78ad8902c),
        firstname : "Thomas",
        lastname : "Shelby",
        position : "Directeur",
        gender : "Homme",
        age : 35,
        company : "Peaky Blinders"})
        
Pour des soucis de performances, si un grand nombre de document doivent être insérés très rapidement sans surcharger les appels réseaux il est possible de passer une liste d'objets à la fonction insert


.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.insert([
    {
        firstname : "Arthur",
        lastname : "Shelby",
        position : "Associé",
        gender : "Homme",
        age : 38,
        company : "Peaky Blinders",
        
    },{
        firstname : "John",
        lastname : "Shelby",
        position : "Associé",
        gender : "Homme",
        age : 30,
        company : "Peaky Blinders"
    },{
        firstname : "Ada",
        lastname : "Shelby",   
        gender : "Femme"
        age : 28,
        company : "Peaky Blinders"
    },{
        firstname : "Michael",
        lastname : "Gray",
        position : "Comptable",
        gender : "Homme",
        age : 21,
        company : "Peaky Blinders"
    },{
        firstname : "Polly",
        lastname : "Gray",
        gender : "Femme",
        age : 45,
        position : "Directrice Financière",
        company : "Peaky Blinders"
    })
        

Requêter
********
Afin de récupérer les documents stockés dans une collection, un set de fonctions de requêtes sont disponibles.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find()
    
Il est possible de récupérer qu'un seul élément.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.findOne()
    
Il est possible de faire des requêtes plus complexes. 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({"lastname":"Shelby"})
    
Les différentes opérations mathématiques sont implémentées. 

- Egalité :  {key:value}
- Différence :  {key: {$ne:value}}
- Plus (Grand|Petit) que :  les opérateurs sont $lt (lower than) ; $lte (lower than equals) ; $gt (greater than) ; $gte (greater than equals) : {key: {<OPERATEUR>:value}}

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({"age":{$gte :30}})

Les opérations logiques sont aussi disponibles.

OR $or et AND $and permettent de faire des requêtes complexes sur une collection. 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find($and:[{"age":{$gte: 28}}, "lastname":"Shelby", {"age":{$lt:40}}])
    
Pour des raisons de performances il peut être intéressant de limiter les accès réseaux. Pour cela, on peut sélectionner les champs devant être retournés. On peut aussi demander de limiter le nombre de documents.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find(QUERY, PROJECTION)
    
.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({"lastname":"Shelby"}, {"position":1})
    

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({"lastname":"Shelby"}).limit(3)
    
Il est aussi possible de passer directement au Nième document avec la fonction skip

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({"lastname":"Shelby"}).limit(3).skip(2)
    
On peut trier les résultats récupérés. 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({"lastname":"Shelby"}).sort({"age":-1})
    db.<YOUR_COLLECTION_NAME>.find({"lastname":"Shelby"}).sort({"age":1})


Indexation
**********

L'indexation permet d'accélérer les performances sur les requêtes. Si aucun n'index n'est mis en place, MongoDB doit effectuer un scan de tous les documents pour trouver ceux qui sont pertinents. L'index permet de stocker les valeurs d'un champs dans de façon triée pour limiter le nombre de document à parcourir pour effectuer une requête. 

# TODO : Récupérer la photo https://docs.mongodb.com/manual/indexes/

Indexation simple
'''''''''''''''''

L'indexation simple permet de créer l'index en fonction d'un seul champ. On spécifie alors l'ordre dans lequel l'index est créé et trié. 
Dans l'ordre croissant, 

.. code-block:: bash

     db.<YOUR_COLLECTION_NAME>.createIndex( { age: 1 } )

Dans l'ordre décroissant, 

.. code-block:: bash

     db.<YOUR_COLLECTION_NAME>.createIndex( { age: -1 } )


Indexation composée
'''''''''''''''''''

L'indexation composée permet de créé un index basé sur deux champs différents. L'ordre des champs spécifié dans la création d'un index est important.On peut trier dans l'ordre croissant le premier champs et dans l'ordre décroissant le deuxième champs. 


.. code-block:: bash

     db.<YOUR_COLLECTION_NAME>.createIndex( { age: -1, name : 1 } )





    
    
    




    

Mettre à jour
*************

Supprimer 
*********



    






