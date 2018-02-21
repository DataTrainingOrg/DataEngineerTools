Introduction
============

`Scrapy <https://scrapy.org/>`_ est un framework permettant de crawler des sites web et d'en extraire les données de façon structurée. 


Installation
------------

Nous travaillerons dans un environnement `Anaconda <https://www.anaconda.com/download/>`_, déjà présent sur les machines de l'ESIEE. Sur vos machines personnelles, télécharger la distribution correspondant à la version la plus récente de Python. 

.. note::
    `Python 2 ne sera plus maintenu à partir de 2020 <https://pythonclock.org/>`_.

`Scrapy <https://scrapy.org/>`_ ne fait pas partie de la distribution par défaut et doit être installé manuellement. Anaconda utilise `conda <https://conda.io/docs/>`_ pour gérer l'installation et la maintenance des packages : 

:command:`conda install -c conda-forge scrapy`.

Tester la réussite de l'opération dans un interpréteur Python. Avant installation::

    >>> import scrapy

    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    ModuleNotFoundError: No module named 'scrapy'

Après installation, l'importation du module ne provoque plus d'erreur::

    >>> import scrapy
    >>>

Architecture
------------

`Scrapy <https://scrapy.org/>`_ est un framework comportant plusieurs composants.

.. image:: images/architecture.png
    :scale: 75 %
    :align: center

L'ensemble du processus est contrôlé par l'*engine* (les termes anglo saxons ont été retenus pour un meilleur référencement dans la `documentation officielle <https://docs.scrapy.org/en/latest/>`_).

Fonctionnement
--------------

`Scrapy <https://scrapy.org/>`_ est entièrement organisé autour d'un composant central : l'*engine*.

Le rôle de l'*engine* est de contrôler le flux de données entre les différents composants du système. 

1. En particulier, il est chargé de récupérer les *requests* définies dans les *spiders* 
2. Ces *requests* sont ensuite fournies au *scheduler* qui se charge de leur ordonnancement
3. Les *requests* sont présentées selon cet ordonnancement à l'*engine*...
4. ... qui les transmet au *downloader* 
5. Le *downloader* effectue la *request* et transmet la *response* (le contenu de la page web) à l'*engine*...
6. ... puis l'envoie au *spider* pour traitement
7. Le *spider* génére des *items* qui sont transmis à l'*engine* 
8. Les *items* sont ensuite poussés dans un pipeline pour nettoyage, validation et stockage

Ce processus est répété jusqu'à épuisement des requêtes.

`Scrapy <https://scrapy.org/>`_ utilise des *middlewares* entre l'*engine* et le *downloader* et entre l'*engine* et le *spider*. Ces *middlewares* permettent d'inclure des traitements additionnels.

`Scrapy <https://scrapy.org/>`_ est un `framework orienté événements <https://en.wikipedia.org/wiki/Event-driven_architecture>`_ (basé sur `Twisted <https://twistedmatrix.com/>`_) permettant une programmation asynchrone (non bloquante). C'est particulièrement intéressant dans les opérations de scraping, puisque **le programme n'attend pas le résultat d'une requête pour en lancer une autre**. 

En effet, lorsque l'on sollicite une ressource (requête réseau, système de fichier, etc.) en mode bloquant, l'exécution du programme est suspendue le temps que la transaction avec la ressource se termine (par exemple le temps qu'une page web soit complètement téléchargée). L'intérêt de faire des appels non bloquants, c'est que l'on peut gérer de multiples téléchargements en parallèle, et que le programme peut continuer à tourner pendant ce temps. 

