import pandas as pd

from src.analysis.championship_player_performance import (
    format_dataframe,
    get_top_ranked_players,
    match_and_merge_with_fpl_data,
    process_promotions,
)
from src.data_prep.join_data import (
    load_combine_championship_assists_data,
    load_combine_championship_goals_data,
)
from src.tools.yaml_loader import load_yaml_file

# Load promotion/relegation yaml
file_path = "conf/promoted_teams_by_season.yaml"
promoted_teams_by_season = load_yaml_file(file_path)


# Goal scorers
season_years = [
    "2015-2016",
    "2016-2017",
    "2017-2018",
    "2018-2019",
    "2019-2020",
    "2020-2021",
    "2021-2022",
    "2022-2023",
    "2023-2024",
]

df_goals = load_combine_championship_goals_data(
    season_years=season_years, export_csv=True
)
df_assists = load_combine_championship_assists_data(
    season_years=season_years, export_csv=True
)

# Filter promoted players
df_goals = process_promotions(df_goals, promoted_teams_by_season)
df_assists = process_promotions(df_assists, promoted_teams_by_season)

# Join with FPL data
fpl_df = pd.read_csv("data/fpl_data/joined/seasons_joined.csv")
df_goals = match_and_merge_with_fpl_data(df=df_goals, fpl_df=fpl_df)
df_assists = match_and_merge_with_fpl_data(df=df_assists, fpl_df=fpl_df)

# Reformat and tidy output
df_goals = format_dataframe(df=df_goals, metric="Goals", export_csv=True)
df_assists = format_dataframe(df=df_assists, metric="Assists", export_csv=True)
