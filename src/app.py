from flask import Flask
from dash import Dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
from preprocess import load_and_preprocess_data, get_goal_distribution_df
from graphs import create_offensive_3d_scatter_plot, create_defensive_3d_scatter_plot, create_parallel_coordinates_plot, \
    create_goal_dist_bar_chart, create_radar_chart
import os

server = Flask(__name__)

app = Dash(__name__, server=server, url_base_pathname='/dash/', suppress_callback_exceptions=True)

with open('templates/index.html', 'r') as file:
    index_string = file.read()

# Assign index_string to app.index_string
app.index = index_string
file_path = os.path.join(os.path.dirname(__file__), 'static', 'EURO_2020_DATA.xlsx')

team_stats = load_and_preprocess_data(file_path)
goal_dist = get_goal_distribution_df(file_path)

app.layout = html.Div([
    html.H1("UEFA Euro 2020 Team Performance in 3D", style={'textAlign': 'center', 'padding': '20px'}),
    html.Div([
        html.Label("Select a team:", style={'padding': '10px'}),
        dcc.Dropdown(
            id='team-dropdown',
            options=[{'label': team, 'value': team} for team in team_stats['TeamName'].unique()],
            value='Italy',
            style={'width': '95%'}
        ),
    ], style={'display': 'flex', 'padding': '10px'}),

    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Offensive Performance', value='tab-1', style={'padding': '10px'}),
        dcc.Tab(label='Defensive Performance', value='tab-2', style={'padding': '10px'}),
    ]),
    dcc.Graph(id='graph-content', style={'height': '80vh', 'width': '100%'}),
    dcc.Graph(id='parallel_coordinates_plot', style={'height': '80vh', 'width': '100%'}),
    html.Div(id='compare-title', style={'padding': '10px'}),
    html.Div([
        dcc.Dropdown(
            id='team-dropdown-compare',
            options=[{'label': team, 'value': team} for team in team_stats['TeamName'].unique()],
            value='',
            style={'width': '95%'}
        ),
        dcc.Graph(id='radar-chart', style={'height': '80vh', 'width': '100%'})
    ], style={'padding': '10px'}),
    dcc.Graph(id='goal_dist_bar_chart', style={'height': '80vh', 'width': '100%'}),

    html.Div(id='hover-data')
])


@app.callback(Output('graph-content', 'figure'),
              [Input('tabs-example', 'value'),
               Input('team-dropdown', 'value')])
def render_3d_scatter_plot(tab, selected_team):
    if tab == 'tab-1':
        return create_offensive_3d_scatter_plot(team_stats)
    elif tab == 'tab-2':
        return create_defensive_3d_scatter_plot(team_stats)


@app.callback(Output('parallel_coordinates_plot', 'figure'),
              [Input('team-dropdown', 'value')])
def render_parallel_coordinates_plot(selected_team):
    return create_parallel_coordinates_plot(team_stats, selected_team)


@app.callback(Output('compare-title', 'children'),
              [Input('team-dropdown', 'value')])
def update_compare_title(selected_team):
    return html.Label(f"Select a team to compare to {selected_team}:", style={'padding': '10px'})


@app.callback(Output('radar-chart', 'figure'),
              [Input('team-dropdown', 'value'),
               Input('team-dropdown-compare', 'value')])
def render_radar_chart(selected_team, selected_team_to_compare):
    return create_radar_chart(team_stats, selected_team, selected_team_to_compare)


@app.callback(Output('goal_dist_bar_chart', 'figure'),
              [Input('team-dropdown', 'value')])
def render_goal_dist_bar_chart(selected_team):
    return create_goal_dist_bar_chart(goal_dist, selected_team)


if __name__ == '__main__':
    app.run_server(debug=True)
