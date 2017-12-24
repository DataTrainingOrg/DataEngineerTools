=======
MongoDB
=======

Introduction
------------

MongoDB est une base de données opensource codée en C++ basée sur un concept de stockage sous la forme de document au format JSON.
Le grand avantage de ce système est l'optimisation de la mémoire. Dans une base SQL chaque colonne doit être définie au préalable avec une empreinte mémoire et un type de donnée.
Dans une base MongoDB si le champs n'est pas présent, il n'apparait pas dans un document alors qu'en SQL la place mémoire est utilisée pour spécifié que la valeur est nulle.

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
        name: 'Dupont',
        firstname: 'Jean',
        grades: [	
            {
                user:'DRIOA5001',
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


