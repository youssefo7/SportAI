import pandas as pd

def load_and_preprocess_data(file_path):
    match_stats = pd.read_excel(file_path, sheet_name='Match Stats')

    stats_to_extract = [
        'Goals', 'Ball Possession', 'Attempts on target', 'Total Attempts',
        'Passes completed', 'Passes accuracy', 'Goals conceded', 'Fouls committed', 'Tackles', 'Saves'
    ]

    filtered_stats = match_stats[match_stats['StatsName'].isin(stats_to_extract)]

    pivot_df = filtered_stats.pivot_table(
        index=['TeamID', 'TeamName'],
        columns='StatsName',
        values='Value',
        aggfunc='sum'
    ).reset_index()

    pivot_df.columns.name = None
    pivot_df = pivot_df.rename_axis(None, axis=1)

    return pivot_df
