from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio
from preprocess import load_and_preprocess_data
import plotly.graph_objects as go
app = Flask(__name__)

@app.route('/')
def index():
    # Load the data
    file_path = './static/EURO_2020_DATA.xlsx'
    match_stats = pd.read_excel(file_path, sheet_name='Match Stats')

    # Extract relevant data
    goals_data = match_stats[match_stats['StatsName'] == 'Goals']
    goals_data = goals_data[['MatchID', 'TeamName', 'Value']].rename(columns={'Value': 'Goals'})

    possession_data = match_stats[match_stats['StatsName'] == 'Ball Possession']
    possession_data = possession_data[['MatchID', 'TeamName', 'Value']].rename(columns={'Value': 'Possession'})

    shots_data = match_stats[match_stats['StatsName'] == 'Total Attempts']
    shots_data = shots_data[['MatchID', 'TeamName', 'Value']].rename(columns={'Value': 'Shots'})

    # Merge the dataframes on MatchID and TeamName
    merged_data = goals_data.merge(possession_data, on=['MatchID', 'TeamName'])
    merged_data = merged_data.merge(shots_data, on=['MatchID', 'TeamName'])

    # Create the 3D scatter plot
    merged_data = merged_data.astype({'Possession': 'int32', 'Shots': 'int32', 'Goals': 'int32'})
    fig = px.scatter_3d(
        merged_data,
        x='Goals',
        y='Possession',
        z='Shots',
        color='TeamName',
        title='UEFA Euro 2020 Team Performance in 3D',
        labels={'Goals': 'Goals Scored', 'Possession': 'Ball Possession (%)', 'Shots': 'Total Shots'}
    )

    # Create the parallel coordinates plot
    parallel_fig = go.Figure(data=go.Parcoords(
    line=dict(color=merged_data['Goals'],  # Color code the lines based on Goals
              colorscale='Tealrose',  # Color scale for numerical data
              showscale=True,  # Show color scale legend
              colorbar=dict(title='Goals'),  # Color bar title
              cmin=merged_data['Goals'].min(),  # Minimum value of color scale
              cmax=merged_data['Goals'].max()  # Maximum value of color scale
             ),
    dimensions=[
        dict(range=[merged_data['Possession'].min(), merged_data['Possession'].max()],
             label='Possession (%)', values=merged_data['Possession']),
        dict(range=[merged_data['Shots'].min(), merged_data['Shots'].max()],
             label='Shots', values=merged_data['Shots']),
        dict(range=[merged_data['Goals'].min(), merged_data['Goals'].max()],
             label='Goals', values=merged_data['Goals']),
    ],
    ))
    # Convert plotly figure to JSON
    graph_json = pio.to_json(fig)
    parallel_graph_json = pio.to_json(parallel_fig)

    return render_template('index.html', graph_json=graph_json, parallel_graph_json=parallel_graph_json)


@app.route('/debug')
def debug():
    file_path = './static/EURO_2020_DATA.xlsx'
    
    team_stats = load_and_preprocess_data(file_path)
    # Log the DataFrame
    app.logger.debug(f"\n{team_stats}")

    return "DataFrame has been logged to the console."

if __name__ == '__main__':
    app.run(debug=True)
