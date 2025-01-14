from dash import html,dcc

page_rechercher=html.Div(
    [
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


       
    ]
)

base_contenu_début=html.Div(
    [
        html.Label('Durée entre deux récupérations de données (en heures) :'),
                dcc.Input(
                    id={"type": "input-duration", "index": "1"},
                    type='number',
                    value=24,
                    min=1,
                    style={'width': '30%'}
                )
    ]
)
#Si url, append ce contenu
contenu_pour_url=html.Div(
    [
        html.Div([
                        html.Label('Nombre de pages à scrapper (max 5) :'),
                        dcc.Dropdown(
                            id={"type": 'input-pages', "index": "1"},
                            options=[{'label': str(i), 'value': i} for i in range(1, 6)],
                            value=1,
                            style={'width': '30%'}
                        ),
                    ])
    ])


def resultat_url(product_name,product_image_url,price,asin):
    div=html.Div(
        [
            html.H4(product_name, style={'text-align': 'center', 'color': '#333'}),
            html.Img(src=product_image_url, style={'display': 'block', 'margin': '20px auto', 'max-width': '80%'}),
            html.P(f"Prix : {price}", style={'text-align': 'center', 'color': '#666'}),
            html.P(f"ASIN : {asin}", style={'text-align': 'center', 'color': '#666'}),
            
        ]
    )
    return div

def resulat_theme(data):
    dif=html.Div(
        [
            html.H4(f"Nombres de produits trouvés : {data}", style={'text-align': 'center', 'color': '#333'})
        ]
        )
    return dif
   
