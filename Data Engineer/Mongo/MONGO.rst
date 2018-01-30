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
        firstname : "Thomas",
        lastname : "Shelby",
        position : "CEO",
        gender : "Male",
        age : 35,
        description : "Thomas 'Tommy' Michael Shelby M.P. OBE, is the leader of the Birmingham criminal gang Peaky Blinders and the patriarch of the Shelby Family. His experiences during and after the First World War have left him disillusioned and determined to move his family up in the world.",
        nicknames : ["Tom", "Tommy", "Thomas"],
        company : "Peaky Blinders",
        episodes : [1,2,4,5,6]
        })
        
Pour des soucis de performances, si un grand nombre de document doivent être insérés très rapidement sans surcharger les appels réseaux il est possible de passer une liste d'objets à la fonction insert


.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.insert([
    {
        firstname : "Arthur",
        lastname : "Shelby",
        position : "Associate",
        gender : "Male",
        age : 38,
        description : "Arthur Shelby Jr. is the eldest of the Shelby siblings and the tough member of Peaky Blinders, the Deputy Vice President Shelby Company Limited. He's also a member of the ICA.",
        company : "Peaky Blinders",
        episodes : [1,4,6]
        
    },{
        firstname : "John",
        lastname : "Shelby",
        position : "Associate",
        gender : "Male",
        age : 30,
        description : "John Michael Shelby, also called Johnny or John Boy, was the third of Shelby siblings and a member of the Peaky Blinders.",
        nicknames : ["Johnny", "John Boy"],
        company : "Peaky Blinders",
        episodes : [4,5,6]
    },{
        firstname : "Ada",
        lastname : "Thorne",   
        position : "HR",
        gender : "Female",
        age : 28,
        description : "Ada Thorne is the fourth and only female of the Shelby sibling. She's the Head of Acquisitions of the Shelby Company Limited.",
        nicknames : ["Ada Shelby"],
        company : "Peaky Blinders",
        episodes : [1,2,6]
    },{
        firstname : "Michael",
        lastname : "Gray",
        position : "Accounting",
        gender : "Male",
        age : 21,
        description : "Michael Gray is the son of Polly Shelby, his father is dead, and cousin of the Shelby siblings. He is the Chief Accountant in the Shelby Company Limited.",
        nicknames : ["Henry Johnson", "Jobbie Muncher", "Mickey"],
        company : "Peaky Blinders",
        episodes : [5,6]
    },{
        firstname : "Polly",
        lastname : "Gray",
        gender : "Female",
        age : 45,
        position : "CFO",
        description : "Elizabeth Polly Gray (née Shelby) is the matriarch of the Shelby Family, aunt of the Shelby siblings, the treasurer of the Birmingham criminal gang, the Peaky Blinders, a certified accountant and company treasurer of Shelby Company Limited. ",
        nicknames : ["Aunt Polly", "Polly Gray", "Elizabeth Gray", "Polly Shelby", "Pol"],
        company : "Peaky Blinders",
        episodes : [1,2,5,6]
    }])
        

Requêter
********
Afin de récupérer les documents stockés dans une collection, un set de fonctions de requêtes sont disponibles.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find().pretty()
    
Il est possible de récupérer qu'un seul élément.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.findOne()
    
Il est possible de faire des requêtes plus complexes. - 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({"lastname":"Shelby"}).pretty()
    
Les différentes opérations mathématiques sont implémentées. 

- Egalité :  {key:value}
- Différence :  {key: {$ne:value}}
- Plus (Grand|Petit) que :  les opérateurs sont $lt (lower than) ; $lte (lower than equals) ; $gt (greater than) ; $gte (greater than equals) : {key: {<OPERATEUR>:value}}

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({"age":{$gte :30}})

Les opérations logiques sont aussi disponibles.

OR $or et AND $and permettent de faire des requêtes complexes sur une collection. 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({$and:[{"age":{$gte: 28, $lt:40}}, {"lastname":"Shelby"}]})
    
Pour des raisons de performances il peut être intéressant de limiter les accès réseaux. Pour cela, on peut sélectionner les champs devant être retournés. On peut aussi demander de limiter le nombre de documents.

Requêtes complexes
''''''''''''''''''

Les objets Mongo peuvent être assez complexes et les requêtes doivent pouvoir matcher des documents:

- Les requêtes sur les sous-objets:

Pour faire une requêtes sur un objet complet il faut redéfinir l'objet.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find( { size: { h: 14, w: 21, uom: "cm" } } ) #TODO: Dot it
    
Pour faire une requête sur uniquement un champs de l'objet  :

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find( { "size.uom": "in" } ) #TODO : Do it 
    
Pour requêter les valeurs d'une liste : 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find( { nicknames:  ["Henry Johnson", "Jobbie Muncher", "Mickey"] } )

Le champ nicknames doit matcher parfaitement la liste donnée en argument en contenu et en ordre. Si maintenant on veut récupérer tous les documents avec "Mickey" et "Jobbie Muncher", peu importe l'ordre d'apparition et peu importe les autres éléments du tableau.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find( { nicknames:  {$all :["Mickey", "Jobbie Muncher"] } } )
    
On peut vouloir maintenant vouloir récupérer tous les éléments comptenant "Mickey" dans les surnoms.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find( { nicknames: "Mickey" } )
    - 
En général, une requête sur un champ d'un tableau se construit de la même manière qu'une requête sur un champ 'basique'


.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find( { <array field>: { <operator1>: <value1>, ... } })





Limitation, Projection et Tris
''''''''''''''''''''''''''''''

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find(QUERY, PROJECTION)
    
.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({"lastname":"Shelby"}, {"position":1})
    

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({"lastname":"Shelby"}).limit(2)
    
Il est aussi possible de passer directement au Nième document avec la fonction skip

.. code-block:: bash

    db.<YOUR_COLLECTION- _NAME>.find({"lastname":"Shelby"}).skip(2)
    
On peut trier les résultats récupérés. 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({"lastname":"Shelby"}, {"firstname":1}).sort({"age":-1})
    db.<YOUR_COLLECTION_NAME>.find({}, {"firstname":1}).sort({"age":1})


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
     db.<YOUR_COLLECTION_NAME>.getIndexes()

Dans l'ordre décroissant, 

.. code-block:: bash

     db.<YOUR_COLLECTION_NAME>.createIndex( { age: -1 } )
     db.<YOUR_COLLECTION_NAME>.getIndexes()
     
Pour supprimer tous les index : 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.dropIndexes()
    db.<YOUR_COLLECTION_NAME>.getIndexes()
    

Indexation composée
'''''''''''''''''''

L'indexation composée permet de créé un index basé sur deux champs différents. L'ordre des champs spécifié dans la création d'un index est important.On peut trier dans l'ordre croissant le premier champs et dans l'ordre décroissant le deuxième champs. 


.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.createIndex( { age: -1, firstname : 1 } )
    db.<YOUR_COLLECTION_NAME>.getIndexes()

Indexation spéciales
''''''''''''''''''''

- Text : permet de faire de la recherche naturelle de queries dans du texte. Cette index peut devenir très rapidement très important et prendre beaucoup de place mémoire. Il contient un index par mot contenu dans l'ensemble des documents. Il peut aussi être très lent à créer.
- Multiclés : permet de créer un index sur les éléments d'objets stockés dans des listes ou arrays.
- 2D, 2DSphère, geoHaystack : permet de créer des index sur des données géospaciales.
- Hash : permet de stocker les valeurs des champs sous forme de hash.

Tous ces mécanismes d'indexation permettent d'accélérer les performances de requêtes. Mais ils peuvent avoir des effets négatifs: 

- Chaque index doit avoir un minimum de 8kB et peut prendre beaucoup de place sur le disque et dans la mémoire RAM.
- Ils sont gourmands pour insertions pour les opérations d'écriture puisqu'il doit insérer le nouveau document dans l'index en plus de l'insertion du document dans la collection.

Exemple : 

Pour créer un index sur le texte de la description des personnages : 


.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.createIndex( { description: "text" } )
    db.<YOUR_COLLECTION_NAME>.getIndexes()
    
Uniquement après que cet index de texte ait été créé on peut utiliser la méthode find avec l'argument $text pour faire une requête dans le texte.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find( { $text: { $search: "female" } } ).pretty()
    
    
Exercice : 

Supprimez tous les index créé et réessayez de faire la recherche. 


Mettre à jour
*************
La mise à jour des documents et une opération très courante dans les bases de données. MongoDB implémente trois fonction différentes permettant de mettre à jour un ou plusieurs documents à la fois.


- Mettre à jour un seul document : 

.. code-block:: bash

     db.<YOUR_COLLECTION_NAME>.updateOne(<filter>, <update>, <options>)
     
 Cette fonction va mettre à jour le premier élément renvoyer par la requête du filtre. 
 
.. code-block:: bash
    
    db.<YOUR_COLLECTION_NAME>.updateOne({"firstname":"Thomas"}, {$set:{maincharacter:true}})
    db.<YOUR_COLLECTION_NAME>.findOne({"firstname":"Thomas"})

- Mettre à jour une liste de documents : 

.. code-block:: bash

     db.<YOUR_COLLECTION_NAME>.updateMany(<filter>, <update>, <options>)
     
Cette fonction va mettre à jour tous les documents concernée par la requête.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.updateMany({"lastname":"Shelby"}, {$set:{shelbyFamily:true}})
    db.<YOUR_COLLECTION_NAME>.find({"lastname":"Shelby"}).pretty()

- Remplacer un document : 

.. code-block:: bash

     db.<YOUR_COLLECTION_NAME>.replaceOne(<filter>, <update>, <options>)
     
 
 Une  option peut être très intéressante, c'est l'option upsert. Elle permet d'ajouter un document si il n'existe pas déjà directement depuis la fonction update. Par défaut, cette option est à False. 
 
 
.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.update(<filter>, <update>, {upsert: true})
    
    
# TODO: Exercice 


Supprimer 
*********

Pour supprimer des documents, il existe deux méthodes : 

- deleteMany({ <field1>: <value1>, ... }
- deleteOne({ <field1>: <value1>, ... }


Pour supprimer tous les documents de la collection: 
 
.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.deleteMany({})
    
Pour supprimer tous les documents possédant une condition : 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.deleteMany({lastname: "Gray"})
    
Pour supprimer un seul document (ou le premier si la condition n'est pas assez restrictive. 


.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.deleteOne({firstname: "Arthur"})

Quelques choses à savoir : 

La méthode deleteMany applique une fonction à tous les documents. La fonction n'est pas une fonction globale. Toutes les fonctions en mongo sont atomique ce qui veut dire qu'elles s'appliquent à chaque document indépendament les uns des autres.
La méthode delete ne supprime pas les indexes, même si on supprimer tous les documents de la collection


Aggreagation
************

Les aggrégations permettent de faire des opérations complexes sur des groupes de documents directement dans la base. Elle se charge de grouper les documents entre eux suivant la requête et se charge d'effectuer une opération sur l'ensemble des documents de chacun des groupes. On peut retrouver les mêmes opérations en SQL avec les arguments GROUP BY.

La syntaxe est très similaire à toutes les autres fonctions Mongo mais la requête va être plus complexe. 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.aggregate(AGGREGATE_OPERATION)
    
On peut vouloir récupérer le nombre de personnage de chaque famille présente dans la série : 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.aggregate([{$group : {_id : "$lastname", charactereNumberByFamily : {$sum : 1}}}])
    
Vous avez accès à toutes les opérations mathématiques dont vous avez besoin : 

- $sum : fait la somme de 
- $avg : fait la moyenne 
- $min : récupère la valeur minimale 
- $max : récupère la valeur maximal 
- $first : récupère le premier élément
- $last : récupère le denier élément


.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.aggregate([{$group : {_id : "$lastname", averageAgeByFamily : {$avg : "$age"}}}])
    db.<YOUR_COLLECTION_NAME>.aggregate([{$group : {_id : "$lastname", minAgeByFamily : {$min : "$age"}}}])
    db.<YOUR_COLLECTION_NAME>.aggregate([{$group : {_id : "$lastname", lastAgeByFamily : {$last : "$age"}}}])
    
On peut ajouter un paramètre à la fonction aggregate pour filtrer les élements à aggréger.
Si on veut récupérer que les hommes : 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.aggregate([
        {$match:{gender:"Male"}},
        {$group : {_id : "$lastname", averageAgeByFamily : {$avg : "$age"}}}
    ])
    
    
Il est aussi possible d'intégrer directement du code JavaScript dans les requêtes Mongo. Des fonctions de Map->Reduce sont disponibles pour effectuer les fonctions d'aggrégations. Cette phase de Map Reduce se découpe en deux phases : 

- Phase de MAP : Il parcourt tous les élements et extrait les champs voulus.
- Phase de REDUCE : qui utilise les champs retournés pour effectuer l'opération finale. 


.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.mapReduce(
        function(){emit(this.lastname, this.age)},
        function(key,values){return Array.sum(values)},
        {query :{gender:"Male"}, out:"sumAge"}
        )
 
On voit le nombre de d'entrées pour le MAP et le résultas du REDUCE.
Maintenant pour récupérer les résultats du map->reduce : 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.mapReduce(
        function(){emit(this.lastname, this.age)},
        function(key,values){return Array.sum(values)},
        {query :{gender:"Male"}, out:"sumAge"}
        )
        
        
API Python
----------

Il existe une API Python développée pour intéragir avec une base de données MongoDB. Ce package s'appelle pymongo  https://docs.mongodb.com/getting-started/python/client/. Il est important d'avoir des APIs dans les différents langages pour faciliter l'intégration dans des applications. 

Pour installer le package : 

.. code-block:: Python

    pip install pymongo
    
Ce package garde très largement la syntaxe mongo shell et permet d'utiliser ces méthodes et items (DataBases, Collections, Documents) en tant qu'objets Python. 


.. code-block:: Python

    client = MongoClient()
    
Permet de se connecter à une base MongoDB en créant un pointeur client vers cette base. Par défault ce client est paramétré sur le localhost. 

.. code-block:: Python

    client = MongoClient("http://<YOUR_IP_ADDRESS>:<YOUR_PORT_NUMBER>)
    
Dans la plupart des cas, le port par défaut est le 27017.
Il est possible comme depuis le MongoShell de lister les bases de données. 

.. code-block:: Python

    client.database_names()
    
Et de les sélectionner : 

.. code-block:: Python

    db = client.<YOUR_DATABASE_NAME>
    db = client["<YOUR_DATABASE_NAME>"]
    
Pour lister les différentes collections présentes sur une database.

.. code-block:: Python

    db.collection_names()

Il en va de même pour sélectionner une collection : 

.. code-block:: Python

    collection = db.<YOUR_COLLECTION_NAME> or db_pkb["<YOUR_COLLECTION_NAME>"]
    
Pour récupérer un document : 

.. code-block:: Python 

    collection.find_one()
    
C'est un peu différent pour la méthode find(). Cela créé, pour des raison de performances un curseur PyMongo. En effet, les données seront récupérées uniquement si elles sont utilisées. C'est intéressant pour des collections très volumineuses.

.. code-block:: Python 

    cursor = collection.find()
    type(cursor)

.. code-block:: Python 
    
    cursor.next()
    
.. code-block:: Python 
    
    for document in cursor : 
        print(document)
        
    
    
Exercice : 

Ouvrir le fichier `ks-projects-201801.csv`, il recense environ 400 000 projets KickStarter. Intégrer les données directement avec L'API Python dans une base de données Mongo. Il conviendra de bien spécifier l'ID du document. Pensez aussi à bien formatter le type des données pour profiter des méthodes implémentées par Mongo. L'ensemble de données n'est pas forcément nécessaire, c'est à vous de créer votre modèle de données.   

- Récupérer les 5 projets ayant reçu le plus de promesse de dons.
- Compter le nombre de projets ayant atteint leur but.
- Compter le nombre de projets pour chaque catégories.
- Compter le nombre de projets francais ayant été instancié avant 2016.
- Récupérer les projets américains ayant demandé plus de 200 000 dollars.
- Compter le nombre de projet ayant "Sport" dans elru nom


Intégrer le fichier `USvideos.csv`. Qui représente un ensemble de 8000 vidéos Youtube. Merger le fichier `US_category_id.json` pour récupérer le nom des catégories. Il conviendra de bien spécifier l'ID du document.

- Récupérer toutes les vidéos de la chaîne Apple.
- Compter le nombre de catégories différentes 
- Si vous ne l'avais pas déjà fait, découper les tags en listes et mettre à jour les tags de chacun des documents avec une requête update. 
- Récupérer les vidéos les plus vues.
- Compter le nombre de vue moyen en fonction de la catégorie. 
- Récupérer les chaines Youtube avec la plus grande moyenne de likes.
