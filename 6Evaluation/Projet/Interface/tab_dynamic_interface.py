from dash import html, dcc

# Mise en page de l'onglet dynamique
layout = html.Div(
    style={'padding': '20px', 'font-family': 'Arial, sans-serif', 'backgroundColor': '#f4f4f9'},
    children=[
        html.H3('Interface Dynamique', style={'text-align': 'center', 'color': '#333'}),

        dcc.Input(
            id='input-tracking',
            placeholder='Entrez un lien ou un thème...',
            type='text',
            style={'width': '70%', 'marginRight': '10px', 'padding': '10px', 'font-size': '16px'}
        ),

        html.Button('Rechercher', id='search-button', n_clicks=0, style={
            'background-color': '#4CAF50', 'color': 'white', 'border': 'none', 'padding': '10px 20px',
            'font-size': '16px', 'cursor': 'pointer', 'border-radius': '5px'
        }),

        # Affichage dynamique des entrées
        html.Div(id='dynamic-inputs', style={'margin-top': '20px'}),
        html.Div(id='feedback-output', style={'margin-top': '20px', 'color': 'green'}),
        html.Div(id='confirmation-message', style={'margin-top': '20px', 'color': 'blue'}),

        
    ]
)
