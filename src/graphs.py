import plotly.express as px
import plotly.graph_objects as go

def create_offensive_3d_scatter_plot(merged_data):
     fig = px.scatter_3d(
        merged_data,
        x='Goals',
        y='Ball Possession',
        z='Total Attempts',
        color='TeamName',
        title='UEFA Euro 2020 Team Offensive Performance in 3D',
        labels={'Goals': 'Goals Scored', 'Ball Possession': 'Ball Possession (%)', 'Total Attempts': 'Total Shots'}
    )

     return fig

def create_defensive_3d_scatter_plot(merged_data):
    fig = px.scatter_3d(
        merged_data,
        x='Fouls committed',
        y='Tackles',
        z='Saves',
        color='TeamName',
        title='UEFA Euro 2020 Team Defensive Performance in 3D',
        labels={'Fouls committed': 'Fouls Committed', 'Tackles': 'Tackles Won', 'Saves': 'Saves'}
    )
    return fig

def create_parallel_coordinates_plot(merged_data,selected_team):
     # Default line color (gray)
    line_colors = merged_data['Goals']
    
    # Highlight the selected team in a specific color, if specified
    if selected_team and selected_team in merged_data['TeamName'].values:
        line_colors = [ merged_data['Goals'].max() if team == selected_team else merged_data['Goals'].min() for team in merged_data['TeamName']]
    
    parallel_fig = go.Figure(data=go.Parcoords(
        line=dict(color=line_colors,  
                  colorscale='Tealrose',  
                 ),
        dimensions=[
            dict(range=[merged_data['Ball Possession'].min(), merged_data['Ball Possession'].max()],
                 label='Ball Possession (%)', values=merged_data['Ball Possession']),
            dict(range=[merged_data['Total Attempts'].min(), merged_data['Total Attempts'].max()],
                 label='Total Attempts', values=merged_data['Total Attempts']),
            dict(range=[merged_data['Goals'].min(), merged_data['Goals'].max()],
                 label='Goals', values=merged_data['Goals']),
            dict(range=[merged_data['Passes completed'].min(), merged_data['Passes completed'].max()],
                 label='Passes Completed', values=merged_data['Passes completed']),
            dict(range=[merged_data['Passes accuracy'].min(), merged_data['Passes accuracy'].max()],
                 label='Passes Accuracy (%)', values=merged_data['Passes accuracy']),
            dict(range=[merged_data['Attempts on target'].min(), merged_data['Attempts on target'].max()],
                 label='Attempts on Target', values=merged_data['Attempts on target']),
            dict(range=[merged_data['Goals conceded'].min(), merged_data['Goals conceded'].max()],
                 label='Goals Conceded', values=merged_data['Goals conceded']),
            dict(range=[merged_data['Fouls committed'].min(), merged_data['Fouls committed'].max()],
                 label='Fouls Committed', values=merged_data['Fouls committed']),
        ],
        ids=merged_data.index,
    ))
    parallel_fig.update_layout(
        title="UEFA Euro 2020 Team Performance: Parallel Coordinates",
        font=dict(size=12),
        paper_bgcolor='white',
        plot_bgcolor='white',
        hovermode='closest'
    )

    return parallel_fig

def create_goal_dist_bar_chart(data, team):
     team = str(team).strip()
     
     team_data = data.loc[team]
     plot_df = team_data.reset_index()
     plot_df.columns = ['Period', 'Goals']
    
     fig = px.bar(plot_df, x='Period', y='Goals', title=f'Goal distribution within a match of {team} during Euro 2020')
     return fig

import plotly.graph_objects as go

def create_radar_chart(team_stats, selected_team, selected_team_to_compare):
    stats_to_plot = [
        'Goals', 'Ball Possession', 'Attempts blocked', 'Goals conceded',
        'Attempts on target conceded', 'Attempts on target'
    ]
    radar_chart_title = f'{selected_team} Performance Radar Chart'

    team_stats_selected = team_stats[team_stats['TeamName'] == selected_team][stats_to_plot].iloc[0]
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=team_stats_selected,
        theta=stats_to_plot,
        fill='toself',
        name=selected_team,
        line=dict(color='blue')
    ))

    if selected_team_to_compare:
        team_stats_compare = team_stats[team_stats['TeamName'] == selected_team_to_compare][stats_to_plot].iloc[0]

        fig.add_trace(go.Scatterpolar(
            r=team_stats_compare,
            theta=stats_to_plot,
            fill='toself',
            name=selected_team_to_compare,
            line=dict(color='red')
        ))

        radar_chart_title = f'{selected_team} vs {selected_team_to_compare} Performance Radar Chart'

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
            )),
        title=radar_chart_title
    )

    return fig
