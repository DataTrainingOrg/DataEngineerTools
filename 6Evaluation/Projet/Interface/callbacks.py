import time
import dash
from dash import Dash, Input, Output, State, dcc, html, ALL
import dash_bootstrap_components as dbc
from MongoDB.website_request import add_task_to_db
from Scrapping.Amazon_scrap import scrape_product_details_with_image, count_products_on_page
from backend.input_processing import is_amazon_url,is_url,clean_text
from Interface.page_recherche import resultat_url, resulat_theme

def register_callbacks(app):
    #Callback pour la gestion d'apparition de mon bouton traquer et du choix de délai
    @app.callback(
        Output('duration-submit-div', 'style'),
        Input('dynamic-content-div', 'children')
    )
    def toggle_duration_submit_visibility(dynamic_content):
        """
        Affiche ou masque le conteneur de durée et bouton en fonction du contenu généré.
        """
        if dynamic_content:  # Si du contenu existe dans dynamic-content-div
            return {'display': 'block', 'margin-top': '20px'}  # Affiche
        return {'display': 'none'}  # Masque


    # Callback pour déterminer le type de donnée (URL ou thème)
    @app.callback(
        Output('type-data-store', 'data'),
        Input('input-tracking', 'value')
    )
    def determine_input_type(input_value):
        if input_value:
            isUrl = is_url(input_value)
            type_data = 'link' if isUrl else 'theme'
            return type_data
        return None
    
    # Callback pour gérer les interactions des boutons "Envoyer" et "Rechercher"
    @app.callback(
        [
            Output('input-tracking', 'value'),
            Output('dynamic-content-div', 'children'),
            Output('confirmation-message-div', 'children'),
            Output('loading', 'overlay_style')  # Afficher/masquer l'animation de chargement
        ],
        Input('search-button', 'n_clicks'),
        Input('submit-button', 'n_clicks'),
        [
            State('input-tracking', 'value'),
            State('input-duration', 'value'),
            State('type-data-store', 'data')
        ]
    )
    def handle_search_click(search_n_clicks,submit_n_clicks, input_value, duration_values, type_data):
        ctx = dash.callback_context
        # Vérification si l'action vient du bouton "Rechercher"
        if not ctx.triggered:
            return input_value, "", "", {"visibility": "hidden", "filter": "none"}  # Pas d'action, valeurs par défaut

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'search-button' and search_n_clicks > 0 and input_value:
            print(type_data)
            # Afficher l'animation de chargement pendant le traitement
            overlay_style = {"visibility": "visible", "filter": "blur(2px)"}  # Animation visible

            if type_data == 'link':
                # Si type_data est 'link' (URL Amazon), traiter l'URL
                return handle_url_search(input_value, overlay_style)
            elif type_data == 'theme':
                input_value,error=clean_text(input_value)
                # Si type_data est 'theme', traiter la recherche par thème
                return handle_theme_search(input_value,error, overlay_style)

        if triggered_id == 'submit-button' and submit_n_clicks > 0 and input_value:
            
            # Logique pour le bouton "Envoyer"
            duration = duration_values if duration_values else None
            print(f"Envoi des données : Type - {type_data}, URL/Thème - {input_value}, Durée - {duration}")
            add_task_to_db(type_data, input_value, duration)
            confirmation_message = f"Les données ont été envoyées. Prochaine récupération dans {duration} heures."
            return "", "", confirmation_message , {"visibility": "hidden", "filter": "none"} # Réinitialisation de l'input
        # Valeurs par défaut si aucune action pertinente
        return input_value, "", "", {"visibility": "hidden", "filter": "none"}  # Masquer l'animation

    def handle_url_search(input_value, overlay_style):
        """Traite la recherche basée sur un lien Amazon."""
        if is_amazon_url(input_value):
            data = scrape_product_details_with_image(input_value)
            if not data:
                return "", "", "Aucun produit trouvé pour cette URL.", {"visibility": "hidden", "filter": "none"}
            
            product_name = data["product_name"]
            price = data["price"]
            asin = data["asin"]
            product_image_url = data["image_url"]
            
            dynamic_elements = [
                resultat_url(product_name, product_image_url, price, asin)
            ]
            return input_value, dynamic_elements, "", {"visibility": "hidden", "filter": "none"}  # Résultat trouvé
        else:
            return "", "","URL invalide, veuillez fournir un lien Amazon.",  {"visibility": "hidden", "filter": "none"}

    def handle_theme_search(input_value,error, overlay_style):
        """Traite la recherche basée sur un theme Amazon."""
        
        data = count_products_on_page(input_value)
        if data == 0:
            return "", "", "Aucun produit trouvé pour ce thème.", {"visibility": "hidden", "filter": "none"}

        dynamic_elements = [
            resulat_theme(data)
        ]
        return input_value, dynamic_elements, "Les caractères suivants ont été supprimés : "+error+", recherche effectuée pour "+input_value, {"visibility": "hidden", "filter": "none"}  # Résultat trouvé
