Les Projets
===========

Sujet 1
-------

Objectif : Construire une base MongoDB des monuments historiques parisiens consultable via une interface Flask

URL : `http://www.culture.gouv.fr/public/mistral/dapamer_fr?ACTION=RETOUR&USRNAME=nobody&USRPWD=4%24%2534P`

Structure de la base MongoDB :

.. code-block::

    <adresse>:
        {   "numero" : [<32-bit integer>] , 
            "voie" : <String>, 
            "nom_voie" : <String>, 
            "code_postal" : <32-bit integer>, 
            "ville" : <String> }

    <loc>:
        {   "lat" : <Double>,
            "lon" : <Double>
        }

    { "appellation" : <String>,
        "adresses" : [<adresse>],
        "locs" : [<loc>]
        "date_protection" : <Date>,
        "inscrit_mh" : <Boolean>,
        "prec_protection" : <String>,
        "denomination" : [<String>],
        "elements_mh" : [<String>],
        "date" : <Date>,
        "auteur" : <String>,
        "historique" : <String>,
        "statut" : <String>
    }
    
Exemple : www.culture.gouv.fr/public/mistral/dapamer_fr?ACTION=RETROUVER&NUMBER=1&REQ=((paris) %3aLOCA%2cPLOC )
Ressources externes : on pourra utiliser https://adresse.data.gouv.fr/api pour le geocoding


Sujet 2
-------

Objectif : Construire une base MongoDB des jardins et musées parisiens consultable via une interface Flask
URLs : https://meslieux.paris.fr/principaux-parcs-et-jardins, https://meslieux.paris.fr/musees-municipaux
Structure de la base MongoDB :

.. code-block:: 

    <adresse>:
        {   "numero" : [<32-bit integer>] , 
            "voie" : <String>, 
            "nom_voie" : <String>, 
            "code_postal" : <32-bit integer>, 
            "ville" : <String> }

    <loc>:
        {   "lat" : <Double>,
            "lon" : <Double>
        }

    <station> : 
        {   nom:<String>, 
            adresse:<adresse>
        }

    <metro> : <station>
    <bus> : <station>
    <velib> : <station>

    <horaire> : 
        {
            <jour> : <String>,
            <heures> : [<32-bit integer>, <32-bit integer>] # 7:00 - 21:00 stored as [ 420, 1260]
        }

    <tarif> :
        {
            "categorie" : <String>,
            "prix" : <Double>
        }
    

    { "appellation" : <String>,
        "adresses" : [<adresse>],
        "locs" : [<loc>],
        "metros" : [<metro>]
        "buss" : [<bus>]
        "velibs" : [<velib>]
        "infos" : <String>,
        "horaires" : [<horaire>],
        "tarifs" : [tarif]
    }
    
Exemple : http://equipement.paris.fr/musee-cognacq-jay-1519, http://equipement.paris.fr/jardin-des-tuileries-1795
Ressources externes : on pourra utiliser https://adresse.data.gouv.fr/api pour le geocoding


Sujet 3
-------

Récupérer toutes les agences immobilières de la chaine ORPi ainsi que toutes les annonces correspondantes. Vous pouvez récupérer toutes les agences depuis ce lien https://www.orpi.com/agences-immobilieres/recherche/
Structure de la base MongoDB :
Pour une agence (exemple https://www.orpi.com/agence-de-lizy/)

.. code-block::

    <contact>:
        {   
            "phone" : <String>, 
            "email" : <String>, 
         }

    <location>:
        {               
            "address" : <String>, 
            "city" : <String>,
            "lat" : <double>, 
            "lon" : <double> 
        }

    <informations> : 
        {   
            rating:<String>, 
            description:<String>,
            sells_number:<32-bit integer>,
            location_number:<32-bit integer>,
            ad_number:<32-bit integer>,
            agent_number:<32-bit integer>,

        }
    <agent_contacts> : 
        {   
            name:<String>,
            title:<String>,
            email:<String>,
            phone_number:<32-bit integer>,
        }


Le document représentant une agence s'agencera sous la forme : 

.. code-block::

    { 
        "url" : <String>,
        "agency_contact" : <contact>,
        "location" : <location>,
        "informations" : <informations>,
        "agent_contacts" : <agent_contacts>,

    }
    
Ensuite vous devrez récupérer toutes les annonces des différentes agences dans une nouvelle collection : 

Le format de données représentant une annonce sera : 

.. code-block::

    { 
        "url" : <String>,
        "domaine": <String>,
        "title" : <String>,
        "type":<String>,
        "room_number":<32-bit integer>,
        "bed_room_number":<32-bit integer>,
        "bath_room_number":<32-bit integer>,
        "construction_year":<32-bit integer>,
        "area" : <32-bit integer>,
        "storey" : <32-bit integer>,
        "total_storey" : <32-bit integer>,
        "description" : <String>,
        "ges" : <String>,
        "energy" : <String>,
        "location":<location>,
        "local_id":<String>, 
        "images":[<String>]
    }


Encore dans l'immobilier, je vous propose de récupérer toutes les annonces du site Logic-Immo. Pour cela vous pouvez partir de la page index de toutes les villes : http://www.logic-immo.com/index-villes-vente.html. Récupérer les villes par ordre alphabétique, et ensuite récupérer la page annonce. 

La structure des annonces sera à peut près la même que pour le projet précédant. 

.. code-block::

    { 
        "url" : <String>,
        "domaine": <String>,
        "title" : <String>,
        "type":<String>, 
        "room_number":<32-bit integer>,
        "phone_number":<32-bit integer>,
        "bed_room_number":<32-bit integer>,
        "bath_room_number":<32-bit integer>,
        "construction_year":<32-bit integer>,
        "area" : <32-bit integer>,
        "storey" : <32-bit integer>,
        "total_storey" : <32-bit integer>,
        "description" : <String>,
        "ges" : <String>,
        "energy" : <String>,
        "location":<location>,
        "local_id":<String>,
        "images":[<String>]

    }
