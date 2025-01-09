from dash import Input, Output, State, ALL, html, dcc
from MongoDB.website_request import add_task_to_db
from Scrapping.Amazon_scrap import scrape_product_details_with_image

def register_callbacks(app):
    # Callback pour l'affichage dynamique des entrées en fonction de l'input
    @app.callback(
        [Output('dynamic-inputs', 'children'),
         Output('type-data-store', 'data')],
        Input('input-tracking', 'value')
    )
    def display_dynamic_inputs(input_value):
        if input_value:
            is_url = input_value.startswith('http')
            type_data = 'link' if is_url else 'theme'
            dynamic_elements = [
                html.Label('Durée entre deux récupérations de données (en heures) :'),
                dcc.Input(
                    id={"type": "input-duration", "index": "1"},
                    type='number',
                    value=24,
                    min=1,
                    style={'width': '30%'}
                )
            ]
            if not is_url:
                dynamic_elements.append(
                    html.Div([
                        html.Label('Nombre de pages à scrapper (max 5) :'),
                        dcc.Dropdown(
                            id={"type": 'input-pages', "index": "1"},
                            options=[{'label': str(i), 'value': i} for i in range(1, 6)],
                            value=1,
                            style={'width': '30%'}
                        ),
                    ])
                )
            return dynamic_elements, type_data

        return "", None

    # Callback pour gérer les deux boutons "Envoyer" et "Rechercher"
    @app.callback(
        [Output('feedback-output', 'children'),
         Output('confirmation-message', 'children'),
         Output('input-tracking', 'value'),
         Output('dynamic-elements-container', 'children')],  # Ajoutez cet Output pour afficher dynamic_elements
        [Input('submit-button', 'n_clicks'), Input('search-button', 'n_clicks')],
        State('input-tracking', 'value'),
        State({'type': 'input-duration', 'index': ALL}, 'value'),
        State({'type': 'input-pages', 'index': ALL}, 'value'),
        State('type-data-store', 'data')
    )
    def handle_buttons_click(submit_n_clicks, search_n_clicks, input_value, duration_values, pages_values, type_data):
        if submit_n_clicks > 0 and input_value:
            # Logique pour le bouton "Envoyer"
            duration = duration_values[0] if duration_values else None
            pages = pages_values[0] if pages_values else None
            print(f"Envoi des données : Type - {type_data}, URL/Thème - {input_value}, Durée - {duration}, Pages - {pages}")
            add_task_to_db(type_data, input_value, duration, pages)
            confirmation_message = f"Les données ont été envoyées : URL/Thème - {input_value}, Durée - {duration}, Pages - {pages}"
            return "", confirmation_message, "", ""  # Réinitialisation de l'input

        elif search_n_clicks > 0 and input_value:
            # Logique pour le bouton "Rechercher"
            print(f"Recherche lancée pour : {input_value}")
            data = scrape_product_details_with_image(input_value)
            product_name = data["product_name"]
            price = data["price"]
            asin = data["asin"]
            product_image_url = data["image_url"]
            dynamic_elements = [
                html.H4(product_name, style={'text-align': 'center', 'color': '#333'}),
                html.Img(src=product_image_url, style={'display': 'block', 'margin': '20px auto', 'max-width': '80%'}),
                html.P(f"Prix : {price}", style={'text-align': 'center', 'color': '#666'}),
                html.P(f"ASIN : {asin}", style={'text-align': 'center', 'color': '#666'})
            ]
            confirmation_message = f"Les données ont été envoyées : URL/Thème - {input_value}, Durée - {duration_values}, Pages - {pages_values}"
            
            # Retourner dynamic_elements ici pour les afficher dans la Div correspondante
            return "", confirmation_message, input_value, dynamic_elements

        return "", "", input_value, ""  # Aucun changement si aucun bouton n'est cliqué
