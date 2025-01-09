from dash import html, dcc
from Interface.tab_dynamic_interface import layout as tab_dynamic_layout

# Mise en page principale
layout = html.Div(
    style={'padding': '20px', 'font-family': 'Arial, sans-serif', 'backgroundColor': '#f4f4f9'},
    children=[
        dcc.Store(id='type-data-store'),  # Stockage pour type_data
        html.H3('Interface Dynamique avec Onglets', style={'text-align': 'center', 'color': '#333'}),

        dcc.Tabs([
            dcc.Tab(label='Onglet Dynamique', children=tab_dynamic_layout),
            dcc.Tab(label='Autre Onglet', children=html.Div("Contenu de l'autre onglet"))
        ])
    ]
)
