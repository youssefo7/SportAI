from dash import html, dcc, Input, Output, register_page, callback
from service.graphs import create_goal_dist_bar_chart, create_radar_chart
from service.preprocess import Preprocessor
from service.stateManager import StateManager

state_manager = StateManager()

preprocessor = Preprocessor()

team_stats = preprocessor.get_processed_data()
goal_dist = preprocessor.get_goal_distribution_df()

register_page(__name__, "/analytic")

layout = html.Div([ 
    dcc.Location(id='url', refresh=True), 
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
])
@callback(
    Output('url', 'pathname'),
    [Input('url', 'pathname')]
)
def check_team_selected(pathname):
    # Redirect to a different page if no team is selected
    selected_team = state_manager.getAttr('selected_team')
    if not selected_team:
        pathname = '/dash/'
        return pathname 
    return pathname

@callback(Output('compare-title', 'children'),
              [Input('compare-title', 'title')])
def update_compare_title(title):
    selected_team = state_manager.getAttr('selected_team')
    title = f"Select a team to compare to {selected_team}:"
    return title

@callback(Output('radar-chart', 'figure'),
              [Input('team-dropdown-compare', 'value')])
def render_radar_chart(selected_team_to_compare):
    selected_team = state_manager.getAttr('selected_team')
    return create_radar_chart(team_stats, selected_team, selected_team_to_compare)

@callback(
    Output('goal_dist_bar_chart', 'figure'),
    [Input('goal_dist_bar_chart', 'figure')]
)
def update_on_graph_creation(figure):
    selected_team = state_manager.getAttr('selected_team')
    figure = create_goal_dist_bar_chart(goal_dist, selected_team)
    return figure
