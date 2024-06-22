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

def create_parallel_coordinates_plot(merged_data):
    parallel_fig = go.Figure(data=go.Parcoords(
        line=dict(color=merged_data['Goals'],  
                  colorscale='Tealrose',  
                  showscale=True,  
                  colorbar=dict(title='Goals'), 
                  cmin=merged_data['Goals'].min(), 
                  cmax=merged_data['Goals'].max()  
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
    ))

    parallel_fig.update_layout(
        title="UEFA Euro 2020 Team Performance: Parallel Coordinates",
        font=dict(size=12),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    return parallel_fig
