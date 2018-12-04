Votre premier projet
====================

Dans un premier temps vous devez créer un projet Scrapy avec la commande : 

.. code-block:: bash

    scrapy startproject newscrawler
    
Cette commande va créer un dossier ``monprojet`` contenant les éléments suivants correspondant au squelette ::

    newscrawler/
        scrapy.cfg            # Options de déploiement

        newscrawler/             # Le module Python contenant les informations
            __init__.py

            items.py          # Fichier contenant les items
            
            middlewares.py    # Fichier contenant les middlewares

            pipelines.py      # Fichier contenant les pipelines

            settings.py       # Fichier contenant les paramètres du projet

            spiders/          # Dossier contenant toutes les spiders
                __init__.py


Votre première Spider
=====================

Une Spider est une classe Scrapy qui permet de mettre en place toute l'architecture complexe vue dans l'introduction. Pour définir une spider, il vous faut hériter de la classe `scrapy.Spider`. La seule chose à faire est de définir la première requête à effectuer et comment suivre les liens. La Spider s'arrêtera lorsqu'elle aura parcouru tous les liens qu'on lui a demandé de suivre. 

Pour créer une Spider on utilise la syntaxe: 

.. code-block:: bash

    scrapy genspider <SPIDER_NAME> <DOMAIN_NAME>

Par exemple, 

.. code-block:: bash

    cd newscrawler
    scrapy genspider lemonde lemonde.fr
    
Cette commande permet de créer une spider appelée ``lemonde`` pour scraper le domaine ``lemonde.fr``. Cela crée le fichier Python ``spiders/lemonde.py`` suivant :

.. code-block:: Python

    # -*- coding: utf-8 -*-
    import scrapy


    class LemondeSpider(scrapy.Spider):
        name = "lemonde"
        allowed_domains = ["www.lemonde.fr"]
        start_urls = ['http://www.lemonde.fr/']

        def parse(self, response):
            pass


Une bonne pratique pour commencer à développer une Spider est de passer par l'interface Shell proposée par Scrapy. Elle permet de récupérer un objet ``Response`` et de tester les méthodes de récupération des données.
 
 
.. code-block:: bash
    
    scrapy shell 'http://lemonde.fr'
    
Pour les utilisateurs de windows il vous faut mettre des doubles quotes : 

.. code-block:: bash
    
    scrapy shell "http://lemonde.fr"
    
Scrapy lance un kernel Python 

.. code-block:: bash

    2018-12-02 16:05:50 [scrapy.utils.log] INFO: Scrapy 1.3.3 started (bot: newscrawler)
    2018-12-02 16:05:50 [scrapy.utils.log] INFO: Overridden settings: {'BOT_NAME': 'newscrawler', 'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter', 'LOGSTATS_INTERVAL': 0, 'NEWSPIDER_MODULE': 'newscrawler.spiders', 'ROBOTSTXT_OBEY': True, 'SPIDER_MODULES': ['newscrawler.spiders']}
    2018-12-02 16:05:50 [scrapy.middleware] INFO: Enabled extensions:
    ['scrapy.extensions.corestats.CoreStats',
    'scrapy.extensions.telnet.TelnetConsole']
    2018-12-02 16:05:50 [scrapy.middleware] INFO: Enabled downloader middlewares:
    ['scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware',
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware',
    'scrapy.downloadermiddlewares.retry.RetryMiddleware',
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware',
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware',
    'scrapy.downloadermiddlewares.stats.DownloaderStats']
    2018-12-02 16:05:50 [scrapy.middleware] INFO: Enabled spider middlewares:
    ['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',
    'scrapy.spidermiddlewares.referer.RefererMiddleware',
    'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
    'scrapy.spidermiddlewares.depth.DepthMiddleware']
    2018-12-02 16:05:50 [scrapy.middleware] INFO: Enabled item pipelines:
    []
    2018-12-02 16:05:50 [scrapy.extensions.telnet] DEBUG: Telnet console listening on 127.0.0.1:6023
    2018-12-02 16:05:50 [scrapy.core.engine] INFO: Spider opened
    2018-12-02 16:05:50 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://www.lemonde.fr/robots.txt> (referer: None)
    2018-12-02 16:05:50 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://www.lemonde.fr/> (referer: None)
    2018-12-02 16:05:54 [traitlets] DEBUG: Using default logger
    2018-12-02 16:05:54 [traitlets] DEBUG: Using default logger
    [s] Available Scrapy objects:
    [s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
    [s]   crawler    <scrapy.crawler.Crawler object at 0x10fc38c18>
    [s]   item       {}
    [s]   request    <GET https://www.lemonde.fr/>
    [s]   response   <200 https://www.lemonde.fr/>
    [s]   settings   <scrapy.settings.Settings object at 0x113bb0898>
    [s]   spider     <DefaultSpider 'default' at 0x113e60cc0>
    [s] Useful shortcuts:
    [s]   fetch(url[, redirect=True]) Fetch URL and update local objects (by default, redirects are followed)
    [s]   fetch(req)                  Fetch a scrapy.Request and update local objects
    [s]   shelp()           Shell help (print this help)
    [s]   view(response)    View response in a browser
    
Grâce à cette interface, vous avez accès à plusieurs objets comme la ``Response``, la ``Request``,  la ``Spider`` par exemple. Vous pouvez aussi exécuter ``view(response)`` pour afficher ce que Scrapy récupère dans un navigateur.


.. code-block:: Python

    In [1]: response
    Out[1]: <200 https://www.lemonde.fr/>
    
    In [3]: request
    Out[3]: <GET https://www.lemonde.fr/>

    In [4]: type(request)
    Out[4]: scrapy.http.request.Request
    
    In [5]: spider
    Out[5]: <LemondeSpider 'lemonde' at 0x1080fccc0>

    In [6]: type(spider)
    Out[6]: monprojet.spiders.lemonde.LeMondeSpider
   
   
Ici on voit que la Spider est une instance de LemondeSpider. Lorsqu'on lance le `scrapy shell` scrapy va chercher dans les spiders si une correspond au lien passé en paramètre, si oui , il l'utilise sinon une `DefaultSpider` est instanciée. 

Vos premières requêtes
----------------------

On peut commencer à regarder comment extraire les données de la page web en utilisant le langage de requêtes proposé par Scrapy. Il existe deux types de requêtes : les requêtes ``css`` et ``xpath``. Les requêtes ``xpath`` sont plus complexes mais plus puissantes que les requêtes ``css``. Dans le cadre de ce tutorial, nous allons uniquement aborder les requêtes ``css``, elles nous suffiront pour extraire les données dont nous avons besoin (en interne, Scrapy transforme les requêtes ``css``en requêtes ``xpath``. 

Que ce soit les requêtes ``css`` ou ``xpath``, elles crééent des sélecteurs de différents types.
Quelques exemples :

Pour récupérer le titre d'une page : 

.. code-block:: Python

    In [1]: response.css('title')
    Out[1]: [<Selector xpath='descendant-or-self::title' data='<title>Le Monde.fr - Actualités et Infos'>]
    
On récupère une liste de sélecteurs correspondant à la requête ``css`` appelée. La requête précédente était unique, d'autres requêtes moins restrictives permettent de récupérer plusieurs résultats. 
Par exemple pour rechercher l'ensemble des liens présents sur la page, on va rechercher les balises HTML ``<a></a>``

.. code-block:: Python

    In [5]: response.css("a")[0:10]
    Out[5]:
    [<Selector xpath='descendant-or-self::a' data='<a target="_blank" data-target="jelec-he'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/"> <div class="logo__lemonde l'>,
    <Selector xpath='descendant-or-self::a' data='<a href="https://secure.lemonde.fr/sfuse'>,
    <Selector xpath='descendant-or-self::a' data='<a href="https://abo.lemonde.fr/#xtor=CS'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/" class="Burger__right-arrow j'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/" class="Burger__right-arrow j'>,
    <Selector xpath='descendant-or-self::a' data='<a href="#" class="js-dropdown Burger__r'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/mouvement-des-gilets-jaunes/" '>,
    <Selector xpath='descendant-or-self::a' data='<a href="/carlos-ghosn/" data-suggestion'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/implant-files/" data-suggestio'>]
    
Pour récupérer le texte contenu dans les balises, on passe le paramètre ``<TAG>::text``. Par exemple : 
    
.. code-block:: Python

    In [6]: response.css("title::text")
    Out[6]: [<Selector xpath='descendant-or-self::title/text()' data='Le Monde.fr - Actualités et Infos en Fra'>]
    
.. note:: Exercice 

    Comparer les résultats des deux requêtes ``response.css('title')`` et ``response.css('title::text')``.
    
Maintenant pour extraire les données des selecteurs on utilise l'une des deux méthodes suivantes :
- ``extract()`` permet de récupérer une liste des données extraites de tous les sélecteurs
- ``extract_first()`` permet de récupérer une ``String`` provenant du premier sélecteur de la liste.

.. code-block:: Python

    In [7]: response.css('title::text').extract_first()
    Out[7]: 'Le Monde.fr - Actualités et Infos en France et dans le monde'
    
On peut récupérer un attribut d'une balise avec la syntaxe ``<TAG>::attr(<ATTRIBUTE_NAME>)``:

Par exemple, les liens sont contenus dans un attribut ``href``.

.. code-block:: Python

    In [9]: response.css('a::attr(href)')[0:10]
    Out[9]:
    [<Selector xpath='descendant-or-self::a/@href' data='https://journal.lemonde.fr'>,
    <Selector xpath='descendant-or-self::a/@href' data='/'>,
    <Selector xpath='descendant-or-self::a/@href' data='https://secure.lemonde.fr/sfuser/connexi'>,
    <Selector xpath='descendant-or-self::a/@href' data='https://abo.lemonde.fr/#xtor=CS1-454[CTA'>,
    <Selector xpath='descendant-or-self::a/@href' data='/'>,
    <Selector xpath='descendant-or-self::a/@href' data='/'>,
    <Selector xpath='descendant-or-self::a/@href' data='#'>,
    <Selector xpath='descendant-or-self::a/@href' data='/mouvement-des-gilets-jaunes/'>,
    <Selector xpath='descendant-or-self::a/@href' data='/carlos-ghosn/'>,
    <Selector xpath='descendant-or-self::a/@href' data='/implant-files/'>]
     
Comme vu précédemment, si on veut récupérer la liste des liens de la page on applique la méthode `extract()`
     
.. code-block:: Python

    In [11]: response.css('a::attr(href)').extract()[0:10]
    Out[11]:
    ['https://journal.lemonde.fr',
    '/',
    'https://secure.lemonde.fr/sfuser/connexion',
    'https://abo.lemonde.fr/#xtor=CS1-454[CTA_LMFR]-[HEADER]-5-[Home]',
    '/',
    '/',
    '#',
    '/mouvement-des-gilets-jaunes/',
    '/carlos-ghosn/',
    '/implant-files/']
     
Les liens dans une page HTML sont souvent codés de manière relative par rapport à la page courante. La méthode de l'objet ``Response`` peut être utilisée pour recréer l'url complet. 

Un exemple sur le 4e élément : 

.. code-block:: Python

    In [14]: response.urljoin(response.css('a::attr(href)').extract()[8])
    Out[14]: 'https://www.lemonde.fr/carlos-ghosn/'

alors que

.. code-block:: Python

    In [15]: response.css('a::attr(href)').extract()[8]
    Out[15]: '/carlos-ghosn/'
    
.. note:: Exercice :  Utiliser une liste compréhension pour transformer les 10 premiers liens relatifs récupérés par la méthode ``extract()`` en liens absolus.
    
Le résultat doit ressembler à : 

.. code-block:: Python

    Out[23]: 
    ['https://journal.lemonde.fr',
    'https://www.lemonde.fr/',
    'https://secure.lemonde.fr/sfuser/connexion',
    'https://abo.lemonde.fr/#xtor=CS1-454[CTA_LMFR]-[HEADER]-5-[Home]',
    'https://www.lemonde.fr/',
    'https://www.lemonde.fr/',
    'https://www.lemonde.fr/',
    'https://www.lemonde.fr/mouvement-des-gilets-jaunes/',
    'https://www.lemonde.fr/carlos-ghosn/',
    'https://www.lemonde.fr/implant-files/']
     
..  [response.urljoin(url) for url in response.css('a::attr(href)').extract()]

Des requêtes plus complexes
---------------------------

On peut créer des requêtes plus complexes en utilisant à la fois la structuration HTML du document mais également la couche de présentation CSS. On utilise l'inspecteur de ``Google Chrome`` pour identifier le type et l'identifiant de la balise contenant les informations.  

Il y a au moins deux choses à savoir en ``css`` :  

- Les ``.`` représentent les classes 
- Les ``#`` représentent les id


On se propose de récupérer toutes les sous-catégories de news dans la catégorie **Actualités**. On remarque en utilisant l'inspecteur d'élement de Chrome que toutes les catégories sont rangées dans une balise avec l'id `#nav-markup` ensuite dans les classes `Nav__item`.
        
A partir de cette structure HTML on peut construire la requête suivante pour récupérer la barre de navigation: 

.. code-block:: Python

    In [19]: response.css("#nav-markup")
    Out[19]: [<Selector xpath="descendant-or-self::*[@id = 'nav-markup']" data='<ul id="nav-markup"> <li class="Nav__ite'>]

Ensuite pour récupérer les différentes catégories : 

.. code-block:: Python

    In [24]: response.css("#nav-markup .Nav__item")
    Out[24]:
    [<Selector xpath="descendant-or-self::*[@id = 'nav-markup']/descendant-or-self::*/*[@class and contains(concat(' ', normalize-space(@class), ' '), ' Nav__item ')]" data='<li class="Nav__item js-burger-to-show N'>,
    <Selector xpath="descendant-or-self::*[@id = 'nav-markup']/descendant-or-self::*/*[@class and contains(concat(' ', normalize-space(@class), ' '), ' Nav__item ')]" data='<li class="Nav__item Nav__item--home Nav'>,
    <Selector xpath="descendant-or-self::*[@id = 'nav-markup']/descendant-or-self::*/*[@class and contains(concat(' ', normalize-space(@class), ' '), ' Nav__item ')]" data='<li class="Nav__item"> <a href="/" class'>,
    <Selector xpath="descendant-or-self::*[@id = 'nav-markup']/descendant-or-self::*/*[@class and contains(concat(' ', normalize-space(@class), ' '), ' Nav__item ')]" data='<li class="Nav__item"> <a href="#" class'>,
    <Selector xpath="descendant-or-self::*[@id = 'nav-markup']/descendant-or-self::*/*[@class and contains(concat(' ', normalize-space(@class), ' '), ' Nav__item ')]" data='<li class="Nav__item"> <a href="#" class'>,
    <Selector xpath="descendant-or-self::*[@id = 'nav-markup']/descendant-or-self::*/*[@class and contains(concat(' ', normalize-space(@class), ' '), ' Nav__item ')]" data='<li class="Nav__item"> <a href="#" class'>,
    <Selector xpath="descendant-or-self::*[@id = 'nav-markup']/descendant-or-self::*/*[@class and contains(concat(' ', normalize-space(@class), ' '), ' Nav__item ')]" data='<li class="Nav__item"> <a href="#" class'>,
    <Selector xpath="descendant-or-self::*[@id = 'nav-markup']/descendant-or-self::*/*[@class and contains(concat(' ', normalize-space(@class), ' '), ' Nav__item ')]" data='<li class="Nav__item"> <a href="#" class'>,
    <Selector xpath="descendant-or-self::*[@id = 'nav-markup']/descendant-or-self::*/*[@class and contains(concat(' ', normalize-space(@class), ' '), ' Nav__item ')]" data='<li class="Nav__item"> <a href="#" class'>,
    <Selector xpath="descendant-or-self::*[@id = 'nav-markup']/descendant-or-self::*/*[@class and contains(concat(' ', normalize-space(@class), ' '), ' Nav__item ')]" data='<li class="Nav__item"> <a href="#" class'>,
    <Selector xpath="descendant-or-self::*[@id = 'nav-markup']/descendant-or-self::*/*[@class and contains(concat(' ', normalize-space(@class), ' '), ' Nav__item ')]" data='<li class="Nav__item"> <a href="/recherc'>]


On veut maintenant retourner tous les liens présents dans cette catégorie. On remarque qu'elle apparait à la 4eme position. 

.. code-block:: Python

    In [34]: response.css("#nav-markup .Nav__item")[3]
    Out[34]: <Selector xpath="descendant-or-self::*[@id = 'nav-markup']/descendant-or-self::*/*[@class and contains(concat(' ', normalize-space(@class), ' '), ' Nav__item ')]" data='<li class="Nav__item"> <a href="#" class'>

Maintenant pour récupérer tous les liens on peut chainer les requêtes. On accède alors à toutes les balises `a`.


.. code-block:: Python

    In [35]: response.css("#nav-markup .Nav__item")[3].css("a")
    Out[35]:
    [<Selector xpath='descendant-or-self::a' data='<a href="#" class="js-dropdown Burger__r'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/mouvement-des-gilets-jaunes/" '>,
    <Selector xpath='descendant-or-self::a' data='<a href="/carlos-ghosn/" data-suggestion'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/implant-files/" data-suggestio'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/climat/" data-suggestion>Clima'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/affaire-khashoggi/" data-sugge'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/emmanuel-macron/" data-suggest'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/ukraine/" data-suggestion>Ukra'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/russie/" data-suggestion>Russi'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/referendum-sur-le-brexit/" dat'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/harcelement-sexuel/" data-sugg'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/actualite-en-continu/" data-su'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/international/">International<'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/politique/">Politique</a>'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/societe/">Société</a>'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/les-decodeurs/">Les Décodeurs<'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/sport/">Sport</a>'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/planete/">Planète</a>'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/sciences/">Sciences</a>'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/campus/">M Campus</a>'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/afrique/">Le Monde Afrique</a>'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/pixels/">Pixels</a>'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/actualite-medias/">Médias</a>'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/sante/">Santé</a>'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/big-browser/">Big Browser</a>'>,
    <Selector xpath='descendant-or-self::a' data='<a href="/disparitions/">Disparitions</a'>]

Et pour récupérer les titres : 

.. code-block:: Python 

    In [37]: response.css("#nav-markup .Nav__item")[3].css("a::text").extract()
    Out[37]:
    ['Actualités',
    'Mouvement des "gilets jaunes"',
    'Carlos Ghosn',
    'Implant Files',
    'Climat',
    'Affaire Khashoggi',
    'Emmanuel Macron',
    'Ukraine',
    'Russie',
    'Brexit',
    'Harcèlement sexuel',
    'Toute l’actualité en continu',
    'International',
    'Politique',
    'Société',
    'Les Décodeurs',
    'Sport',
    'Planète',
    'Sciences',
    'M Campus',
    'Le Monde Afrique',
    'Pixels',
    'Médias',
    'Santé',
    'Big Browser',
    'Disparitions']
     
Le shell Scrapy permet de définir la structure des requêtes et de s'assurer de la pertinence du résultat retourné.
Pour automatiser le processus, il faut intégrer cette syntaxe au code Python des modules de spider définis dans la structure du projet.

Intégration des requêtes
------------------------

Le squelette de la classe ``LeMondeSpider`` généré lors de la création du projet doit maintenant être enrichi. Par défaut 3 attributs et une méthode ``parse()`` ont été créés :

- ``name`` permet d'identifier sans ambiguïté la spider dans le code.
- ``allowed_domain`` permet de filtrer les requêtes et forcer la spider à rester sur une liste de domaines.
- ``starts_urls`` est la liste des urls d'où la spider va partir pour commencer son scraping.
- ``parse()`` est une méthode héritée de la classe ``scrapy.Spider``. Elle doit être redéfinie selon les requêtes que l'on doit effectuer et sera appelée sur l'ensemble des urls contenus dans la liste ``starts_urls``.

``parse()`` est une fonction ``callback`` qui sera appelée automatiquement sur chaque objet ``Response`` retourné par la requête. Cette fonction est appelée de manière asynchrone. Plusieurs requêtes peuvent ainsi être lancées en parallèles sans bloquer le thread principal.
L'objet ``Response`` passé en paramètre est le même que celui mis à disposition lors de l'exécution du Scrapy Shell.

.. code-block:: Python

    def parse(self, response):
        title = response.css('title::text').extract_first()
        all_links = {
            name:response.urljoin(url) for name, url in zip(
            response.css("#nav-markup .Nav__item")[3].css("a::text").extract(),
            response.css("#nav-markup .Nav__item")[3].css("a::attr(href)").extract())
        }
        yield {
            "title":title,
            "all_links":all_links
        }
        
La fonction est un générateur (``yield``) et retourne un dictionnaire composé de deux éléments : 

- Le titre de la page; 
- La liste des liens sortants sous forme de String.

Pour le moment cette spider ne parcourt que la page d'accueil, ce qui n'est pas très productif.


Votre premier scraper
---------------------

Récupérer les données sur un ensemble de pages webs nécessite d'explorer en profondeur la structure du site en suivant tout ou partie des liens rencontrés.

La spider peut se ``balader`` sur un site assez efficacement. Il suffit de lui indiquer comment faire. Il faut spécifier à Scrapy de générer une requête vers une nouvelle page en construisant l'objet ``Request`` correspondant. Ce nouvel objet ``Request`` est alors inséré dans le scheduler de Scrapy. On peut évidemment générer plusieurs ``Request`` simultanément, correspondant par exemple, à différents liens sur la page courante. Ils sont insérés séquentiellement dans le scheduler.

Pour cela on modifie la méthode ``parse()`` de façon à ce qu'elle retourne un objet ``Request`` pour chaque nouveau lien rencontré. On associe également à cet objet une fonction de callback qui déterminera la manière dont cette nouvelle page doit être extraite.

Par exemple, pour que la spider continue dans les liens des différentes régions (pour l'instant la fonction de callback ne fait rien) : 

.. code-block:: Python

    import scrapy
    from scrapy import Request


    
    class LemondeSpider(scrapy.Spider):
        name = "lemonde"
        allowed_domains = ["www.lemonde.fr"]
        start_urls = ['https://www.lemonde.fr']

        def parse(self, response):
            title = response.css('title::text').extract_first()
            all_links = {
                name:response.urljoin(url) for name, url in zip(
                response.css("#nav-markup .Nav__item")[3].css("a::text").extract(),
                response.css("#nav-markup .Nav__item")[3].css("a::attr(href)").extract())
            }
            yield {
                "title":title,
                "all_links":all_links
            }

            
On veut ensuite *entrer* dans les liens des différentes sous-catégories pour récupérer les articles. Pour cela, nous créons une méthode ``parse_category()`` prend en argument un objet ``Response`` qui sera la réponse correspondant aux liens des régions. On peut comme ceci traverser un site en définissant des méthodes différentes en fonction du type de contenu.

Si la structure du site est plus profonde, on peut empiler autant de couches que souhaité.
            
Quand on arrive sur une page d'une sous-catégorie, on peut vouloir récupérer tous les éléments de la page. Pour cela, on réutilise le scrapy Shell pour commencer le développement de la nouvelle méthode d'extraction.

Par exemple pour la page ``https://www.lemonde.fr/international/`` : 

.. code-block:: bash

    scrapy shell 'https://www.lemonde.fr/international/'
    
Le fil des articles est stocké dans une balise avec la classe `class=fleuve`.

.. code-block:: Python

    In [3]: response.css(".fleuve")
    Out[3]:
    [<Selector xpath="descendant-or-self::*[@class and contains(concat(' ', normalize-space(@class), ' '), ' fleuve ')]" data='<div class="fleuve">\n   <section>\n      '>,
    <Selector xpath="descendant-or-self::*[@class and contains(concat(' ', normalize-space(@class), ' '), ' fleuve ')]" data='<div class="fleuve">\n</div>'>]

Pour récupérer chacun des articles, il faut adresser les balises ``<article>`` contenues dans le sélecteur: 
    
.. code-block:: Python

    In [4]: response.css(".fleuve")[0].css("article")
    Out[4]:
    [<Selector xpath='descendant-or-self::article' data='<article class="grid_12 alpha enrichi mg'>,
    <Selector xpath='descendant-or-self::article' data='<article class="grid_12 alpha enrichi">\n'>,
    <Selector xpath='descendant-or-self::article' data='<article class="grid_12 alpha enrichi">\n'>,
    <Selector xpath='descendant-or-self::article' data='<article class="grid_12 alpha enrichi">\n'>,
    <Selector xpath='descendant-or-self::article' data='<article class="grid_12 alpha enrichi">\n'>,
    <Selector xpath='descendant-or-self::article' data='<article class="grid_12 alpha enrichi">\n'>,
    <Selector xpath='descendant-or-self::article' data='<article class="grid_12 alpha enrichi">\n'>,
    <Selector xpath='descendant-or-self::article' data='<article class="grid_12 alpha enrichi">\n'>]   

Comme précédemment, on peut empiler les sélecteurs ``css`` pour créer des requêtes plus complexes.

Par exemple, pour récupérer tous les titres des différents articles :

.. code-block:: Python

    In [8]: response.css(".fleuve")[0].css("article h3 a::text").extract()
    Out[8]:
    ['Des dizaines de milliers de Géorgiens contestent dans la rue l’élection de Salomé Zourabichvili\r\n\r\n\r\n',
    'A Budapest en Hongrie, un îlot décroissant pour favoriser la transition\r\n\r\n\r\n',
    'En Israël, la police recommande l’inculpation de Nétanyahou dans une troisième enquête\r\n\r\n\r\n',
    'Donald Trump veut «\xa0mettre fin\xa0» à l’Aléna rapidement\r\n\r\n\r\n',
    'Le cauchemar de la «\xa0rééducation\xa0» des musulmans en Chine\r\n\r\n',
    '\r\n',
    '«\xa0AMLO\xa0» lance sa transformation du Mexique\r\n\r\n\r\n',
    '«\xa0Paris brûle\xa0»\xa0: les médias étrangers relatent le «\xa0chaos\xa0» en marge des défilés des «\xa0gilets jaunes\xa0»\r\n\r\n\r\n',
    'Andrés Manuel Lopez Obrador intronisé président du Mexique\r\n\r\n\r\n']

En HTML les données sont souvent de très mauvaise qualité. Il faut définir des méthodes permettant de les nettoyer pour être intégrées dans des bases de données.

Par exemple, pour supprimer tous les espaces superflus : 

.. code-block:: Python

    In [13]: def clean_spaces(string_):
    ...:        if string_ is not None: 
    ...:            return " ".join(string_.split())
        

Pour l'appliquer à tous les titres récupérés, on peut faire une list comprehension : 
.. code-block:: Python

    In [11]: [clean_spaces(article) for article in response.css(".fleuve")[0].css("article h3 a::text").extract()]
    Out[11]:
    ['Des dizaines de milliers de Géorgiens contestent dans la rue l’élection de Salomé Zourabichvili',
    'A Budapest en Hongrie, un îlot décroissant pour favoriser la transition',
    'En Israël, la police recommande l’inculpation de Nétanyahou dans une troisième enquête',
    'Donald Trump veut « mettre fin » à l’Aléna rapidement',
    'Le cauchemar de la « rééducation » des musulmans en Chine',
    '',
    '« AMLO » lance sa transformation du Mexique',
    '« Paris brûle » : les médias étrangers relatent le « chaos » en marge des défilés des « gilets jaunes »',
    'Andrés Manuel Lopez Obrador intronisé président du Mexique']
        
La méthode précédente est intéressante si l'on ne recherche qu'une seule information par article.
     
Par contre si l'on veut récupérer d'autres caractéristiques comme l'image ou la description par exemple, il est plus intéressant et plus efficace de récupérer l'objet et d'effectuer plusieurs traitements sur ce dernier.

Chaque objet retourné par les requêtes ``css`` est un selecteur avec lequel on peut interagir.

Par exemple pour récupérer le titre et le prix 

.. code-block:: Python

    In [25]: for article in response.css(".fleuve")[0].css("article"):
    ...:     title = clean_spaces(article.css("h3 a::text").extract_first())
    ...:     image = article.css("img::attr(data-src)").extract_first()
    ...:     description = article.css(".txt3::text").extract_first()
    ...:     print(f"Title {title} \nImage {image}\nDescription {description}\n ----")

    Title Des dizaines de milliers de Géorgiens contestent dans la rue l’élection de Salomé Zourabichvili
    Image https://s1.lemde.fr/image/2018/12/02/147x97/5391641_7_5874_les-partisans-de-l-opposant-grigol-vashadze_20d2e8693a49b83fd3c5578f7799ae9c.jpg
    Description Elue présidente (un rôle essentiellement symbolique en Géorgie), l’ex-diplomate française, candidate du pouvoir, est contestée par l’opposition.
    ----
    Title A Budapest en Hongrie, un îlot décroissant pour favoriser la transition
    Image https://img.lemde.fr/2018/12/01/10/0/4214/2809/147/97/60/0/15b32ca_1EY4qISQ_BP4kPAh1fozJdXZ.jpg
    Description Le centre logistique Cargonomia sert de matrice aux coopératives de l’économie durable et solidaire hongroise.
    ----
    Title En Israël, la police recommande l’inculpation de Nétanyahou dans une troisième enquête
    Image https://img.lemde.fr/2018/12/02/167/0/4207/2804/147/97/60/0/9e02c9b_3580d043ebc94b48b0f2cfef4e9a21e7-3580d043ebc94b48b0f2cfef4e9a21e7-0.jpg
    Description Le premier ministre est soupçonné de corruption, fraude et abus de pouvoir, dans une affaire impliquant le groupe de télécoms israélien Bezeq.
    ----
    Title Donald Trump veut « mettre fin » à l’Aléna rapidement
    Image https://img.lemde.fr/2018/11/30/0/0/4861/3240/147/97/60/0/8b87184_5826023-01-06.jpg
    Description Le président américain souhaite voir disparaître l’accord de libre-échange remontant à 1994 avec le Mexique et le Canada, qu’il qualifie régulièrement de « pire accord jamais signé », en faveur du nouveau traité négocié difficilement avec ses voisins nord-américains ces derniers mois.
    ----
    Title Le cauchemar de la « rééducation » des musulmans en Chine
    Image https://img.lemde.fr/2018/11/15/151/0/5000/3333/147/97/60/0/118c78f_248b226e6b91450aa8a68bd0ea5525a8-248b226e6b91450aa8a68bd0ea5525a8-0.jpg
    Description Ouïgours et Kazakhs du Xinjiang... C’est toute une population musulmane que Pékin veut « rééduquer » en internant des centaines de milliers d’entre eux dans des camps.
    ----
    Title « AMLO » lance sa transformation du Mexique
    Image https://img.lemde.fr/2018/12/02/45/0/1497/998/147/97/60/0/a33c174_GGGTBR84_MEXICO-POLITICS-_1202_11.JPG
    Description Education et santé gratuites, hausse du salaire minimum, bourses scolaires : à peine investi, le président Andres Manuel Lopez Obrador a listé les mesures qu’il entend prendre pour redresser le pays.
    ----
    Title « Paris brûle » : les médias étrangers relatent le « chaos » en marge des défilés des « gilets jaunes »
    Image https://img.lemde.fr/2018/12/02/361/0/598/396/147/97/60/0/ba46a6e_XVIt1Ffwm50iYBheccVieUQQ.jpg
    Description Les images de destructions, d’échauffourées ou de voitures enflammées s’affichaient samedi soir en « une » de nombreux sites d’actualité internationaux.
    ----
    Title Andrés Manuel Lopez Obrador intronisé président du Mexique
    Image https://img.lemde.fr/2018/12/02/91/145/1346/897/147/97/60/0/877cd51_a4618baa8da2414bb62bab28a6d4c745-a4618baa8da2414bb62bab28a6d4c745-0.jpg
    Description Le nouveau chef d’Etat a promis de lutter contre la corruption en menant une transformation « profonde et radicale » du pays.
    ----
    
Persistence des données
-----------------------
    
Pour pouvoir stocker les informations que l'on récupère en parcourant un site il faut pouvoir les stocker. On utilise soit de simples dictionnaires Python, ou mieux des ``scrapy.Item`` qui sont des dictionnaires améliorés. 

Nous allons voir les deux façons de faire. On peut réécrire la méthode ``parse_category()`` pour lui faire retourner un dictionnaire correspondant à chaque offre rencontrée.

.. code-block:: Python

    def parse_category(self, response):
        for article in response.css(".fleuve")[0].css("article"):
            title = self.clean_spaces(article.css("h3 a::text").extract_first())
            image = article.css("img::attr(data-src)").extract_first()
            description = article.css(".txt3::text").extract_first()
            yield {
                "title":title,
                "image":image,
                "description":description
            }

            
Si on combine tout dans la spider : 

.. code-block:: Python

    import scrapy
    from scrapy import Request


    class LemondeSpider(scrapy.Spider):
        name = "lemonde"
        allowed_domains = ["www.lemonde.fr"]
        start_urls = ['https://www.lemonde.fr']

        def parse(self, response):
            title = response.css('title::text').extract_first()
            all_links = {
                name:response.urljoin(url) for name, url in zip(
                response.css("#nav-markup .Nav__item")[3].css("a::text").extract(),
                response.css("#nav-markup .Nav__item")[3].css("a::attr(href)").extract())
            }
            for link in all_links.values():
                yield Request(link, callback=self.parse_category)

        def parse_category(self, response):
            for article in response.css(".fleuve")[0].css("article"):
                title = self.clean_spaces(article.css("h3 a::text").extract_first())
                image = article.css("img::attr(data-src)").extract_first()
                description = article.css(".txt3::text").extract_first()
                yield {
                    "title":title,
                    "image":image,
                    "description":description
                }


        def clean_spaces(self, string):
            if string:
                return " ".join(string.split())
                
On peut maintenant lancer notre spider avec la commande suivante : 

.. code-block:: bash

    scrapy crawl <NAME>
    
``scrapy crawl`` permet de démarrer le processus en allant chercher la classe ``scrapy.Spider`` dont l'attribut ``name``  = <NAME>.

Par exemple, pour la spider ``LeMondeSpider`` : 

.. code-block:: bash

    scrapy crawl lemonde
    
    {'title': '« Gilets jaunes » : « La question n’est plus la crise écologique. Elle est de sortir au plus vite de la violence »', 'image': 'https://img.lemde.fr/2018/12/01/0/0/1999/1333/147/97/60/0/bd07906_oYK0XUhof1ma2smWloAu1mbd.jpg', 'description': 'L’exécutif n’est pas assuré de pouvoir maintenir la sécurité et l’ordre en cas de quatrième week-end de mobilisation, estime l’éditorialiste au «\xa0Monde\xa0» Françoise Fressoz, au soir d’une journée d’émeutes dans Paris, samedi.'}
    2018-12-02 17:10:03 [scrapy.core.scraper] DEBUG: Scraped from <200 https://www.lemonde.fr/mouvement-des-gilets-jaunes/>
    {'title': '« Gilets jaunes » : Emmanuel Macron réagit après les violences à Paris', 'image': 'https://img.lemde.fr/2018/12/01/0/4/4920/3280/147/97/60/0/9202b53_91f4a2b01be642658d32730018fbb799-91f4a2b01be642658d32730018fbb799-0.jpg', 'description': 'Emmanuel Macron a condamné les violences survenues en marge des rassemblements des «\xa0gilets jaunes\xa0», samedi 1er janvier à Paris.'}
    2018-12-02 17:10:03 [scrapy.core.scraper] DEBUG: Scraped from <200 https://www.lemonde.fr/mouvement-des-gilets-jaunes/>
    {'title': '« Gilets jaunes » à Lille : « Ils veulent nous laminer, mais aujourd’hui, toute notre colère ressort »', 'image': 'https://img.lemde.fr/2018/12/01/32/0/4323/2879/147/97/60/0/9b3842c_b_34XdIsl-E7T-GBIHr9Vgr8.jpg', 'description': 'Près de 2\xa0500\xa0personnes, selon les organisateurs, ont manifesté à Lille, sans qu’aucun incident n’ait été signalé.'}
    2018-12-02 17:10:03 [scrapy.core.scraper] DEBUG: Scraped from <200 https://www.lemonde.fr/mouvement-des-gilets-jaunes/>
    {'title': '« Gilets jaunes » : « Les stations-service de certains territoires ruraux doivent être dispensées de la taxe carbone »', 'image': 'https://img.lemde.fr/2018/11/28/118/0/5184/3452/147/97/60/0/84b3ae3_ebokcanGhRHtcS5n75IAdwfr.JPG', 'description': 'Dans une tribune au «\xa0Monde\xa0», l’économiste Alain Trannoy préconise, en attendant le déploiement d’une véritable alternative électrique sur tout le territoire, de supprimer la taxe dans les zones où la mobilité est contrainte.'}
    2018-12-02 17:10:03 [scrapy.core.scraper] DEBUG: Scraped from <200 https://www.lemonde.fr/mouvement-des-gilets-jaunes/>
    {'title': 'La journée de mobilisation des « gilets jaunes » en images', 'image': 'https://img.lemde.fr/2018/12/01/0/0/5949/3966/147/97/60/0/fe11fe3_7pHsoBoJhcKJfFDcSyWF5XEV.jpg', 'description': 'A Paris et province, des «\xa0gilets jaunes\xa0» se sont de nouveau réunis samedi. La journée a été marquée par de graves violences, notamment dans la capitale.'}
    2018-12-02 17:10:03 [scrapy.core.scraper] DEBUG: Scraped from <200 https://www.lemonde.fr/mouvement-des-gilets-jaunes/>
    {'title': '« Gilets jaunes » : les images des violences au cœur de Paris', 'image': 'https://img.lemde.fr/2018/12/01/0/0/4372/2914/147/97/60/0/7e8cfdd_5833490-01-06.jpg', 'description': 'Magasins pillés, voitures incendiées, bâtiments attaqués… les affrontements entre «\xa0gilets jaunes\xa0» et forces de l’ordre ont fait plus d’une centaine de blessés.'}
    2018-12-02 17:10:03 [scrapy.core.scraper] DEBUG: Scraped from <200 https://www.lemonde.fr/mouvement-des-gilets-jaunes/>
    {'title': 'Près de l’Arc de triomphe, les doléances des « gilets jaunes » recouvertes par le bruit des émeutes', 'image': 'https://img.lemde.fr/2018/12/01/0/0/1620/1080/147/97/60/0/6eee987_wvZ85RkQO3Q7OVvF7msFvvkS.jpg', 'description': 'Toute la journée, les manifestants les plus virulents et les forces de l’ordre se sont disputé le contrôle des avenues autour de la place de l’Etoile.'}
    2018-12-02 17:10:03 [scrapy.core.scraper] DEBUG: Scraped from <200 https://www.lemonde.fr/implant-files/>
    {'title': 'Implants médicaux : « Je suis une miraculée mais j’ai vécu sept ans de calvaire »', 'image': 'https://img.lemde.fr/2018/11/22/0/0/2899/1933/147/97/60/0/91a79f9_dwNEK3IQwvsEEpgllltYxA47.jpg', 'description': 'Douleurs insupportables, manque de réaction et d’information de la part de médecins, explantation difficile… Trois femmes témoignent des conséquences de la pose d’un dispositif médical dans leur corps.'}
    
On peut exporter les résultats de ces retours dans différents formats de fichiers. 

- CSV : `scrapy crawl lemonde -o lbc.csv`
- JSON : `scrapy crawl lemonde -o lbc.json`
- JSONLINE : `scrapy crawl lemonde -o lbc.jl`
- XML : `scrapy crawl lemonde -o lbc.xml`

.. note:: Exercice : Exécuter la spider avec les différents formats de stockage. Explorer ensuite le contenu des fichiers ainsi créés.

Votre premier Item
------------------

La classe ``Item`` permet de structurer les données que l'on souhaite récupérer sous la forme d'un modèle. Les items doivent être définis dans le fichier ``items.py`` créé par la commande ``scrapy startproject``. Les ``Item`` héritent de la class ``scrapy.Item``.

On veut structurer les données avec deux champs : le titre et le prix de l'annonce. Scrapy utilise une classe ``scrapy.Field`` permettant de 'déclarer' ces champs. Dans notre cas : 

.. code-block:: Python

    import scrapy

    class ArticleItem(scrapy.Item):
        title = scrapy.Field()
        image = scrapy.Field()
        description = scrapy.Field()
        
    
        
Utiliser la classe ``scrapy.Item`` plutôt qu'un simple dictionnaire permet plus de contrôle sur la structure des données. En effet, on ne peut insérer dans les items que des données avec des clés 'déclarées'. Ce qui assure une plus grande cohérence au sein d'un projet. 

On peut instancier un item de plusieurs façons : 

.. code-block:: Python

    In [4]: article_item = ArticleItem(title="Gilets Jaunes", image=None, description="Un samedi de manifestations")

    In [5]: print(article_item)
    {'description': 'Un samedi de manifestations',
    'image': None,
    'title': 'Gilets Jaunes'}

    
.. code-block:: Python

    In [9]: article_item = ArticleItem()
        ...: article_item["title"] = 'Gilets Jaunes'
        ...: article_item["description"] = 'Un samedi de manifestations'
        ...:

    In [10]: print(article_item)
    {'description': 'Un samedi de manifestations', 'title': 'Gilets Jaunes'}
    
La définition d'un item permet de palier toutes les erreurs de typo dans les champs.

.. code-block:: Python

    In [11]: article_item = ArticleItem()
        ...: article_item["titel"] = 'Gilets Jaunes'
        ...:
    ---------------------------------------------------------------------------
    KeyError                                  Traceback (most recent call last)
    <ipython-input-11-de371261a7a5> in <module>()
        1 article_item = ArticleItem()
    ----> 2 article_item["titel"] = 'Gilets Jaunes'

    ~/anaconda3/lib/python3.6/site-packages/Scrapy-1.3.3-py3.6.egg/scrapy/item.py in __setitem__(self, key, value)
        64         else:
        65             raise KeyError("%s does not support field: %s" %
    ---> 66                 (self.__class__.__name__, key))
        67
        68     def __delitem__(self, key):

KeyError: 'ArticleItem does not support field: titel'


Les items héritent des dictionnaires Python, et possèdent donc toutes les méthodes de ceux-ci: 

.. code-block:: Python

    In [13]: article_item = ArticleItem(title="Gilets Jaunes")
        ...: print(article_item["title"]) # Méthode __getitem__()
        ...: print(article_item.get("description", "no description")) # Méthode get()
        ...:
    Gilets Jaunes
    no description

On peut transformer un ``Item`` en dictionnaire très facilement, en le passant au constructeur:

.. code-block:: Python

    article_item = ArticleItem(title="Drone DJI")
    print(type(article_item))
    dict_item = dict(article_item)
    print(type(dict_item))
    print(dict_item)
    
    <class '__main__.ArticleItem'>
    <class 'dict'>
    {'title': 'Drone DJI'}
    
On intègre maintenant cet item dans notre spider.

.. code-block:: Python

    # -*- coding: utf-8 -*-
    import scrapy
    from scrapy import Request
    from ..items import ArticleItem
    class LemondeSpider(scrapy.Spider):
        name = "lemonde"
        allowed_domains = ["www.lemonde.fr"]
        start_urls = ['https://www.lemonde.fr']

        def parse(self, response):
            title = response.css('title::text').extract_first()
            all_links = {
                name:response.urljoin(url) for name, url in zip(
                response.css("#nav-markup .Nav__item")[3].css("a::text").extract(),
                response.css("#nav-markup .Nav__item")[3].css("a::attr(href)").extract())
            }
            for link in all_links.values():
                yield Request(link, callback=self.parse_category)

        def parse_category(self, response):
            for article in response.css(".fleuve")[0].css("article"):
                title = self.clean_spaces(article.css("h3 a::text").extract_first())
                image = article.css("img::attr(data-src)").extract_first()
                description = article.css(".txt3::text").extract_first()
                #yield {
                #    "title":title,
                #    "image":image,
                #    "description":description
                #}

                yield ArticleItem(
                    title=title,
                    image=image,
                    description=description
                )

        def clean_spaces(self, string):
            if string:
                return " ".join(string.split())
                
                
 On voit bien que le générateur retourne maintenant un ``Item``.
 
 .. note:: Exercice : 
 
 Relancer la spider pour vérifier le bon déroulement de l'extraction.
 

Postprocessing
--------------

Si l'on se réfère au diagramme d'architecture de Scrapy, on voit qu'il est possible d'insérer des composants suplémentaires dans le flux de traitement. Ces composants s'appellent ``Pipelines``. 

Par défaut, tous les ``Item`` générés au sein d'un projet Scrapy passent par les ``Pipelines``. Les pipelines sont utilisées la plupart du temps pour : 

- Nettoyer du contenu HTML ;
- Valider les données scrapées ; 
- Supprimer les items qu'on ne souhaite pas stocker ;
- Stocker ces objets dans des bases de données.

Les pipelines doivent être définis dans le fichier ``pipelines.py``.

Dans notre cas on peut vouloir nettoyer le champ ``title`` pour enlever les caractères supperflus.

Nous allons alors transferer la fonction de nettoyage du code html dans une Pipeline. 

.. code-block:: Python

    from scrapy.exceptions import DropItem

    class TextPipeline(object):

        def process_item(self, item, spider):
            if item['title']:
                item["title"] = clean_spaces(item["title"])
                return item
            else:
                raise DropItem("Missing title in %s" % item)


    def clean_spaces(string):
        if string:
            return " ".join(string.split())


Pour dire au process Scrapy de faire transiter les items par ces pipelines. Il faut le spécifier dans le fichier de paramétrage ``settings.py``.

.. code-block:: Python

   ITEM_PIPELINES = {
        'newscrawler.pipelines.TextPipeline': 300,
    }

    
On peut maintenant supprimer la fonction `clean_spaces()` de l'extraction des données et laisser la Pipeline faire son travail. 
La valeur entière définie permet de déterminer l'ordre dans lequel les pipelines vont être appelées. Ces entiers peuvent être entre compris 0 et 1000.

On relance notre spider : 

.. code-block:: bash

    scrapy crawl lemonde -o ../data/articles.json
    
On peut aussi utiliser les Pipelines pour stocker les données récupérées dans une base de données. Pour stocker les items dans des documents mongo. 

.. code-block:: Python

    import pymongo

    class MongoPipeline(object):

        collection_name = 'scrapy_items'

        def open_spider(self, spider):
            self.client = pymongo.MongoClient()
            self.db = self.client["lemonde"]

        def close_spider(self, spider):
            self.client.close()

        def process_item(self, item, spider):
            self.db[self.collection_name].insert_one(dict(item))
            return item
            
Ici redéfini deux autres méthodes:  ``open_spider()``et ``close_spider()``, ces méthode sont appelés comme leurs noms l'indiquent elles sont appelées lorsque la Spider est instanciée et fermée. 

Ces méthodes nous permettent d'ouvrir la connexion Mongo et de la fermer lorsque le scraping se termine. La méthode ``process_item()`` est appelé à chaque fois qu'un item passe dans le mécanisme interne de scrapy. Ici, la méthode permet d'insérer l'item en tant que document mongo. 

Pour que cette pipeline soit appelé il faut l'ajouter dans les settings du projet.


.. code-block:: Python

    ITEM_PIPELINES = {
        'newscrawler.pipelines.TextPipeline': 100,
        'newscrawler.pipelines.MongoPipeline': 300
    }
    
La pipeline est ajoutée à la fin du process pour profiter des deux précédantes.
    
Settings
--------

Scrapy permet de gérer le comportement des spiders avec certains paramètres. Comme expliqué dans le premier cours, il est important de suivre des règles en respectant les différents site. Il existe énormément de paramètres mais nous allons (dans le cadre de ce cours) aborder les plus utilisés : 

- DOWNLOAD_DELAY : Le temps de téléchrgement entre chaque requête sur le même domaine ;
- CONCURRENT_REQUESTS_PER_DOMAIN : Nombre de requêtes simultanées par domaine ;
- CONCURRENT_REQUESTS_PER_IP : Nombre de requêtes simultanées par IP ;
- DEFAULT_REQUEST_HEADERS : Headers HTTP utilisé pour les requêtes ;
- ROBOTSTXT_OBEY : Scrapy récupère le robots.txt et adapte le scraping en fonction des règles trouvées ;
- USER_AGENT : UserAgent utilisé pour faire les requêtes ;
- BOT_NAME : Nom du bot annoncé lors des requêtes
- HTTPCACHE_ENABLED : Utilisation du cache HTTP, utile lors du parcours multiple de la même page.

Le fichiers settings.py permet de définir les paramètres globaux d'un projet. Si votre projet contient un grand nombre de spiders il peut être intéressant d'avoir des paramètres distincts pour chaque spider. Un moyen simple est d'ajouter un attribut ``custom_settings`` à votre spider :

.. code-block:: Python

    class LeMondeSpider(scrapy.Spider):
            name = "lemonde"
            allowed_domains = ["lemonde.fr"]
            start_urls = ['http://lemonde.fr/']
            custom_settings = {
                "HTTPCACHE_ENABLED":True, 
                "CONCURRENT_REQUESTS_PER_DOMAIN":100
            }

