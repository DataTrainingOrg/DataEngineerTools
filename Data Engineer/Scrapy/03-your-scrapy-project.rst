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

Pour créer une Spider : 

.. code-block:: bash

    cd monprojet
    scrapy genspider leboncoin leboncoin.fr
    
Cette commande permet de créer une spider appelée leboncoin pour scraper le domaine leboncoin.fr. Cela créé un fichier Python :

.. code-block:: Python

    import scrapy


    class LeboncoinSpider(scrapy.Spider):
        name = "leboncoin"
        allowed_domains = ["leboncoin.fr"]
        start_urls = ['http://leboncoin.fr/']

        def parse(self, response):
            pass
            

Une bonne pratique pour commencer à développer une Spider est de passer par l'interface Shell proposée par Scrapy. Elle permet de récupérer un objet response et de tester les méthodes de récupérations.
 
 
 .. code-block:: bash
    
    scrapy shell 'http://leboncoin.fr'
    
Scrapy lance un kernel Python 

    2018-02-08 11:28:47 [scrapy.utils.log] INFO: Scrapy 1.3.3 started (bot: monprojet)
    2018-02-08 11:28:47 [scrapy.utils.log] INFO: Overridden settings: {'BOT_NAME': 'monprojet', 'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter', 'LOGSTATS_INTERVAL': 0, 'NEWSPIDER_MODULE': 'monprojet.spiders', 'ROBOTSTXT_OBEY': True, 'SPIDER_MODULES': ['monprojet.spiders']}
    2018-02-08 11:28:47 [scrapy.middleware] INFO: Enabled extensions:
    ['scrapy.extensions.corestats.CoreStats',
     'scrapy.extensions.telnet.TelnetConsole']
    2018-02-08 11:28:47 [scrapy.middleware] INFO: Enabled downloader middlewares:
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
    2018-02-08 11:28:47 [scrapy.middleware] INFO: Enabled spider middlewares:
    ['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
     'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',
     'scrapy.spidermiddlewares.referer.RefererMiddleware',
     'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
     'scrapy.spidermiddlewares.depth.DepthMiddleware']
    2018-02-08 11:28:47 [scrapy.middleware] INFO: Enabled item pipelines:
    []
    2018-02-08 11:28:47 [scrapy.extensions.telnet] DEBUG: Telnet console listening on 127.0.0.1:6023
    2018-02-08 11:28:47 [scrapy.core.engine] INFO: Spider opened
    2018-02-08 11:28:47 [scrapy.downloadermiddlewares.redirect] DEBUG: Redirecting (301) to <GET https://www.leboncoin.fr/robots.txt> from <GET https://leboncoin.fr/robots.txt>
    2018-02-08 11:28:47 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://www.leboncoin.fr/robots.txt> (referer: None)
    2018-02-08 11:28:47 [scrapy.downloadermiddlewares.redirect] DEBUG: Redirecting (301) to <GET https://www.leboncoin.fr/> from <GET https://leboncoin.fr>
    2018-02-08 11:28:47 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://www.leboncoin.fr/robots.txt> (referer: None)
    2018-02-08 11:28:47 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://www.leboncoin.fr/> (referer: None)
    2018-02-08 11:28:49 [traitlets] DEBUG: Using default logger
    2018-02-08 11:28:49 [traitlets] DEBUG: Using default logger
    [s] Available Scrapy objects:
    [s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
    [s]   crawler    <scrapy.crawler.Crawler object at 0x11035dc50>
    [s]   item       {}
    [s]   request    <GET https://leboncoin.fr>
    [s]   response   <200 https://www.leboncoin.fr/>
    [s]   settings   <scrapy.settings.Settings object at 0x1148e4ef0>
    [s]   spider     <LeboncoinSpider 'leboncoin' at 0x114b83080>
    [s] Useful shortcuts:
    [s]   fetch(url[, redirect=True]) Fetch URL and update local objects (by default, redirects are followed)
    [s]   fetch(req)                  Fetch a scrapy.Request and update local objects 
    [s]   shelp()           Shell help (print this help)
    [s]   view(response)    View response in a browser
    
Grace à cette interface vous avec accès à plusieurs objets comme la response, la request  la spider par exemple. Vous pouvez aussi exécuter `view(response)` pour afficher ce que Scrapy récupère dans un navigateur.

On peut commencer à regarder comment extraire les données en utilisant le langage de requêtes proposé par Scrapy. Il existe deux types de requêtes les requêtes `css` et `xpath`. Les requêtes xpath sont plus complexes mais plus puissante que les requêtes `css`. Dans le cadre de ce tutorial nous allons uniquement aborder les requêtes `css`, elles nous suffirons pour extraire les données dont avons besoin.

Que ce soit les requêtes `css` ou `xpath` crééent des sélecteurs de différents types. Nous pouvons commencer à faire quelques requêtes.

Pour récupérer le titre d'une page : 

.. code-block:: Python

    In [1]: response.css('title')
    Out[1]: [<Selector xpath='descendant-or-self::title' data='<title>\n\n\t\tleboncoin, site de petites an'>]
    
On récupère une liste de sélecteurs correspondant à la requête. Si on utilise une requête moins restrictive : 

.. code-block:: Python

    In [2]: response.css('a')
    Out[2]: 
    [<Selector xpath='descendant-or-self::a' data='<a href="" title="Fermer le menu" class='>,
     <Selector xpath='descendant-or-self::a' data='<a id="appRedirect" target="_blank" clas'>,
     <Selector xpath='descendant-or-self::a' data='<a class="displayMenu button-white-mobil'>,
     <Selector xpath='descendant-or-self::a' data='<a href="//www.leboncoin.fr/" class="log'>,
     <Selector xpath='descendant-or-self::a' data='<a href="" class="logo-site trackable cu'>,
     <Selector xpath='descendant-or-self::a' data='<a href="//www.leboncoin.fr/" title="Acc'>,
     <Selector xpath='descendant-or-self::a' data='<a href="//www.leboncoin.fr/ai?ca=12_s" '>, ... ]
    
Pour récupérer le texte d'une balise : 
    
.. code-block:: Python

    In [3]: response.css('title::text')
    Out[3]: [<Selector xpath='descendant-or-self::title/text()' data='\n\n\t\tleboncoin, site de petites annonces '>]
    
    
Maintenant pour extraire les données des selecteurs on utilise deux méthodes `extract()` qui permet de récupérer une liste des données extraites de tous les selecteurs et `extract_first()` permet de récupérer une string provenant du premier.

.. code-block:: Python

    In [4]: response.css('title::text').extract_first()
    Out[4]: '\n\n\t\tleboncoin, site de petites annonces gratuites\n\n'
    
On peut maintenant vouloir récupérer un attribut d'un balise. Par exemple, les liens sont contenu dans un attribut `href`.

.. code-block:: Python

    In [5]: response.css('a::attr(href)')
    Out[5]: 
    [<Selector xpath='descendant-or-self::a/@href' data=''>,
     <Selector xpath='descendant-or-self::a/@href' data='//www.leboncoin.fr/'>,
     <Selector xpath='descendant-or-self::a/@href' data=''>,
     <Selector xpath='descendant-or-self::a/@href' data='//www.leboncoin.fr/'>,
     <Selector xpath='descendant-or-self::a/@href' data='//www.leboncoin.fr/ai?ca=12_s'>,
     <Selector xpath='descendant-or-self::a/@href' data='//www.leboncoin.fr/annonces/offres'>,
     <Selector xpath='descendant-or-self::a/@href' data='//www.leboncoin.fr/annonces/demandes'>,
     <Selector xpath='descendant-or-self::a/@href' data='//www.leboncoin.fr/aw?ca=12_s'>,
     <Selector xpath='descendant-or-self::a/@href' data='//www.leboncoin.fr/aw?ca=12_s&selected=b'>,
     <Selector xpath='descendant-or-self::a/@href' data='//www.leboncoin.fr/aw?ca=12_s&selected=s'>,
     <Selector xpath='descendant-or-self::a/@href' data='//www.leboncoin.fr/boutiques/tout_secteu'>,
     <Selector xpath='descendant-or-self::a/@href' data=''>,
     <Selector xpath='descendant-or-self::a/@href' data=''>,
     <Selector xpath='descendant-or-self::a/@href' data='https://corporate.leboncoin.fr/'>,
     <Selector xpath='descendant-or-self::a/@href' data='//www.leboncoin.fr/recrutement.htm?ca=12'>,
     <Selector xpath='descendant-or-self::a/@href' data='http://secondhandeffect.leboncoin.fr/'>,
     <Selector xpath='descendant-or-self::a/@href' data='//www.leboncoin.fr/legal.htm?ca=12_s'>,
     <Selector xpath='descendant-or-self::a/@href' data='//www.leboncoin.fr/regles.htm?ca=12_s'>,
     <Selector xpath='descendant-or-self::a/@href' data='//www.leboncoin.fr/cgv_general.htm?ca=12'>,
     <Selector xpath='descendant-or-self::a/@href' data='//www.leboncoin.fr/cookies/'>,
     <Selector xpath='descendant-or-self::a/@href' data='//www2.leboncoin.fr/pub/form/?ca=12_s'>,
     <Selector xpath='descendant-or-self::a/@href' data='//www2.leboncoin.fr/dc/vos_droits_et_obl'>,
     <Selector xpath='descendant-or-self::a/@href' data='https://comptepro.leboncoin.fr/immobilie'>,
     <Selector xpath='descendant-or-self::a/@href' data='//www.leboncoin.fr/vos-recrutements'>,...]
     
Si on veut récupérer la liste des liens de la page on applique la méthode `extract()`
     
 .. code-block:: Python

    In [18]: response.css('a::attr(href)').extract()
    Out[18]: 
    ['',
     '//www.leboncoin.fr/',
     '',
     '//www.leboncoin.fr/',
     '//www.leboncoin.fr/ai?ca=12_s',
     '//www.leboncoin.fr/annonces/offres',
     '//www.leboncoin.fr/annonces/demandes',
     '//www.leboncoin.fr/aw?ca=12_s',
     '//www.leboncoin.fr/aw?ca=12_s&selected=backup',
     '//www.leboncoin.fr/aw?ca=12_s&selected=search',
     '//www.leboncoin.fr/boutiques/tout_secteur_d_activite/toutes_categories/ile_de_france/',
     '',
     '',
     'https://corporate.leboncoin.fr/',
     '//www.leboncoin.fr/recrutement.htm?ca=12_s&c=0&w=3',
     'http://secondhandeffect.leboncoin.fr/',
     '//www.leboncoin.fr/legal.htm?ca=12_s',
     '//www.leboncoin.fr/regles.htm?ca=12_s',
     '//www.leboncoin.fr/cgv_general.htm?ca=12_s',
     '//www.leboncoin.fr/cookies/',...]
     
Les liens dans une page HTML sont souvent codés de manière relative par rapport à la page courante. L'objet response peut être utilisé pour recréé l'url complet. 

Un exemple sur le 4e élément : 

 .. code-block:: Python

    In [22]: response.urljoin(response.css('a::attr(href)').extract()[3])
    Out[22]: 'https://www.leboncoin.fr/'
    
    
On peut utiliser une liste compréhension pour transformer tous les liens récupérés par la méthode `extract()`.


 .. code-block:: Python

    In [23]: [response.urljoin(url) for url in response.css('a::attr(href)').extract()]
    Out[23]: 
    ['https://www.leboncoin.fr/',
     'https://www.leboncoin.fr/',
     'https://www.leboncoin.fr/',
     'https://www.leboncoin.fr/',
     'https://www.leboncoin.fr/ai?ca=12_s',
     'https://www.leboncoin.fr/annonces/offres',
     'https://www.leboncoin.fr/annonces/demandes',
     'https://www.leboncoin.fr/aw?ca=12_s',
     'https://www.leboncoin.fr/aw?ca=12_s&selected=backup',
     'https://www.leboncoin.fr/aw?ca=12_s&selected=search',
     'https://www.leboncoin.fr/boutiques/tout_secteur_d_activite/toutes_categories/ile_de_france/',
     'https://www.leboncoin.fr/',...]




     


    


    

