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
