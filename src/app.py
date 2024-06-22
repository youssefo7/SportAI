from flask import Flask
from dash import Dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
from preprocess import load_and_preprocess_data
from graphs import create_offensive_3d_scatter_plot, create_defensive_3d_scatter_plot, create_parallel_coordinates_plot
import os

server = Flask(__name__)

app = Dash(__name__, server=server, url_base_pathname='/dash/')

file_path = os.path.join(os.path.dirname(__file__), 'static', 'EURO_2020_DATA.xlsx')

team_stats = load_and_preprocess_data(file_path)

team_stats = team_stats.astype({'Ball Possession': 'int32', 'Total Attempts': 'int32', 'Goals': 'int32'})
offensive_fig = create_offensive_3d_scatter_plot(team_stats)
defensive_fig = create_defensive_3d_scatter_plot(team_stats)
parallel_fig = create_parallel_coordinates_plot(team_stats)

app.layout = html.Div([
    html.H1("UEFA Euro 2020 Team Performance in 3D", style={'textAlign': 'center', 'padding': '20px'}),
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Offensive Performance', value='tab-1', style={'padding': '10px'}),
        dcc.Tab(label='Defensive Performance', value='tab-2', style={'padding': '10px'}),
        dcc.Tab(label='Parallel Coordinates', value='tab-3', style={'padding': '10px'}),
    ]),
    html.Div(id='tabs-content-example', style={'padding': '20px'})
])

@app.callback(Output('tabs-content-example', 'children'),
              Input('tabs-example', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return dcc.Graph(figure=offensive_fig)
    elif tab == 'tab-2':
        return dcc.Graph(figure=defensive_fig)
    elif tab == 'tab-3':
        return dcc.Graph(figure=parallel_fig)

if __name__ == '__main__':
    app.run_server(debug=True)