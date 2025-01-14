from dash import html, dcc
from Interface.page_recherche import page_rechercher

# Mise en page principale
layout = html.Div(
    style={'padding': '20px', 'font-family': 'Arial, sans-serif', 'backgroundColor': '#f4f4f9'},
    children=[
        dcc.Store(id='type-data-store'),  # Stockage pour type_data
        html.H1('Interface Dynamique avec Onglets', style={'text-align': 'center', 'color': '#333'}),

        # Onglets pour navigation
        dcc.Tabs([
            dcc.Tab(label='Recherche produit', children=[
                page_rechercher,
                html.Div(id='dynamic-inputs', style={'margin-bottom': '0px'}), 

                # Conteneur pour l'animation de recherche
                html.Div([
                    dcc.Loading(
                        id='loading',  # Identifiant du composant de chargement
                        type='circle',  # Type d'animation
                        overlay_style={"visibility": "hidden", "filter": "none"}  # Initialement caché
                    ),
                ], id='loading-container', style={'display': 'block','margin-bottom': '100px','margin-top': '100px'}),  # Visible quand activé

                html.Div(id='dynamic-content-div', style={'margin-top': '0px'}),  # Conteneur pour le contenu généré
                html.Div([
                    html.Label('Durée entre deux récupérations de données (en heures) :'),
                    dcc.Input(
                        id='input-duration',
                        type='number',
                        value=24,  # Valeur par défaut
                        min=1,  # Valeur minimale
                        step=1,  # Incrément de 1 heure
                        style={'width': '30%', 'padding': '10px', 'font-size': '16px'}
                    )
                ], style={'margin-top': '20px'}),

                html.Button('Traquer', id='submit-button', n_clicks=0, style={
                    'background-color': '#4CAF50', 'color': 'white', 'border': 'none', 'padding': '10px 20px',
                    'font-size': '16px', 'cursor': 'pointer', 'border-radius': '5px'
                }),
                html.Div(id='confirmation-message-div', style={'margin-top': '0px'})  # Confirmation
            ])
        ]),
    ]
)
