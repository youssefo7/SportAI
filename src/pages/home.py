from dash import html, dcc, Input, Output, register_page, callback
import dash_bootstrap_components as dbc
from service.graphs import create_defensive_3d_scatter_plot, create_offensive_3d_scatter_plot, create_parallel_coordinates_plot
from service.preprocess import Preprocessor
from service.stateManager import StateManager
register_page(__name__, "/")

state_manager = StateManager()

preprocessor = Preprocessor()

team_stats = preprocessor.get_processed_data()
layout = html.Div([ html.Div([
        html.Label("Select a team:", style={'padding': '10px', 'width': '10%'}),
        dcc.Dropdown(
            id='team-dropdown',
            options=[{'label': team, 'value': team} for team in team_stats['TeamName'].unique()],
            value='',
            style={'width': '90%','margin-left': '2%'}
        ),
        dbc.Button(
            id='next-page-button',
            href='/dash/analytic',
            color='primary',
            className='fas fa-arrow-right',
            style={'width': '150px', 'margin-left': '10px'}
        ),
    ], style={'display': 'flex', 'align-items': 'center','padding': '10px', 'textAlign': 'center'}),
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Offensive Performance', value='tab-1', style={'padding': '10px'}),
        dcc.Tab(label='Defensive Performance', value='tab-2', style={'padding': '10px'}),
    ]),
    dcc.Graph(id='graph-content', style={'height': '80vh', 'width': '100%'}),
    dcc.Graph(id='parallel_coordinates_plot', style={'height': '80vh', 'width': '100%'})
])

@callback(Output('graph-content', 'figure'),
              [Input('tabs-example', 'value'),
               Input('team-dropdown', 'value')])
def render_3d_scatter_plot(tab, selected_team):
    if tab == 'tab-1':
        return create_offensive_3d_scatter_plot(team_stats)
    elif tab == 'tab-2':
        return create_defensive_3d_scatter_plot(team_stats)
    
@callback(Output('parallel_coordinates_plot', 'figure'),
              [Input('team-dropdown', 'value')])
def render_parallel_coordinates_plot(selected_team):
    return create_parallel_coordinates_plot(team_stats, selected_team)

@callback(
    Output('next-page-button', 'disabled'),
    Input('team-dropdown', 'value')
)
def update_button_state(selected_team):
    state_manager.setAttr('selected_team', selected_team)

    if selected_team and selected_team in team_stats['TeamName'].values:
        return False
    else:
        return True
    
