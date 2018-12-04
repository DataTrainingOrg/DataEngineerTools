=======
MongoDB
=======

Introduction
------------

MongoDB est une base de données open source (codée en C++) basée sur un concept de stockage sous la forme de documents au format JSON.
Le grand avantage de ce système est l'optimisation de la mémoire. Dans une base relationelle, chaque colonne doit être définie au préalable avec une empreinte mémoire et un type de donnée.
Dans une base MongoDB, si le champ n'est pas présent, il n'apparait pas dans un document et n'impacte pas la mémoire, alors qu'en SQL la place mémoire est utilisée même si le champ est absent, pour spécifier que la valeur est ``null``.

Les avantages
^^^^^^^^^^^^^
* Optimisé pour le multi-machines et la réplication de données ;
* Pas besoin de jointures entre les tables compte tenu du modèle de données sous forme de documents ;
* Un index est créé sur chaque clé pour une rapidité de requêtes ;
* Un langage de requêtage aussi puissant que le SQL ;
* Optimisation de la mémoire .

Concepts basiques
-----------------

* Database : une database est un regroupement de collections. Chaque database possède son propre système de fichiers et sa propre authentification. Elle a le même rôle qu'une database en MySQL.
* Collection : une collection est un regroupement de documents. C'est une table en MySQL, la principale différence étant qu'elle ne définit pas un schéma de données fixe. Les documents présents dans une collection n'ont pas forcément tous les mêmes champs.
* Document : un document est un objet JSON stocké sous la forme de plusieurs paires clé:valeur. C'est l'équivalent d'une ligne dans une table SQL.
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
Tous les documents possèdent un identifiant unique, ce qui permet de le retrouver très efficacement.
L'identifiant peut être spécifié lors de l'ajout d'un nouveau document (nom+prenom, adresse email, url, etc).
Dans le cas ou aucun identifiant n'est précisé, MongoDB se charge d'en ajouter un. Il est composé d'un nombre stocké sur 12 bytes au format hexadécimal : 

* Les 4 premiers bytes sont le timestamp de l'ajout du document
* Les 3 suivants correspondent à l'identifiant de la machine
* Les 2 suivants l'identifiant du processus 
* Les 3 derniers sont une valeur incrémentale

Les types de données
^^^^^^^^^^^^^^^^^^^^

Une base de données MongoDB permet de stocker un grand volume de données hétérogènes sans imposer un modèle de données fixe pour tous les documents. Il est conseillé, comme vu plus haut, de bien définir la structure globale pour garder une cohérence tout au long des développements.

- Integer : entier relatif stocké sur 32 ou 64 bits. 
- Double : nombre décimal stocké sur 64 bits.
- String : chaine de caractère (encodée en utf-8)
- Booléen : True ou False 
- Object : sous-objet stocké au format JSON 
- Date : date au format UNIX (nombre de ms écoulées depuis le 1er janvier 1970) stockée sur 64 bits.
- Array : stocker une liste d'éléments au format atomique ou d'objets 

D'autres types sont disponibles et vous pouvez les trouver  # TODO: Ajouter lien (https://docs.mongodb.com/manual/reference/bson-types/)

Installation
------------

L'installation peut se faire de plusieurs manières.

- Directement depuis les sources ou à partir de packages. Liens vers le tutorial https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

Sur une Debian 9 Stretch:

.. code-block:: bash

    # export http_proxy=http://147.215.1.189:3128
    # export https_proxy=http://147.215.1.189:3128
    # apt-get update
    # apt-get install -y mongodb-org

- Ou en instanciant un conteneur Docker. L'avantage de Docker est qu'il n'installe aucune dépendance sur votre machine et laisse son environnement propre. Lien vers le tutorial : https://hub.docker.com/_/mongo/

Démarrage du service
^^^^^^^^^^^^^^^^^^^^

Vérifier que le service Mongo est démarré

.. code-block:: bash

    # service mongodb status
    ● mongodb.service - An object/document-oriented database
       Loaded: loaded (/lib/systemd/system/mongodb.service; enabled; vendor preset: 
       Active: active (running) since Mon 2018-02-05 13:51:14 CET; 18min ago
         Docs: man:mongod(1)
     Main PID: 22845 (mongod)
        Tasks: 16 (limit: 4915)
       CGroup: /system.slice/mongodb.service
               └─22845 /usr/bin/mongod --unixSocketPrefix=/run/mongodb --config /etc

    févr. 05 13:51:14 debian systemd[1]: Started An object/document-oriented databas

Sinon, le démarrer avec

.. code-block:: bash

    # service mongodb start


Connexion
---------
Pour se connecter à une base Mongo, deux solutions sont possibles. En ligne de commande ou via un gestionnaire de BDD comme Robo3T https://robomongo.org/ . Dans les deux cas, la syntaxe Mongo est utilisée pour effectuer des requêtes. L'avantage de Robo3T est qu'il possède une interface permettant de visualiser très simplement les données.

Dans un terminal utilisateur standard, la commande ``mongo`` permet d'obtenir un shell interactif:

.. code-block:: bash

    student@debian:~$ mongo
    MongoDB shell version: 3.2.11
    connecting to: test
    > 

Le port par défaut de Mongo est le 27017.

Création d'un modèle de données
-------------------------------

La création d'un modèle de données clair et adapté est une tâche importante et primordiale. 
Ce modèle de données doit être réfléchi à court et long terme, et doit prendre en compte la capacité de stockage et les besoins métiers.


Database
^^^^^^^^

A partir du shell Mongo, on peut afficher les databases disponibles. Au démarrage, aucune n'est créée:

.. code-block:: bash

    > show dbs
    local  0.000GB
    
.. code-block:: bash

    use test
    show dbs
    
Pour supprimer définitivement une database: 

.. code-block:: bash

    db.dropDatabase()
    show dbs
    
Comme vous pouvez le deviner cette commande est à utiliser avec précaution.

Collections
^^^^^^^^^^^

Les collections correspondent aux tables en SQL. Elles sont des sous-ensembles d'une database. Pour créer une collection il faut auparavant s'être référencé sur une database.

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

Un document (objet JSON) est un sous-ensemble d'une collection qui est lui même une sous-partie d'une database. Pour insérer un document il faut donc se référencer sur une database et sur la collection souhaitée.

.. code-block:: bash

    use <YOUR_DB_NAME>
    db.createCollection(<YOUR_COLLECTION_NAME>)
    show collections
    db.<YOUR_COLLECTION_NAME>.insert({
        firstname : "Thomas",
        lastname : "Shelby",
        position : "director",
        company : "Peaky Blinders"})
        
Si vous ne précisez pas d'identifiant unique (id du document), MongoDB se charge de le remplir avec les règles définies précédement. Une bonne pratique est de trouver une règle permettant de retrouver facilement et efficacement un document sans avoir à faire une requête complexe et obliger la base à rechercher dans ses champs. Une technique est de prendre le hash d'une combinaison des champs qui permet de créer une clé unique SHA128(firstname+lastname+position) par exemple.

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
        
Pour des soucis de performances, si un grand nombre de documents doivent être insérés très rapidement sans surcharger les appels réseaux, il est possible de passer une liste JSON d'objets à la fonction insert.


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
Afin de récupérer les documents stockés dans une collection, des fonctions de requête sont disponibles. La fonction find() permet de récupérer les N premiers documents. Toutes les fonctions de récupérations peuvent être suivie de pretty() qui permet d'afficher plus proprement les résultats.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find().pretty()
    
Il est possible de ne récupérer qu'un seul élément. Si aucun argument n'est précisé, il récupère le premier document.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.findOne()
    
Il est possible de passer des arguments à la fonction find() ou findOne().
    
.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({"lastname":"Shelby"}).pretty()
    
Les différentes opérations mathématiques sont implémentées. 

- Egalité :  `{key:value}` Correspondance clé valeur entre le champ et la requête. 
- Différence :  `{key: {$ne:value}}`
- Plus (Grand|Petit) que :  les opérateurs sont `$lt` (lower than) ; `$lte` (lower than equals) ; `$gt` (greater than) ; `$gte` (greater than equals) : `{key: {<OPERATEUR>:value}}`.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({"age":{$gte :30}})

Les opérations logiques sont aussi disponibles.

OR `$or` et AND `$and` permettent de faire des requêtes complexes sur une collection. 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({$and:[{"age":{$gte: 28, $lt:40}}, {"lastname":"Shelby"}]})
    

Requêtes complexes
''''''''''''''''''

Les objets Mongo peuvent être assez complexes et les requêtes doivent pouvoir matcher tous types de documents:

- Les requêtes sur les sous-objets:

Pour faire une requête sur un objet complet, il faut redéfinir l'objet dans son intégralité.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find( { size: { h: 14, w: 21, uom: "cm" } } ) #TODO: Dot it
    
Pour faire une requête sur uniquement un champ de l'objet  :

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find( { "size.uom": "in" } ) #TODO : Do it 
    
Pour requêter les valeurs d'une liste : 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find( { nicknames:  ["Henry Johnson", "Jobbie Muncher", "Mickey"] } )

Le champ `nicknames` doit matcher exactement la liste donnée en argument (en contenu et en ordre). 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find( { nicknames:  ["Henry Johnson",  "Mickey", "Jobbie Muncher"] } )
    
Si maintenant on veut récupérer tous les documents avec "Mickey" et "Jobbie Muncher", peu importe l'ordre d'apparition et peu importe les autres éléments du tableau.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find( { nicknames:  {$all :["Mickey", "Jobbie Muncher"] } } )
    
On peut vouloir maintenant récupérer tous les documents comptenant "Mickey" dans les nicknames (listes). 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find( { nicknames: "Mickey" } )
    
Comme on vient de le voir, une requête sur le champ d'une liste se construit de la même manière qu'une requête sur un champ 'basique'.

La syntaxe générique d'une requête Mongo est la suivante.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find( { <array field>: { <operator1>: <value1>, ... } })

Limitation, Projection et Tris
''''''''''''''''''''''''''''''

Pour des raisons de performances, il peut être intéressant de limiter les accès réseaux. Pour cela, on peut sélectionner les champs devant être retournés (Projection). On peut aussi demander de limiter le nombre de documents (Limitation).

La syntaxe est la suivante : 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find(QUERY, PROJECTION).LIMIT(N_DOCUMENTS)

Un exemple de projection en utilisant les requêtes déjà utilisées plus haut.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({"lastname":"Shelby"}, {"position":1})
    
Avec une requête plus complexe et une autre projection.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({$and:[{"age":{$gte: 28, $lt:40}}, {"lastname":"Shelby"}]}, {"firstname":1})
    
Un exemple de limitation : 
    
.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({"lastname":"Shelby"}).limit(2)
    
Il est aussi possible de passer directement au Nième document avec la fonction `skip()`.

.. code-block:: bash

    db.<YOUR_COLLECTION- _NAME>.find({"lastname":"Shelby"}).skip(2)
    
On peut trier les résultats récupérés. 

Pour trier dans l'ordre ascendant :

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({"lastname":"Shelby"}, {"firstname":1}).sort({"age":1})
   
Pour trier dans l'ordre descendant :

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({}, {"firstname":1}).sort({"age":-1})
    
On peut aussi trier selon une clé puis une autre.


.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find({}, {"firstname":1}).sort({"age":-1}, {"firstname":1})


Indexation
**********

L'indexation permet d'accélérer les performances sur les requêtes. Si aucun index n'est mis en place, MongoDB doit effectuer un scan de tous les documents pour trouver ceux qui sont pertinents. L'index permet de stocker les valeurs d'un champ de façon triée pour limiter le nombre de document à parcourir pour effectuer une requête. 

# TODO : Récupérer la photo https://docs.mongodb.com/manual/indexes/

Indexation simple
'''''''''''''''''

L'indexation simple permet de créer l'index en fonction d'un seul champ. On spécifie alors l'ordre dans lequel l'index est créé et trié. 
Dans l'ordre croissant, 

.. code-block:: bash

     db.<YOUR_COLLECTION_NAME>.createIndex( { age: 1 } )
     db.<YOUR_COLLECTION_NAME>.getIndexes()
     
     
 #TODO: Ajouter le résultat.

Dans l'ordre décroissant, 

.. code-block:: bash

     db.<YOUR_COLLECTION_NAME>.createIndex( { age: -1 } )
     db.<YOUR_COLLECTION_NAME>.getIndexes()
     
Pour supprimer tous les index : 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.dropIndexes()
    db.<YOUR_COLLECTION_NAME>.getIndexes()
    
    
# TODO : ajouter exemple avec/sans index
    
Les performances ne sont visibles que pour des collections de taille importante.
    

Indexation composée
'''''''''''''''''''

L'indexation composée permet de créer un index basé sur deux champs différents. L'ordre des champs spécifié dans la création d'un index est important.On peut trier dans l'ordre croissant le premier champ et dans l'ordre décroissant le deuxième champ. 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.createIndex( { age: -1, firstname : 1 } )
    db.<YOUR_COLLECTION_NAME>.getIndexes()
    
# TODO : ajouter le résultat

Indexations spéciales
'''''''''''''''''''''

Mongo permet plusieurs indexations : 

- Text : permet de faire de la recherche naturelle de *queries* dans du texte. Cet index peut devenir très rapidement très important et prendre beaucoup de place mémoire. Cet index textuel contient un index par mot contenu dans l'ensemble des documents. Il peut aussi être très lent à créer.
- Multiclés : permet de créer un index sur les éléments d'objets stockés dans des listes ou *arrays*.
- 2D, 2DSphere, geoHaystack : permet de créer des index sur des données géospatiales.
- Hash : permet de stocker les valeurs des champs sous forme de *hash*.

Dans ce cours, on se contentera de faire de l'indexation textuelle.

Tous ces mécanismes d'indexation permettent d'accélérer les performances des requêtes. Mais ils peuvent avoir des effets négatifs: 

- Sur l'occupation mémoire : Chaque index doit avoir un minimum de 8 kB et peut prendre beaucoup de place sur le disque et dans la mémoire RAM.
- Sur le temps d'exécution : les opérations d'insertion et d'écriture peuvent être longues puisque Mongo doit insérer chaque nouveau document dans l'index en plus de l'insertion dans la collection.

Exemple : 

Pour créer un index textuel sur la description des personnages : 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.createIndex( { description: "text" } )
    db.<YOUR_COLLECTION_NAME>.getIndexes()
    
Uniquement après que cet index de texte ait été créé, on peut utiliser la méthode `find()` avec l'argument `$text` pour faire une requête dans le texte.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.find( { $text: { $search: "female" } } ).pretty()
    
    
Exercice : 

Supprimez tous les index créés et réessayez de faire la même requête. Que se passe-t-il ?


Mettre à jour
*************
La mise à jour des documents et une opération très courante dans les bases de données. MongoDB implémente trois fonctions différentes permettant de mettre à jour un ou plusieurs documents à la fois.

- Mettre à jour un seul document : 

.. code-block:: bash

     db.<YOUR_COLLECTION_NAME>.updateOne(<filter>, <update>, <options>)

- Le champ `filter` est une requête comme on vient de voir précédemment ; 
- Le champ `update` permet de préciser la requête de mise à jour ;
- Le champ `option` permet de donner des arguments à cette opération.

 Cette fonction va mettre à jour le premier élément renvoyé par la requête `filter`. 
 
 Par exemple : 
 
.. code-block:: bash
    
    db.<YOUR_COLLECTION_NAME>.updateOne({"firstname":"Thomas"}, {$set:{maincharacter:true}})
    db.<YOUR_COLLECTION_NAME>.findOne({"firstname":"Thomas"})
    
 Ici le champ update utilise le selecteur `$set` qui permet de définir les couples clé:valeurs à mettre à jour.

- Mettre à jour une liste de documents : 

.. code-block:: bash

     db.<YOUR_COLLECTION_NAME>.updateMany(<filter>, <update>, <options>)
     
Cette fonction va mettre à jour tous les documents concernés par la requête `filter`.
Dans l'exemple ci-dessous nous allons mettre à jour tous les éléments correspondant à la family Shelby.

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.updateMany({"lastname":"Shelby"}, {$set:{shelbyFamily:true}})
    db.<YOUR_COLLECTION_NAME>.find({"lastname":"Shelby"}).pretty()

- Remplacer un document : 

.. code-block:: bash

     db.<YOUR_COLLECTION_NAME>.replaceOne(<filter>, <update>, <options>)
     
 
L'option `upsert` peut être très intéressante. Elle permet d'ajouter un document si il n'existe pas déjà directement depuis la fonction `update()`. Par défaut, cette option est `false`. 
 
 
.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.update(<filter>, <update>, {upsert: true})
    
    
# TODO: Exercice 


Supprimer 
*********

Pour supprimer des documents, comme pour la mise à jour, il existe deux méthodes : 

- `deleteMany({ <field1>: <value1>, ... }`
- `deleteOne({ <field1>: <value1>, ... }`

Pour supprimer tous les documents de la collection: 
 
.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.deleteMany({})
    
Pour supprimer tous les documents possédant une condition : 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.deleteMany({lastname: "Gray"})
    
Pour supprimer un seul document (ou le premier si la condition n'est pas assez restrictive) :

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.deleteOne({firstname: "Arthur"})

Quelques choses à savoir : 

- La méthode `deleteMany()` applique une fonction à tous les documents. Toutes les fonctions en Mongo sont atomiques ce qui veut dire qu'elles s'appliquent à chaque document indépendamment les uns des autres.
- La méthode `delete()` ne supprime pas les index, même si on supprime tous les documents de la collection.


Aggregation
***********

Une aggrégation permet de faire des opérations complexes sur des groupes de documents directement dans la base. Elle se charge de grouper les documents entre eux suivant la requête et se charge d'effectuer une opération sur l'ensemble des documents de chacun des groupes. On peut retrouver les mêmes opérations en SQL avec les arguments `GROUP BY`.

La syntaxe est très similaire à toutes les autres fonctions Mongo mais la requête va être plus complexe. 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.aggregate(AGGREGATE_OPERATION)
    
On peut vouloir récupérer le nombre de personnages de chaque famille présente dans la série : 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.aggregate([{$group : {_id : "$lastname", charactereNumberByFamily : {$sum : 1}}}])
    
Vous avez accès à toutes les opérations mathématiques dont vous avez besoin : 

- `$sum` : fait la somme de 
- `$avg` : fait la moyenne 
- `$min` : récupère la valeur minimale 
- `$max` : récupère la valeur maximale 
- `$first` : récupère le premier élément
- `$last` : récupère le dernier élément

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.aggregate([{$group : {_id : "$lastname", averageAgeByFamily : {$avg : "$age"}}}])
    db.<YOUR_COLLECTION_NAME>.aggregate([{$group : {_id : "$lastname", minAgeByFamily : {$min : "$age"}}}])
    db.<YOUR_COLLECTION_NAME>.aggregate([{$group : {_id : "$lastname", lastAgeByFamily : {$last : "$age"}}}])
    
On peut ajouter un paramètre à la fonction `aggregate()` pour filtrer les élements à aggréger.
Si on ne veut récupérer que les hommes : 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.aggregate([
        {$match:{gender:"Male"}},
        {$group : {_id : "$lastname", averageAgeByFamily : {$avg : "$age"}}}
    ])
       
Il est aussi possible d'intégrer directement du code JavaScript dans les requêtes Mongo. Des fonctions de Map->Reduce sont disponibles pour effectuer les fonctions d'aggrégation. L'opération de Map->Reduce se découpe en deux phases : 

- Phase de MAP : parcourt tous les élements et extrait les champs voulus.
- Phase de REDUCE : utilise les champs retournés pour effectuer l'opération finale. 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.mapReduce(
        function(){emit(this.lastname, this.age)},
        function(key,values){return Array.sum(values)},
        {query :{gender:"Male"}, out:"sumAge"}
        )
        
On voit le nombre de d'entrées pour le MAP et le résultat du REDUCE.
Maintenant pour récupérer les résultats du Map->Reduce : 

.. code-block:: bash

    db.<YOUR_COLLECTION_NAME>.mapReduce(
        function(){emit(this.lastname, this.age)},
        function(key,values){return Array.sum(values)},
        {query :{gender:"Male"}, out:"sumAge"}
        )


# Suite

Ouvrez un navigateur et allez à l'adresse http://localhost:8888

Allez voir le notebook `Tutoriel.ipynb`. Quand vous avez terminé vous pouvez passer aux exercices `ExerciceYoutube.ipynb` & `ExerciceKickStarter.ipynb`
