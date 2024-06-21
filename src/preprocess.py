import pandas as pd

def load_and_preprocess_data(file_path):
    match_stats = pd.read_excel(file_path, sheet_name='Match Stats')

    # statistics to extract
    stats_to_extract = [
        'Goals', 'Ball Possession', 'Attempts on target', 'Attempts off target', 'Total Attempts',
        'Attempts against woodwork', 'Attempts Accuracy', 'Passes completed', 
        'Passes accuracy', 'Goals scored', 'Goals conceded', 'Own-goals', 'Fouls committed', 'Attempts blocked', 'Tackles', 'Fouls suffered', 'Fouls committed own half', 
        'Fouls committed opposite half', 'Fouls suffered own half', 'Penalty fouls'
    ]

    # Filter 
    filtered_stats = match_stats[match_stats['StatsName'].isin(stats_to_extract)]

    # Organizing rows and cols
    pivot_df = filtered_stats.pivot_table(
        index=['TeamID', 'TeamName'],
        columns='StatsName',
        values='Value',
        aggfunc='sum' # maybe not necesseray
    ).reset_index()

    # TODO : Rename the columns for clarity
    pivot_df.columns.name = None
    pivot_df = pivot_df.rename_axis(None, axis=1)

    return pivot_df
