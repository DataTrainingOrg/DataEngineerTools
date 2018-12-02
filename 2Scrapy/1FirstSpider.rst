
Un scraping élémentaire
=======================

Avant de rentrer dans les détails du framework, nous allons mettre en oeuvre un premier script permettant de récupérer l'information présente sur `la page web <http://evene.lefigaro.fr/citations/winston-churchill>`_ recensant les citations de `Sir Winston Churchill <https://en.wikipedia.org/wiki/Winston_Churchill>`_. 

.. topic:: Exercice
    
    Examiner le code source de cette page avec l'inspecteur de votre navigateur. Identifier les éléments contenant l'information recherchée, ici la chaîne de caractères contenant la citation proprement dite.

Le code source
--------------

Le code utilisé est le suivant:

.. code-block:: python

    # citations_churchill_spider1.py

    import scrapy

    class ChurchillQuotesSpider(scrapy.Spider):
        name = "citations de Churchill"
        start_urls = ["http://evene.lefigaro.fr/citations/winston-churchill",]

        def parse(self, response):
            for cit in response.xpath('//div[@class="figsco__quote__text"]'):
                text_value = cit.xpath('a/text()').extract_first()
                yield { 'text' : text_value }

Le fonctionnement
-----------------

Le fonctionnement est le suivant:

- On importe le module `Scrapy <https://scrapy.org/>`_ (3)
- et on définit une sous classe de `scrapy.Spider` (5)
- la variable ``start_urls`` contient la liste des pages à scraper (7)
- On redéfinit la méthode `parse` dont la signature est définie dans la classe mère (9)
- L'objet `response <https://docs.scrapy.org/en/latest/topics/request-response.html#response-objects>`_ représente la réponse à la requête HTTP (l'attribut `text` permet d'accéder à son contenu). On recherche ensuite tous les containers ``<div>`` identifiés dans l'exercice précédent. Ici la page est particulièrement bien structurée et les citations disposent de leur propre container, identifié par l'attribut ``class`` de valeur ``figsco__quote__text``. La sélection se fait par une expression `XPath <https://en.wikipedia.org/wiki/XPath>`_, un langage de sélection de noeud dans un document XML (10). En langage naturel, la requête pourrait se formuler : "On recherche tous les containers ``<div>`` dont la valeur de l'attribut ``class`` est égal à ``figsco__quote__text``". 
- Pour chaque résultat, on construit un dictionnaire dont la clé est ``text`` et la valeur le contenu du lien ``<a>``. Ce résultat est fourni par un générateur (`yield`) (12).

On lance le scraping depuis un terminal::

    $ scrapy runspider spiders/citations_churchill_spider1.py

Examinons le log... On y trouve des informations sur les paramètres utilisés::

    2018-01-10 17:21:05 [scrapy.utils.log] INFO: Scrapy 1.4.0 started (bot: scrapybot)
    2018-01-10 17:21:05 [scrapy.utils.log] INFO: Overridden settings: {'SPIDER_LOADER_WARN_ONLY': True}

les `extensions <https://docs.scrapy.org/en/latest/topics/extensions.html>`_ ...::

    2018-01-10 17:21:05 [scrapy.middleware] INFO: Enabled extensions:
    ['scrapy.extensions.corestats.CoreStats',
    'scrapy.extensions.telnet.TelnetConsole',
    'scrapy.extensions.logstats.LogStats']

`Les composants middleware downloader <https://docs.scrapy.org/en/latest/topics/downloader-middleware.html>`_ ... ::

    2018-01-10 17:21:05 [scrapy.middleware] INFO: Enabled downloader middlewares:
    ['scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware',
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware',
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware',
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware',
    'scrapy.downloadermiddlewares.retry.RetryMiddleware',
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware',
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware',
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware',
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware',
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware',
    'scrapy.downloadermiddlewares.stats.DownloaderStats']

Idem pour `les composants middleware spider <https://docs.scrapy.org/en/latest/topics/spider-middleware.html>`_ ...::

    2018-01-10 17:21:05 [scrapy.middleware] INFO: Enabled spider middlewares:
    ['scrapy.spidermiddlewares.httperror.HttpErrorMiddleware',
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware',
    'scrapy.spidermiddlewares.referer.RefererMiddleware',
    'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',
    'scrapy.spidermiddlewares.depth.DepthMiddleware']

Aucun `pipeline <https://docs.scrapy.org/en/latest/topics/item-pipeline.html>`_ n'est activé ::

    2018-01-10 17:21:05 [scrapy.middleware] INFO: Enabled item pipelines:
    []

.. topic:: Exercice

    Identifier la  position des `composants middleware downloader <https://docs.scrapy.org/en/latest/topics/downloader-middleware.html>`_, des `composants middleware spider <https://docs.scrapy.org/en/latest/topics/spider-middleware.html>`_ et du `pipeline <https://docs.scrapy.org/en/latest/topics/item-pipeline.html>`_ dans `l'architecture <Introduction>`

L'exécution du scraping proprement dit débute ::

    2018-01-10 17:21:05 [scrapy.core.engine] INFO: Spider opened
    2018-01-10 17:21:05 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)
    2018-01-10 17:21:05 [scrapy.extensions.telnet] DEBUG: Telnet console listening on 127.0.0.1:6023

La première URL est poussée par le scheduler::

    2018-01-10 17:21:05 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://evene.lefigaro.fr/citations/winston-churchill> (referer: None)

Les résultats
-------------

Les résultats sont fournis par le générateur défini dans la méthode `parse` dans un dictionnaire. Ils contiennent le texte des citations dans la valeur de la clé ``text``::

    2018-01-10 17:21:05 [scrapy.core.scraper] DEBUG: Scraped from <200 http://evene.lefigaro.fr/citations/winston-churchill>
    {'text': '“Le vice inhérent au capitalisme consiste en une répartition inégale des richesses. La vertu inhérente au socialisme consiste en une égale répartition de la misère.”'}
    ...
    2018-01-10 17:21:05 [scrapy.core.scraper] DEBUG: Scraped from <200 http://evene.lefigaro.fr/citations/winston-churchill>
    {'text': "Faire le bien, éviter le mal, c'est ça le paradis."}

Les statistiques
----------------

Une fois le scraping effectué, quelques statistiques sont affichées sur le terminal::

    2018-01-10 17:21:05 [scrapy.core.engine] INFO: Closing spider (finished)
    2018-01-10 17:21:05 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
    {'downloader/request_bytes': 242,
    'downloader/request_count': 1,
    'downloader/request_method_count/GET': 1,
    'downloader/response_bytes': 17435,
    'downloader/response_count': 1,
    'downloader/response_status_count/200': 1,
    'finish_reason': 'finished',
    'finish_time': datetime.datetime(2018, 1, 10, 16, 21, 5, 858347),
    'item_scraped_count': 16,
    'log_count/DEBUG': 18,
    'log_count/INFO': 7,
    'response_received_count': 1,
    'scheduler/dequeued': 1,
    'scheduler/dequeued/memory': 1,
    'scheduler/enqueued': 1,
    'scheduler/enqueued/memory': 1,
    'start_time': datetime.datetime(2018, 1, 10, 16, 21, 5, 645347)}
    2018-01-10 17:21:05 [scrapy.core.engine] INFO: Spider closed (finished)

On observe notamment que notre code permet de récupérer la taille de la page web (17435 bytes), le temps d'exécution à partir des valeurs ``finish_time`` et ``start_time``, le nombre d'items scrapés (16), etc...

.. topic:: Exercice

    Les citations extraites sont elles toutes de `Sir Winston Churchill <https://en.wikipedia.org/wiki/Winston_Churchill>`_ ? Il sera peut être nécessaire de modifier le sélecteur XPath. Nous verrons ça lorsque il faudra récupérer les données relative à l'auteur.

Modifier les données
--------------------

Il est parfois nécessaire de faire un traitement sur les données scrapées, pour ajouter ou retirer de l'information.

.. topic:: Exercice

    Retirer les caractères ``“`` et ``”`` qui délimitent la citation. Ces caractères sont identifiés en Unicode comme `LEFT DOUBLE QUOTATION MARK <http://www.fileformat.info/info/unicode/char/201c/index.htm>`_ et `RIGHT DOUBLE QUOTATION MARK <http://www.fileformat.info/info/unicode/char/201d/index.htm>`_.

..
    text_value = cit.xpath('a/text()').extract_first().replace('“', '').replace('”', '')

Plus de données
---------------

Il est souvent nécessaire de récupérer plusieurs informations relatives à un même item. Dans cet exemple, il est judicieux d'associer à la citation le nom de son auteur, en allant chercher cette information au plus près du texte lui même.

.. topic:: Exercice

    Examiner le code source de la page web et identifier la structuration de la donnée associée à l'auteur. En déduire l'expression XPath permettant de la récupérer. S'assurer que seules les citations de `Sir Winston Churchill <https://en.wikipedia.org/wiki/Winston_Churchill>`_ sont extraites. Ajouter une clé ``author`` au dictionnaire retourné par le `yield` dont la valeur est précisément la chaîne de caractères contenant l'auteur.

    Un exemple de dictionnaire retourné::

        {   'text': "“Si deux hommes ont toujours la même opinion, l'un d'eux est de trop.”", 
            'author': 'Winston Churchill'}

..
    # citations_churchill_spider2.py

    import scrapy

    class ChurchillQuotesSpider(scrapy.Spider):
        name = "citations de Churchill"
        start_urls = ["http://evene.lefigaro.fr/citations/winston-churchill",]

        def parse(self, response):
            for cit in response.xpath('//article'):
                text_value = cit.xpath('div[@class="figsco__quote__text"]/a/text()').extract_first()
                if text_value:
                    text_value = text_value.replace('“', '').replace('”', '')
                author_value = cit.xpath('div/div[@class="figsco__fake__col-9"]/a/text()').extract_first()
                yield { 'text' : text_value,
                        'author' : author_value }

Pour lancer l'exécution de la spider : 

    $ scrapy runspider spiders/citations_churchill_spider2.py

On peut aussi vouloir stocker les données extraites : 

    $ scrapy runspider spiders/citations_churchill_spider2.py -o data/citation.json -t json 

