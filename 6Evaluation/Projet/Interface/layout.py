from dash import html, dcc
from Interface.tab_dynamic_interface import layout as tab_dynamic_layout

# Mise en page principale
layout = html.Div(
    style={'padding': '20px', 'font-family': 'Arial, sans-serif', 'backgroundColor': '#f4f4f9'},
    children=[
        dcc.Store(id='type-data-store'),  # Stockage pour type_data
        html.H3('Interface Dynamique avec Onglets', style={'text-align': 'center', 'color': '#333'}),

        # Onglets pour navigation
        dcc.Tabs([
            dcc.Tab(label='Onglet Dynamique', children=tab_dynamic_layout),
            dcc.Tab(label='Autre Onglet', children=html.Div("Contenu de l'autre onglet"))
        ]),

        # Conteneur pour l'animation de recherche
        html.Div(id='loading-container', children=[
            dcc.Loading(
                id='loading',
                type='circle',  # Animation de type 'circle' pendant la recherche
                children=html.Div(id='dynamic-elements-container', style={'margin-top': '20px'})
            )
        ], style={'margin-top': '20px'}),

        # Bouton "Envoyer" sous les champs de saisie
        html.Div(
            children=[
                html.Button('Envoyer', id='submit-button', n_clicks=0, style={
                    'background-color': '#008CBA', 'color': 'white', 'border': 'none', 'padding': '10px 20px',
                    'font-size': '16px', 'cursor': 'pointer', 'border-radius': '5px', 'margin-top': '20px'
                }),
            ],
            style={'display': 'flex', 'justify-content': 'center'}
        )
    ]
)
