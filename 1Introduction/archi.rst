============
Architecture
============

Il est important en développement logiciel de réfléchir directement à une infrastructure solide et scalable.
Cela demande un coût de développement plus important mais un coût de maintenance beaucoup plus restreint.

Plusieurs technologies peuvent être utilisées en fonction des besoins et des affinités de chacun.

Récupération des données
------------------------
Pour la récupération des données n'importe quelle technologie peut être utilisée. Il suffit de pouvoir faire des requêtes 
HTTP et de pouvoir parser le résultat. Tous les langages de programmation possèdent des API pour faire ces transformations.
En python de nombreuses librairies ont été développée dans ce but et nous en aborderons plusieurs dans ce cours :

* Requests (+ requests_cache qui fait gagner un temps précieux lors des développements)
* BeautifulSoup (permet de créer un objet python à partir de code HTML pour faciliter l'extraction)
* Readability (permet de récupérer le texte pertinent d'une page web)
* Scrapy (Framework de Spider permettant de gérer le Crawling et le Scraping de site web très efficacement)

Stockage
--------

Pour le stockage un grand nombre de bases de données sont disponibles sur le marché. Chacune ayant sa particularité, il est 
souhaitable de bien définir les besoins et le format des données pour utiliser la base la plus adaptée à son environnement.
Dans le contexte du web, les bases noSQL sont très recherchées et demandées, à cause de leur structure très flexible et optimisée
pour le stockage de données hétérogènes.
Quelques examples de bases de données : 

* MySQL (Base de données relationnelles, stockage sous forme de tableau, optimale pour le stockage de chiffres) ;
* PostGreSQL (Deuxième base de données relationnelles, avec une surcouche d'optimisation pour les données géolocalisées) ;
* Cassandra (Base de données noSQL developpée pour garantir une scalabilité et intégrité d'un grand nombre de données) ;
* MongoDB (Base de données noSQL, stockage sous la forme de document JSON)
* Redis (Base de données noSQL, stockage sous la forme de données clé:valeurs avec très grandes performances)
* ElasticSearch n'est pas réellement une base de données, c'est un moteur de recherche qui permet de faire de la recherche 
très efficacement dans des données textuelles, numériques et géolocalisées.

Scalabilité
-----------
Tout dépend de ce dont vous avez besoin mais souvent l'extraction sur une seule machine et un seul processus 
s'avérera trop lente et peu efficace. Il existe des outils permettant de distribuer la charge de calcul.
Pour ce faire, une queue de messages est créée, ce qui permet d'envoyer les instructions à différents programmes devant les
exécuter. 
Les deux les plus utilisés sont :

* RabbitMQ : développé initialement pour l'internet des objets et l'échange de données entre objets connectés.
* Kafka : développé par les équipes de LinkedIn pour faire du streaming de données et partager les données avec différentes interfaces.

Exemple d'Architecture
----------------------
.. image:: images/architecture_globale.png
   :height: 100px
   :width: 200 px
   :scale: 50 %
   :alt: Global Architecture
   :align: right
