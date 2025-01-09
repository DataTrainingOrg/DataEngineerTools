from dash import Dash
from Interface.layout import layout
from Interface.callbacks import register_callbacks

app = Dash(__name__, suppress_callback_exceptions=True)
app.layout = layout

# Enregistrer les callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
