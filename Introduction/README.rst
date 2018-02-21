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
- Nous avons actuellement un ferme de 750 crawlers qui permettent de récupérer environ 1500 pages secondes soit 5,4M de pages par heure.
- Le web francais est estimé à 150M de pages ce qui représente environ 2 Peta Bytes de données duppliquées.

Quelques mots clés et définitions
---------------------------------

Crawler
^^^^^^^
Un Crawler est un robot qui permet de récupérer des données non-structurées soit des informations textuelles, structurelles et de contenu d'un site web. 
La structure de l'algorithme utilisé doit être agnostique de la structure HTML du site web. Elle permet de récupérer des 
informations de base comme le texte, les images, les liens entrants ou sortants par exemple.

Scraper
^^^^^^^
Un Scraper est dépendant du site et de sa structure. Il permet de récupérer des informations beaucoup plus qualitatives
sur un site web. Les Scraper ne sont pas très facilement maintenables puisqu'ils sont basés sur la structure HTML qui est
vouée à changer plus ou moins rapidement selon les sites. 

Les bonnes pratiques
--------------------

On peut comprendre très rapidemement si les sites et les webmasters ont envie qu'on puisse accéder à leurs données. Plusieurs manières permettent de montrer ou d'expliciter les comportements non recommandés sur un site. 

Aujourd'hui certains sites utilisent des méthodes pour empecher la récupération massive de leurs données : 

- Génération à la volée de code HTML et CSS. Le nom des balises HTML est générée de facon à ce qu'on ne puisse pas se baser sur celles-ci. 
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

- https://www.google.com/robots.txt
- http://www.seloger.com/robots.txt
- https://www.leboncoin.fr/robots.txt
- https://booking.com/robots.txt

Site Map ou Site Index
^^^^^^^^^^^^^^^^^^^^^^
Le site map ou le site index (plan du site) sont des pages HTML générée pour améliorer le SEO d'une page. Le SEO (Search Engine Optimisation) permet d'optimiser le référencement sur les moteurs de recherche. La plupart des gros sites ont des équipes SEO dédiée qui permettent aux sites d'être présents dans les premières positions lors des recherches associées. 
Ces pages donnent accès à l'arbre de génération ou de structure du site. La plupart du temps elles permettent l'exploration massive et facile des sites au robots de crawl des moteurs de recherche.

Surcharge du serveur
^^^^^^^^^^^^^^^^^^^^
La plupart des sites importants ont des infrastructures qui tiennent la charge et qui peuvent être utilisées et appelées
un très grand nombre de fois. D'autres sont beaucoup plus restreint et donc il est important de ne pas surcharger ceux-ci.
Les sites comme Wikipédia ou StackOverFlow empèche les robots d'accéder trop rapidement à leurs infrastructures et force 
des temps d'arrêt entre la récupération des différentes pages.

Introduction au scraping
------------------------

Il existe deux grandes pratiques pour scraper un site efficacement nous allons aborder les deux :  

- Récupération et parsing du code HTML. Cette solution nécessite une compréhension du code et des notions basiques de DOM et architecture HTML.
- Récupération des appels API aux serveurs permettant de récupérer les informations directement à la source la plupart
du temps au format JSON. Cette deuxième solution est la plus efficace et facile mais les appels d'API sont souvent cachés
ou bloqués. 

Dans les deux cas, nous utiliserons des requêtes HTTP et le package ``requests``. Celui-ci permet de faire des requêtes très rapidement et facilement via un interpreter Python. De nombreux paramètres sont modifiables. 

Pour réaliser ces opérations une bonne pratique est d'utiliser l'outil de developpement de Chrome ou Firefox. Je conseil celui de Google qui est beaucoup plus intuitif et développé que celui de Mozilla. Il existe plusieurs raccourcis claviers mais la plus simple est de faire une click droit et ``inspecter``. 

.. image:: images/inspecteur.png

Deux onglets sont importants dans notre cas : 
 
- ``Element`` : la partie correspondant au code HTML, elle permet de visualiser la structure et répérer les pointeurs des balises qui encapsulent nos données. 
- ``Network`` : cette partie permet d'analyser tous les appels réseaux réalisés depuis le front. C'est ici que les appels de 
récupération de données sont effectués. 

Une requête HTTP
^^^^^^^^^^^^^^^^
Un requête HTTP est une requête basé sur le protocole TCP, elle fait partie de la couche application de la couche OSI. Elle permet d'accéder aux données mise à disposition sur une adresse IP (ou url résolue par un DNS) et un port. Les deux ports les plus utilisé dans le web sont le 80 pour les sites en HTTP et le 443 pour les sites en HTTPS. HTTPS est une variable du protocole HTTP basé sur le protocole TLS.

Il existe de nombreux types de requêtes selon la convention REST: GET, POST, PUT, DELETE, UPDATE. 

Dans notre cas nous allons utiliser la plupart du temps des GET et potentiellement des POST. 
* Le GET permet comme sont nom l'indique de récupérer des informations en fonction de certain paramètres.
* Le POST nécéssite un envoie de données pour récupérer des données. Le body du post est, la plupart du temps, envoyé sous la forme d'un objet JSON. 

Ces requêtes encapsulent un certain nombre de paramètres qui permettent soient d'identifier une provenance et un utilisateur 
ou de réaliser différentes actions. 

.. code-block:: Python

 >>> import requests

.. code-block:: Python

 >>> url = "http://www.esiee.fr/"
 >>> response = requests.get(url)
 >>> response.status_code
 200
 
Il existe deux méthodes pour récupérer le contenu de la page : 

- ``response.text`` qui permet de retourner le texte sous la forme d'une chaine de charactères.
- ``response.content`` qui permet de récupérer le contenu de la page sous la forme de bytes

.. code-block:: Python

 >>> type(response.content)
 <class 'bytes'>
 >>> type(response.text)
 <class 'str'>
 
Pour récupérer les 1000 premiers charactères de la page : 

.. code-block:: Python

 >>> response.text[0:1000]
 '<!DOCTYPE html>\n<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->\n<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->\n<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->\n<!--[if IE 9]>         <html class="no-js ie9"> <![endif]-->\n<!--[if gt IE 9]><!--> <html class="no-js"> <!--<![endif]-->\n<head profile="http://www.w3.org/1999/xhtml/vocab">\n  <meta name="google-site-verification" content="JnG7DTdhQuWTeSHlWC63CeWpb3WValiOorksYjoYOWI" />\n  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n<meta name="Generator" content="Drupal 7 (http://drupal.org)" />\n<meta name="description" content="École d’ingénieurs généraliste dans les domaines des nouvelles technologies, ESIEE Paris propose une formation en 5 ou 3 ans habilitée par la CTI." />\n<link rel="shortcut icon" href="http://www.esiee.fr/sites/all/themes/custom/esiee_theme/favicon.ico" type="image/vnd.microsoft.icon" />\n  <title>Page d\'accueil | ESIEE Paris</tit'
    
Pour récupérer les headers HTTP de la réponse : 

.. code-block:: Python
    
 >>> response.headers
 {'Date': 'Mon, 12 Feb 2018 12:24:06 GMT', 'Server': 'Apache', 'Expires': 'Sun, 19 Nov 1978 05:00:00 GMT', 'Cache-Control': 'no-cache, must-revalidate', 'X-Content-Type-Options': 'nosniff', 'Content-Language': 'fr', 'X-Frame-Options': 'SAMEORIGIN', 'X-Generator': 'Drupal 7 (http://drupal.org)', 'Vary': 'Accept-Encoding', 'Content-Encoding': 'gzip', 'X-Robots-Tag': 'index,follow,noarchive', 'X-XSS-Protection': '1; mode=block', 'X-Download-Options': 'noopen;', 'X-Permitted-Cross-Domain-Policies': 'none', 'Content-Length': '16258', 'Keep-Alive': 'timeout=5, max=150', 'Connection': 'Keep-Alive', 'Content-Type': 'text/html; charset=utf-8'}

On peut modifier les paramêtres de la requête. On peut par exemple ajouter un UserAgent et un timeout de 10 secondes: 

.. code-block:: Python

    >>> headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
 >>> response = requests.get(url, headers=headers, timeout = 10)
 >>> response.content[0:1000]
 b'<!DOCTYPE html>\n<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->\n<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->\n<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->\n<!--[if IE 9]>         <html class="no-js ie9"> <![endif]-->\n<!--[if gt IE 9]><!--> <html class="no-js"> <!--<![endif]-->\n<head profile="http://www.w3.org/1999/xhtml/vocab">\n  <meta name="google-site-verification" content="JnG7DTdhQuWTeSHlWC63CeWpb3WValiOorksYjoYOWI" />\n  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n<meta name="Generator" content="Drupal 7 (http://drupal.org)" />\n<meta name="description" content="\xc3\x89cole d\xe2\x80\x99ing\xc3\xa9nieurs g\xc3\xa9n\xc3\xa9raliste dans les domaines des nouvelles technologies, ESIEE Paris propose une formation en 5 ou 3 ans habilit\xc3\xa9e par la CTI." />\n<link rel="shortcut icon" href="http://www.esiee.fr/sites/all/themes/custom/esiee_theme/favicon.ico" type="image/vnd.microsoft.icon" />\n  <title>Page d\'accueil | ESIEE Par'
    
.. note:: Exercice 1

 - Créer une classe Python permettant de faire des requêtes HTTP. 
 - Cette classe doit utiliser toujours le même UserAgent. 
 - Le TimeOut sera spécifié à chaque appelle avec une valeur par défaut.
 - Un mécanisme de retry sera mis en place de façon recursive. 

.. note:: Exercice 2

 - Faire une fonction permettant de supprimer tous les espaces supperflus d'une string
 - Faire une fonction qui prend une string html et renvois une string intelligible (enlever les caractères spéciaux, 
 - Récupérer le domaine en fonction d'un url

Exploitation du code HTML
^^^^^^^^^^^^^^^^^^^^^^^^^
Ici, il faut récupérer le code HTML d'un site web à partir d'une requête. Lorsque vous avez récupéré le texte d'un site 
il faut le parser. Pour cela, on utilise BeautifulSoup qui permet de transformer la structure HTML en objet Python. Cela 
permet de récupérer efficacement les données qui nous intéresse.  

Pour les webmasters, le blocage le plus souvent mis en place et un blocage sur le User-Agent. Le User-Agent est un paramètre intégré
dans la requête HTTP réalisé par le Navigateur pour envoyer au front des informations basiques :

- la version du Navigateur,
- la version de l'OS
- Le type de gestionnaire graphique (Gecko)
- le type de device utilisé

Exemple de User Agent 

    Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0

Utilisation de BeautifulSoup :

.. code-block:: bash

    pip install bs4

.. code-block:: Python

    import requests
    from bs4 import BeautifulSoup  
    
Pour transformer une requête (requests) en objets BeautifulSoup : 

.. code-block:: Python

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")   
    
Il se peut qu'un message d'erreur arrive à ce point là si vous n'avez pas la librarie ``lxml`` installée, pour se faire vous avez juste à lancer la commande suivante : ``pip install lxml``.
    
Pour trouver tous les liens d'une page on récupère la balise a : 

.. code-block:: Python

 >>> soup.find_all("a")[0:10]
 [<a href="#">
 <i class="icon-parametres"></i>
 </a>, <a href="https://gmail.com" target="_blank" title="Webmail ESIEE Paris"><i><img alt="" src="http://www.esiee.fr/sites/default/files/menu_icons/menu_icon_950.png"/> </i><span>Webmail ESIEE Paris</span></a>, <a href="https://planif.esiee.fr/direct/" target="_blank" title="Emploi du temps général"><i><img alt="" src="http://www.esiee.fr/sites/default/files/menu_icons/menu_icon_1331.png"/> </i><span>Emploi du temps général</span></a>, <a href="https://planif.esiee.fr/jsp/custom/esiee/easyMyPlanning.jsp" target="_blank" title="Emploi du temps individuel"><i><img alt="" src="http://www.esiee.fr/sites/default/files/menu_icons/menu_icon_1332.png"/> </i><span>Emploi du temps individuel</span></a>, <a href="https://intra.esiee.fr" target="_blank" title="Extranet"><i><img alt="" src="http://www.esiee.fr/sites/default/files/menu_icons/menu_icon_951.png"/> </i><span>Extranet</span></a>, <a href="https://esiee.blackboard.com" target="_blank" title="iCampus"><i><img alt="" src="http://www.esiee.fr/sites/default/files/menu_icons/menu_icon_1311.png"/> </i><span>iCampus</span></a>, <a href="http://e5.onthehub.com/WebStore/Welcome.aspx?vsro=8&amp;ws=45AD823E-799B-E011-969D-0030487D8897&amp;JSEnabled=1" target="_blank" title="Microsoft DreamSpark"><i><img alt="" src="http://www.esiee.fr/sites/default/files/menu_icons/menu_icon_1696.png"/> </i><span>Microsoft DreamSpark</span></a>, <a href="/en">
 <i>
 <img alt="English" src="/sites/all/themes/custom/esiee_theme/assets/images/flag-en.png"/>
 </i>
 </a>, <a href="https://www.facebook.com/esieeparis" target="_blank">
 <i class="fa fa-facebook"></i>
 </a>, <a href="https://twitter.com/ESIEEPARIS" target="_blank">
 <i class="fa fa-twitter"></i>
 </a>]
 >>> 
    
On peut préciser la classe voulue : 

.. code-block:: Python

    soup.find_all(class_="<CLASS_NAME>")[0:10]

Par exemple : 

.. code-block:: Python

 >>> soup.find_all(class_="slide")[0:5]
 [<div class="slide slide-content">
 <span class="slide-content-date inline-block"><span class="date-display-single">15.01.2018</span></span>
 <span class="slide-content-theme inline-block is-uppercase">Admissions</span>
 <div class="clearfix"></div>
 <div class="slide-content-img pull-left"><!-- scald=1434:news_thumbnail --><img alt="illustration-admissions-actu.jpg" height="90" src="http://www.esiee.fr/sites/default/files/styles/news/public/thumbnails/image/illustration-admissions-actu.jpg?itok=uKSbuL6y" title="Ouverture de la plate-forme des admissions ESIEE Paris" width="120"/><!-- END scald=1434 --></div>
 <span class="slide-content-title"><a class="is-uppercase" href="/fr/actualite/inscriptions-rentree-2018">Votre inscription, c'est maintenant !</a></span>
 <div class="clearfix"></div>
 <p class="slide-content-desc">Le portail Parcoursup et la plateforme Admissions ESIEE Paris sont ouverts.</p> </div>, <div class="slide slide-content">
 <span class="slide-content-date inline-block"><span class="date-display-single">21.12.2017</span></span>
 <span class="slide-content-theme inline-block is-uppercase">Journée portes ouvertes</span>
 <div class="clearfix"></div>
 <div class="slide-content-img pull-left"><!-- scald=1689:news_thumbnail --><img alt="illustration-jpo-2018.jpg" height="90" src="http://www.esiee.fr/sites/default/files/styles/news/public/thumbnails/image/illustration-jpo-2018.jpg?itok=-YCadC35" title="Illustration Journées Portes Ouvertes" width="120"/><!-- END scald=1689 --></div>
 <span class="slide-content-title"><a class="is-uppercase" href="/fr/actualite/journee-portes-ouvertes-10-fevrier-2018">Bien choisir son école, c’est aussi la rencontrer !</a></span>
 <div class="clearfix"></div>
 <p class="slide-content-desc">ESIEE Paris vous convie à la prochaine Journée Portes Ouvertes (JPO) qui aura lieu le samedi 10 février de 9h30 à 17h30. </p> </div>, <div class="slide slide-content">
 <span class="slide-content-date inline-block"><span class="date-display-single">04.12.2017</span></span>
 <span class="slide-content-theme inline-block is-uppercase">Admissions</span>
 <div class="clearfix"></div>
 <div class="slide-content-img pull-left"><!-- scald=1404:news_thumbnail --><img alt="illustration-paces-etudiants-passerelle.jpg" height="90" src="http://www.esiee.fr/sites/default/files/styles/news/public/thumbnails/image/illustration-paces-etudiants-passerelle.jpg?itok=Acm93yfD" title="Illustration actualité programme paces" width="120"/><!-- END scald=1404 --></div>
 <span class="slide-content-title"><a class="is-uppercase" href="/fr/fr/actualite/programme-passerelle-2018"> Se réorienter après PACES ? C’est possible grâce au programme Passerelle</a></span>
 <div class="clearfix"></div>
 <p class="slide-content-desc">ESIEE Paris permet aux étudiants issus de PACES ou 1re année de CPGE scientifique d’intégrer le programme « Passerelle » pour se réorienter sans perdre d’année.</p> </div>, <div class="slide slide-content">
 <span class="slide-content-date inline-block"><span class="date-display-single">31.01.2018</span></span>
 <span class="slide-content-theme inline-block is-uppercase">Séminaire</span>
 <div class="clearfix"></div>
 <div class="slide-content-img pull-left"><!-- scald=1740:news_thumbnail --><img alt="visuel-captronics.jpg" height="90" src="http://www.esiee.fr/sites/default/files/styles/news/public/thumbnails/image/visuel-captronics.jpg?itok=iOE9XiJ7" title="Séminaire Captronics" width="120"/><!-- END scald=1740 --></div>
 <span class="slide-content-title"><a class="is-uppercase" href="/fr/actualite/seminaire-captronics">Séminaire « PME, TPE, Startup » : Accélérez vos projets de miniaturisation d’objets connectés !</a></span>
 <div class="clearfix"></div>
 <p class="slide-content-desc">CAP’TRONIC, ESIEE Paris et le Réseau Mesure organise un séminaire consacré à la réalisation d’objets connectés pour les PME.</p> </div>, <div class="slide slide-content">
 <span class="slide-content-date inline-block"><span class="date-display-single">29.01.2018</span></span>
 <span class="slide-content-theme inline-block is-uppercase">Actualités</span>
 <div class="clearfix"></div>
 <div class="slide-content-img pull-left"><!-- scald=1229:news_thumbnail --><img alt="Journée des cordées de la réussite" height="90" src="http://www.esiee.fr/sites/default/files/styles/news/public/thumbnails/image/visuel-jourrnee-des-cordees-de-la-reussite-2016.jpg?itok=dmQZ8UJy" title="Journée des cordées de la réussite" width="120"/><!-- END scald=1229 --></div>
 <span class="slide-content-title"><a class="is-uppercase" href="/fr/actualite/esiee-paris-cordees-de-la-reussite-2018">ESIEE Paris a participé à la journée nationale des cordées de la réussite</a></span>
 <div class="clearfix"></div>
 <p class="slide-content-desc">L'école a participé une nouvelle fois, le vendredi 26 janvier 2018, aux Cordées de la réussite en collaboration avec ses partenaires de la cité Descartes.</p> </div>]
 >>> 
    
Pour récupérer le text sans les balises HTML : 

.. code-block:: Python

 >>> soup.text[0:1000]
 ' \n\n\n\n\n\n\nPage d\'accueil | ESIEE Paris\n\n\n@import url("http://www.esiee.fr/modules/system/system.base.css?p40jh1");\n@import url("http://www.esiee.fr/modules/system/system.menus.css?p40jh1");\n@import url("http://www.esiee.fr/modules/system/system.messages.css?p40jh1");\n@import url("http://www.esiee.fr/modules/system/system.theme.css?p40jh1");\n\n\n@import url("http://www.esiee.fr/sites/all/modules/contrib/date/date_api/date.css?p40jh1");\n@import url("http://www.esiee.fr/sites/all/modules/contrib/scald/modules/library/dnd/css/editor-global.css?p40jh1");\n@import url("http://www.esiee.fr/modules/field/theme/field.css?p40jh1");\n@import url("http://www.esiee.fr/sites/all/modules/contrib/google_cse/google_cse.css?p40jh1");\n@import url("http://www.esiee.fr/modules/node/node.css?p40jh1");\n@import url("http://www.esiee.fr/sites/all/modules/contrib/scald_file/scald_file.css?p40jh1");\n@import url("http://www.esiee.fr/modules/search/search.css?p40jh1");\n@import url("http://www.esiee.fr/modules/user/user.'
 >>> 

.. note:: Exercice 3

 Améliorer la classe développé précédemment.

 - ajouter une méthode pour récupérer l'objet soup d'un url 
 - Récupérer une liste de User Agent et effectuer une rotation aléatoire sur celui à utiliser 
 - Utiliser cette classe pour parser une page HTML et récupérer : le titre, tous les H1 (si ils existes), les liens vers les images, les liens sortants vers d'autres sites, et le texte principal.

 Parsing d'un sitemaps pour récupérer une listes de liens avec les informations disponibles. -> Stocker dans un dictionnaire et dans un fichier JSON local. 


Exploitation des appels d'API  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
Losque le front du site récupère des données sur une API géré par le back, un appel d'API est réalisé. Cet appel est recensé 
dans les appels réseaux. Il est alors possible de re-jouer cet appel pour récupérer à nouveau les données. Il est très facile de récupérer ces appels dans l'onglet Network de la console développeur de Chrome ou FireFox. La console vous permet de copier le code CURL pour effectuée et vous pouvez ensuite la transformer en code Python depuis le site https://curl.trillworks.com/.

Souvent les APIs sont bloquées avec certain paramètres. L'API verifie que dans les headers de la requêtes HTTP ces
paramètres sont présents :
* un token généré à la volée avec des protocole OAuth2 (ou moins développés). 
* un referer provenant du site web (la source de la requête), très facile à falsifier.  

.. note:: Exercice 4

 - Utiliser les informations développées plus haut pour récupérer les premiers résultats d'une recherche d'une requête 
 sur Qwant.

Exercice Final
--------------
Utilisez tout ce que vous avez appris pour récupérer des articles de News avec une catégorie. Il est souvent intéressant de partir des flux RSS pour commencer : 

Les données doivent comprendre : 
 * Le texte important propre
 * L'url 
 * Le domaine
 * la catégorie
 * Le titre de l'article
 * Le titre de la page
 * (Facultatif) : les images
