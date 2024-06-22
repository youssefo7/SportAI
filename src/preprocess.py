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

def get_team_goal_distribution(team_id):
    match_events_df = pd.read_excel('./static/EURO_2020_DATA.xlsx', sheet_name='Match events')

    team_goals = match_events_df[((match_events_df['TeamFromID'] == team_id) & 
                                 (match_events_df['Event'].isin(['Goal', 'GoalOnPenalty']))) | 
                                 ((match_events_df['TeamToID'] == team_id) & 
                                 (match_events_df['Event'] == 'OwnGoal'))]

    first_half_goals = team_goals[team_goals['Phase'] == 1].shape[0]
    second_half_goals = team_goals[team_goals['Phase'] == 2].shape[0]
    ot_goals = team_goals[team_goals['Phase'] >= 3].shape[0]

    return pd.Series({
        'First Half': first_half_goals,
        'Second Half': second_half_goals,
        'Overtime': ot_goals
    })

def get_goal_distribution_df(file_path):
    match_stats_df = pd.read_excel(file_path, sheet_name='Match Stats')
    id_name_df = match_stats_df.drop_duplicates(subset=['TeamID', 'TeamName'])[['TeamID', 'TeamName']]

    team_ids = match_stats_df['TeamID'].unique()

    goal_distribution_df = pd.DataFrame(index=team_ids, columns=['First Half', 'Second Half', 'Overtime'])

    for team_id in team_ids:
        goal_distribution_df.loc[team_id] = get_team_goal_distribution(team_id)

    goal_distribution_df = goal_distribution_df.merge(id_name_df, left_index=True, right_on='TeamID')

    goal_distribution_df.set_index('TeamName', inplace=True)
    goal_distribution_df = goal_distribution_df[['First Half', 'Second Half', 'Overtime']]

    return goal_distribution_df