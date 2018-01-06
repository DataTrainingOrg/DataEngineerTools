============
Introduction
============

Aujourd'hui l'or noir des entreprises est la donnée. Il existe une infinité de sources potentiellement récupérables 
et utilisables: 
- Données propriétaires (Données clients, Données d'exploitation, Données de capteurs...)
- Données Open Data (Adresses, Démographie des départements ou villes...)
- Données publiques disponibles sur le web (Tweets, Réseaux sociaux, produits leboncoin...)

Dans la quête de Data de chaque entreprise, l'important et d'agréger et de mettre en relation un grand nombre de données
différentes pour pouvoir en tirer le maximum d'informations et de mettre en place des axes d'améliorartion. 

Présentation du cours
---------------------

Le but de ce cours est de présenter les tenants et les aboutissants d'une infrastucture de récupération de données.

Contexte de Qwant
^^^^^^^^^^^^^^^^^
Qwant est un moteur de recherche européen basé sur un concept fort de vie privée. Nous ne gardons pas les informations
utilisateurs. 
Pour avoir quelques chiffres: 
- Nous avons actuellement un ferme de 750 crawlers qui permettent de récupérer environ 1500 pages secondes soit
 5,4M de pages par heure.
- Le web francais est estimé à 150M de pages ce qui représente environ 2 Peta Bytes de données duppliquées.

Quelques mots clés et définitions
---------------------------------

Crawler
^^^^^^^
Un Crawler est un robot qui permet de récupérer des informations textuelles, structurelles et de contenu d'un site web. 
La structure de l'algorithme utilisé doit être agnostique de la structure HTML du site web. Elle permet de récupérer des 
informations de base comme le texte, les images, les liens entrants ou sortants.

Scraper
^^^^^^^
Un Scraper est dépendant du site et de sa structure. Il permet de récupérer des informations beaucoup plus qualitatives
sur un site web. Les Scraper ne sont pas très facilement maintenables puisqu'il est basé sur la structure HTML qui est
vouée à changer plus ou moins rapidement selon les sites. 

Les bonnes pratiques
--------------------

On peut comprendre très rapidemement si les sites ont envie qu'on puisse accéder à leurs données. Plusieurs manères 
permettent de montrer ou d'expliciter les comportements non recommandés sur un site. 

Aujourd'hui certains sites utilisent des méthodes pour empecher la récupération massive de leurs données : 

 - Génération à la volée de code HTML et CSS. Le nom des balises HTML est générée de facon à ce qu'on ne puisse
  pas se baser sur celles-ci. 
 - Black list d'adresses IP détectées.
 - Génération de contenu via du JavaScript
 - Algorithmes de détection de comportements non-humains (vitesse de navigation, scroll, click,  etc)

Plusieurs méthodes sont possibles pour éviter ou contourner ces limitations mais elles ne seront pas abordées dans ce cours.

Robots.txt
^^^^^^^^^^
La limitation la plus simple et la plus connue est le fichier Robots.txt. Il est édité par les webmasters des sites 
pour "contrôler" le comportement des robots sur leur site. Différentes politiques sont mises en place par les organismes
en fonction des problématiques métiers. Ce fichier n'empêche absolument pas de récupérer les données mais fait part d'une 
bonne pratique.

https://www.google.com/robots.txt
http://www.seloger.com/robots.txt
https://www.leboncoin.fr/robots.txt
https://booking.com/robots.txt

Site Map ou Site Index
^^^^^^^^^^^^^^^^^^^^^^
Le site map ou le site index sont des pages HTML générée pour améliorer le SEO d'une page. Le SEO (Search Engine Optimisation)
permet d'optimiser le référencement sur les moteurs de recherche. La plupart des gros sites ont des équipes SEO qui permettent
d'arriver dans les premières positions lors des recherches associées. 
Ces deux pages donnent accès à l'arbre de génération du site. La plupart du temps elles permettent l'exploration massive
et facile des sites au robots de crawl des moteurs de recherche.

Surcharge du serveur
^^^^^^^^^^^^^^^^^^^^
La plupart des sites importants ont des infrastructures qui tiennent la charge et qui peuvent être utilisées et appelées
un très grand nombre de fois. D'autres sont beaucoup plus restreint et donc il est important de ne pas surcharger ceux-ci.
Les sites comme Wikipédia ou StackOverFlow empèche les robots d'accéder trop rapidement à leurs infrastructures et force 
des temps d'arrêt entre les pages


Introduction au scraping
------------------------

Il existe deux grandes pratiques pour scraper un site efficacement nous allons aborder les deux :  

- Récupération et parsing du code HTML. Cette solution nécessite une compréhension du code et des notions basiques de DOM et architecture HTML.
- Récupération des appels API aux serveurs permettant de récupérer les informations directement à la source la plupart
du temps au format JSON. Cette deuxième solution est la plus efficace et facile mais les appels d'API sont souvent cachés
ou bloqués. 

Dans les deux cas, nous utiliserons des requêtes HTTP et le package requests. Celui-ci permet de faire des requêtes très rapidement 
et facilement via un interpreter Python. De nombreux paramètres sont modifiables. 

Pour réaliser ces opérations une bonne pratique est d'utiliser l'outil de developpement de Chrome ou Firefox. Je conseil
du moins celui de Chrome qui est beaucoup plus intuitif et développé. Deux onglets sont important dans notre cas : 

* La partie code HTML qui permet de récupérer les pointeurs des balises qui encapsulent nos données. 
* La partie Network qui permet d'analyser tous les appels réseaux réalisés depuis le front. C'est ici que les appels de 
récupération de données sont effectués. 


Une requête HTTP
^^^^^^^^^^^^^^^^
Un requête HTTP est une requête basé sur le protocole XXXXXX. Elle permet d'accéder aux données mise à disposition sur une
adresse IP (ou url résolue par un DNS) et un port. Les deux ports les plus utilisé dans le web sont le 80 pour les sites en 
HTTP et le 443 pour les sites en HTTPS. 
# TODO : Expliquer plus en détails les ports et le protocole HTTP. 

Il existe de nombreux types de requêtes selon la convention REST: GET, POST, PUT, DELETE, UPDATE. 

Dans notre cas nous allons utiliser la plupart du temps des GET et potentiellement des POST. 
* Le GET permet comme sont nom l'indique de récupérer des informations en fonction de certain paramètres. Alors que
* Le POST nécéssite un envoie de données pour récupérer des données. Le body du post est envoyé sous la forme d'un objet JSON. 

Ces requêtes encapsulent un certain nombre de paramètres qui permettent soient d'identifier une provenance et un utilisateur 
ou de réaliser différentes actions. 

# TODO: Exercices

Exploitation du code HTML
^^^^^^^^^^^^^^^^^^^^^^^^^
Ici, il faut récupérer le code HTML d'un site web à partir d'une requête. Lorsque vous avez récupéré le texte d'un site 
il faut le parser. Pour cela, on utilise BeautifulSoup qui permet de transformer la structure HTML en objet Python. Cela 
permet de récupérer efficacement les données qui nous intéresse.  

Pour les webmasters, le blocage le plus souvent mis en place et un blocage sur le User-Agent. Le User-Agent est un paramètre intégré
dans la requête HTTP réalisé par le Navigateur pour envoyer au front des informations basiques :
* la version du Navigateur,
* la version de l'OS
* Le type d # TODO : Gecko moteur de gestion graphique du HTML 
* le type de device utilisé

# TODO: Exemple de UserAgent

# TODO: Mettre en place quelques exercices de récupération de données
    * Netoyage de string HTML 
    * Enlever tous les espaces supperflues 
    * Récupérer le domaine en fonction d'un url

pip install bs4

import requests
from bs4 import BeautifulSoup

Un autre package très utile pour récupérer des données d'un site web est Readability. # TODO: Historique de Readability

pip install python-Readability

from readability import Document
doc = Document(response.text)
print("Le titre de la page est {}".format(doc.title())
print("Le texte important de la page est")
print(doc.summary())


# TODO: Exercices 

Parsing d'un sitemaps pour récupérer une listes de liens avec les informations disponibles. -> Stocker dans un dictionnary et un fichier JSON. 


Exploitation des appels d'API  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
Losque le front du site récupère des données sur une API géré par le back, un appel d'API est réalisé. Cet appel est recensé 
dans les appels réseaux. Il est alors possible de re-jouer cet appel pour récupérer à nouveau les données. 

Souvent les APIs sont bloquées avec certain paramètres. L'API verifie que dans les headers de la requêtes HTTP ces
paramètres sont présents :
* un token généré à la volée avec des protocole OAuth (ou moins développés). 
* un referer provenant du site web (la source de la requête), très facile à falsifier.  

# TODO: Exercices 

Utiliser les informations développées plus haut pour récupérer les premiers résultats d'une recherche d'une requête 
sur Qwant ou sur Google.

Exercice Final
--------------
Utilisez tout ce que vous avez appris pour récupérer des articles de News avec une catégorie. 
Les données doivent comprendre : 
* Le texte important propre
* L'url 
* Le domaine
* la catégorie
* Le titre de l'article
* Le titre de la page
* (Facultatif) : les images











