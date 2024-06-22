import pandas as pd


def load_and_preprocess_data(file_path):
    match_stats = pd.read_excel(file_path, sheet_name='Match Stats')

    stats_to_sum = [
        'Goals', 'Attempts on target', 'Total Attempts', 'Attempts blocked',
        'Passes completed', 'Goals conceded', 'Fouls committed', 'Tackles', 'Saves'
    ]
    stats_to_average = ['Ball Possession', 'Passes accuracy']

    sum_stats = match_stats[match_stats['StatsName'].isin(stats_to_sum)]
    avg_stats = match_stats[match_stats['StatsName'].isin(stats_to_average)]

    pivot_sum_df = sum_stats.pivot_table(
        index=['TeamID', 'TeamName'],
        columns='StatsName',
        values='Value',
        aggfunc='sum'
    ).reset_index()

    pivot_avg_df = avg_stats.pivot_table(
        index=['TeamID', 'TeamName'],
        columns='StatsName',
        values='Value',
        aggfunc='mean'
    ).reset_index()

    pivot_df = pd.merge(pivot_sum_df, pivot_avg_df, on=['TeamID', 'TeamName'], how='left')

    attempts_on_target = match_stats[match_stats['StatsName'] == 'Attempts on target']

    attempts_conceded = attempts_on_target.copy()
    attempts_conceded['OpponentTeamID'] = attempts_conceded.apply(
        lambda row: match_stats[(match_stats['MatchID'] == row['MatchID']) & (match_stats['TeamID'] != row['TeamID'])]['TeamID'].values[0],
        axis=1
    )
    attempts_conceded['OpponentTeamName'] = attempts_conceded.apply(
        lambda row: match_stats[(match_stats['MatchID'] == row['MatchID']) & (match_stats['TeamID'] != row['TeamID'])]['TeamName'].values[0],
        axis=1
    )
    attempts_conceded_grouped = attempts_conceded.groupby(['TeamID', 'TeamName']).agg({'Value': 'sum'}).reset_index()
    attempts_conceded_grouped = attempts_conceded_grouped.rename(columns={'Value': 'Attempts on target conceded'})

    pivot_df = pivot_df.merge(attempts_conceded_grouped, on=['TeamID', 'TeamName'], how='left')

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
        'FirstHalfGoals': first_half_goals,
        'SecondHalfGoals': second_half_goals,
        'OTGoals': ot_goals
    })

def get_goal_distribution_df():
    match_stats_df = pd.read_excel('./static/EURO_2020_DATA.xlsx', sheet_name='Match Stats')
    id_name_df = match_stats_df.drop_duplicates(subset=['TeamID', 'TeamName'])[['TeamID', 'TeamName']]

    team_ids = match_stats_df['TeamID'].unique()

    goal_distribution_df = pd.DataFrame(index=team_ids, columns=['FirstHalfGoals', 'SecondHalfGoals', 'OTGoals'])

    for team_id in team_ids:
        goal_distribution_df.loc[team_id] = get_team_goal_distribution(team_id)

    goal_distribution_df = goal_distribution_df.merge(id_name_df, left_index=True, right_on='TeamID')

    goal_distribution_df.set_index('TeamName', inplace=True)
    goal_distribution_df = goal_distribution_df[['FirstHalfGoals', 'SecondHalfGoals', 'OTGoals']]

    print(goal_distribution_df)