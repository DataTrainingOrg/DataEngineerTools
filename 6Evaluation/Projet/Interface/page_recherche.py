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
   
