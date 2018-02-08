Votre premier projet
====================

Dans un premier temps vous devez créer votre projet. Scrapy le fait pour vous et créer un template de projet que vous aurez à remplir pour remplir vos besoins. 

.. code-block:: bash

    scrapy startproject monprojet
    
Cette commande va créer un dossier `monprojet` contenant les éléments suivants::

    monprojet/
        scrapy.cfg            # Options de déploiement

        monprojet/             # Le module Python contenant les informations
            __init__.py

            items.py          # Fichier contenant les items
            
            middlewares.py    # Fichier contenant les middlewares

            pipelines.py      # Fichier contenant les pipelines

            settings.py       # Fichier contenant les paramètres du projet

            spiders/          # Dossier contenant toutes les spiders
                __init__.py


Votre première spider
=====================

Les Spiders sont des classes Scrapy qui permettent de mettre en place toute l'architecture complexe définie plus haut. Pour définir une spider il vous faut hériter de la classe :class:`scrapy.Spider`. La seule chose à faire est de définir la première requête à effectuer et comment suivre les liens. La Spider ne s'arrêtera uniquement lorsqu'elle aura parcouru tous les liens qu'on lui à demander. 
