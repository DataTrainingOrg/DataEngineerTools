from dash import html, dcc
from Interface.page_recherche import page_rechercher

# Mise en page principale
layout = html.Div(
    style={
        'padding': '20px', 
        'font-family': 'Arial, sans-serif', 
        'backgroundColor': '#f9f9fc'
    },
    children=[
        # Stockage pour type_data
        dcc.Store(id='type-data-store'),  

        # En-tête principal
        html.H1(
            'Interface Dynamique avec Onglets', 
            style={
                'text-align': 'center', 
                'color': '#444', 
                'font-size': '32px', 
                'margin-bottom': '20px'
            }
        ),

        # Onglets pour navigation
        dcc.Tabs(
            style={
                'backgroundColor': '#fff', 
                'border-radius': '8px',
                'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)'
            },
            children=[
                dcc.Tab(
                    label='Recherche produit', 
                    style={
                        'padding': '15px', 
                        'font-size': '18px', 
                        'font-weight': 'bold', 
                        'backgroundColor': '#f1f1f8',
                        'border': '1px solid #ccc',
                        'border-radius': '8px'
                    },
                    selected_style={
                        'backgroundColor': '#4CAF50', 
                        'color': 'white', 
                        'border': '1px solid #4CAF50', 
                        'border-radius': '8px'
                    },
                    children=[
                        page_rechercher,
                        html.Div(
                            id='dynamic-inputs', 
                            style={
                                'margin-bottom': '0px',
                                'padding': '10px',
                                'backgroundColor': '#fff',
                                'border-radius': '8px',
                                'box-shadow': '0 1px 3px rgba(0, 0, 0, 0.1)'
                            }
                        ), 

                        # Animation de chargement
                        html.Div(
                            [
                                dcc.Loading(
                                    id='loading',  
                                    type='circle',  
                                    color='#4CAF50',
                                    style={'visibility': 'visible'}
                                ),
                            ],
                            id='loading-container', 
                            style={
                                'text-align': 'center',
                                'margin-top': '50px',
                                'margin-bottom': '50px'
                            }
                        ),

                        # Conteneur dynamique
                        html.Div(
                            id='dynamic-content-div', 
                            style={
                                'margin-top': '20px',
                                'backgroundColor': '#fff',
                                'padding': '20px',
                                'border-radius': '8px',
                                'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)'
                            }
                        ),

                        # Section pour la durée et le bouton
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Label(
                                            'Durée entre deux récupérations de données (en heures) :',
                                            style={'font-size': '16px', 'font-weight': 'bold', 'color': '#333'}
                                        ),
                                        dcc.Input(
                                            id='input-duration',
                                            type='number',
                                            value=24,  
                                            min=1,  
                                            step=1,  
                                            style={
                                                'width': '40%', 
                                                'padding': '10px', 
                                                'font-size': '16px',
                                                'margin-top': '10px',
                                                'border': '1px solid #ccc',
                                                'border-radius': '4px'
                                            }
                                        )
                                    ], 
                                    style={'margin-bottom': '20px'}
                                ),

                                html.Button(
                                    'Traquer', 
                                    id='submit-button', 
                                    n_clicks=0, 
                                    style={
                                        'background-color': '#4CAF50', 
                                        'color': 'white', 
                                        'border': 'none', 
                                        'padding': '10px 20px',
                                        'font-size': '16px', 
                                        'cursor': 'pointer', 
                                        'border-radius': '5px',
                                        'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)'
                                    }
                                ),
                            ],
                            id='duration-submit-div',
                            style={
                                'display': 'none',
                                'backgroundColor': '#fff',
                                'padding': '20px',
                                'border-radius': '8px',
                                'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
                                'margin-top': '20px'
                            }
                        ),

                        # Confirmation message
                        html.Div(
                            id='confirmation-message-div',
                            style={
                                'margin-top': '20px',
                                'font-size': '16px',
                                'color': '#4CAF50',
                                'font-weight': 'bold',
                                'text-align': 'center'
                            }
                        )
                    ]
                )
            ]
        ),
    ]
)
