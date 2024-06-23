from flask import Flask
from dash import Dash, page_container
from dash import html
from services.preprocess import Preprocessor
import dash_bootstrap_components as dbc
import os

server = Flask(__name__)

file_path = os.path.join(os.path.dirname(__file__), 'static', 'EURO_2020_DATA.xlsx')

preprocessor = Preprocessor(file_path)

app = Dash(__name__, use_pages=True ,server=server, url_base_pathname='/',external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css'  # Include Font Awesome
    ], )

app.layout = html.Div([
    html.H1("UEFA Euro 2020 Team Performance", style={'textAlign': 'center', 'padding': '20px'}),
    page_container
])
    
if __name__ == '__main__':
    app.run_server(debug=True)
