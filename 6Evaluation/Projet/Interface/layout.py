from dash import html, dcc
from Interface.page_recherche import page_rechercher

# Styles globaux Amazon-like
amazon_styles = {
    'container': {
        'padding': '20px',
        'font-family': 'Arial, sans-serif',
        'backgroundColor': '#f3f3f3',
    },
    'header': {
        'text-align': 'center',
        'color': '#131921',
        'font-size': '32px',
        'margin-bottom': '20px',
    },
    'tabs': {
        'backgroundColor': '#ffffff',
        'border-radius': '5px',
        'box-shadow': '0 1px 3px rgba(0, 0, 0, 0.1)',
    },
    'tab': {
        'padding': '15px',
        'font-size': '16px',
        'font-weight': '600',
        'color': '#131921',
        'backgroundColor': '#f3f3f3',
        'border': '1px solid #ddd',
        'border-radius': '5px',
        'cursor': 'pointer',
    },
    'tab_selected': {
        'backgroundColor': '#febd69',
        'color': '#131921',
        'border': '1px solid #f90',
        'border-radius': '5px',
    },
    'content': {
        'backgroundColor': '#ffffff',
        'padding': '20px',
        'border-radius': '5px',
        'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
        'margin-top': '20px',
    },
    'button': {
        'backgroundColor': '#febd69',
        'color': '#131921',
        'border': 'none',
        'padding': '10px 20px',
        'border-radius': '5px',
        'cursor': 'pointer',
        'font-weight': '600',
    },
    'input': {
        'width': '100%',
        'padding': '10px',
        'margin-bottom': '10px',
        'border': '1px solid #ddd',
        'border-radius': '5px',
    },
    'label': {
        'font-size': '16px',
        'font-weight': 'bold',
        'color': '#131921',
    },
    'feedback': {
        'margin-top': '20px',
        'font-size': '16px',
        'color': '#131921',
        'font-weight': 'bold',
        'text-align': 'center',
    }
}

# Mise en page principale
layout = html.Div(
    style=amazon_styles['container'],
    children=[
        # En-tête principal
        html.H1('Interface Amazon-like', style=amazon_styles['header']),

        # Onglets pour navigation
        dcc.Tabs(
            style=amazon_styles['tabs'],
            children=[
                # Onglet Recherche produit
                dcc.Tab(
                    label='Recherche produit',
                    style=amazon_styles['tab'],
                    selected_style=amazon_styles['tab_selected'],
                    children=[
                        page_rechercher,
                        html.Div(id='dynamic-inputs', style=amazon_styles['content']),
                    ]
                ),
                # Onglet Visualisation de données
                dcc.Tab(
                    label='Visualisation de données',
                    style=amazon_styles['tab'],
                    selected_style=amazon_styles['tab_selected'],
                    children=[
                        dcc.Tabs(
                            children=[
                                dcc.Tab(
                                    label='Thème',
                                    style=amazon_styles['tab'],
                                    selected_style=amazon_styles['tab_selected'],
                                    children=[
                                        html.Div(
                                            [
                                                html.Label('Choix du Thème', style=amazon_styles['label']),
                                                dcc.Dropdown(
                                                    id='theme-dropdown',
                                                    options=[
                                                        {'label': 'Thème 1', 'value': 'theme1'},
                                                        {'label': 'Thème 2', 'value': 'theme2'}
                                                    ],
                                                    placeholder='Sélectionnez un thème',
                                                    style=amazon_styles['input']
                                                )
                                            ],
                                            style=amazon_styles['content']
                                        )
                                    ]
                                ),
                                dcc.Tab(
                                    label='URL',
                                    style=amazon_styles['tab'],
                                    selected_style=amazon_styles['tab_selected'],
                                    children=[
                                        html.Div(
                                            [
                                                html.Label('Visualisation via URL', style=amazon_styles['label']),
                                                dcc.Input(
                                                    id='url-input',
                                                    type='url',
                                                    placeholder='Entrez une URL',
                                                    style=amazon_styles['input']
                                                ),
                                                html.Button('Charger', id='load-url-button', style=amazon_styles['button'])
                                            ],
                                            style=amazon_styles['content']
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                # Onglet Alertes
                dcc.Tab(
                    label='Alertes',
                    style=amazon_styles['tab'],
                    selected_style=amazon_styles['tab_selected'],
                    children=[
                        html.Div(
                            [
                                html.Label('Nom du produit', style=amazon_styles['label']),
                                dcc.Input(
                                    id='product-name-input',
                                    type='text',
                                    placeholder='Entrez le nom du produit',
                                    style=amazon_styles['input']
                                ),
                                html.Label('Prix cible', style=amazon_styles['label']),
                                dcc.Input(
                                    id='target-price-input',
                                    type='number',
                                    placeholder='Entrez le prix cible',
                                    style=amazon_styles['input']
                                ),
                                html.Button('Ajouter une alerte', id='add-alert-button', style=amazon_styles['button']),
                                html.Div(id='alert-feedback', style=amazon_styles['feedback']),
                            ],
                            style=amazon_styles['content']
                        )
                    ]
                )
            ]
        )
    ]
)
