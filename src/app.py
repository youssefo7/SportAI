from flask import Flask, render_template
import plotly.io as pio
from preprocess import load_and_preprocess_data
from graphs import create_3d_scatter_plot, create_parallel_coordinates_plot

app = Flask(__name__)

@app.route('/')
def index():
    # Path to the Excel file
    file_path = './static/EURO_2020_DATA.xlsx'
    
    team_stats = load_and_preprocess_data(file_path)

    # Create the plots 
    team_stats = team_stats.astype({'Ball Possession': 'int32', 'Total Attempts': 'int32', 'Goals': 'int32'})
    _3d_fig = create_3d_scatter_plot(team_stats)
    parallel_fig = create_parallel_coordinates_plot(team_stats)

    # Convert plotly figures to JSON
    _3d_graph_json = pio.to_json(_3d_fig)
    parallel_graph_json = pio.to_json(parallel_fig)

    return render_template('index.html', graph_json=_3d_graph_json, parallel_graph_json=parallel_graph_json)

@app.route('/debug')
def debug():
    file_path = './static/EURO_2020_DATA.xlsx'
    
    team_stats = load_and_preprocess_data(file_path)
    # Log the DataFrame
    app.logger.debug(f"\n{team_stats}")

    return "DataFrame has been logged to the console."

if __name__ == '__main__':
    app.run(debug=True)
