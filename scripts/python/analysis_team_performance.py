import pandas as pd
from src.tools.yaml_loader import load_yaml_file
from src.analysis.team_performance import load_and_process_fpl_data

# Load promotion/relegation yaml
file_path = "conf/promoted_teams_by_season.yaml"
promoted_teams_by_season = load_yaml_file(file_path)

seasons = [
    "2016-17",
    "2017-18",
    "2018-19",
    "2019-20",
    "2020-21",
    "2021-22",
    "2022-23",
    "2023-24",
]
base_url = "https://raw.githubusercontent.com/EdwardAnalytics/fpl-pl-table/main/data/fpl_premier_league_tables/"

combined_df = load_and_process_fpl_data(
    seasons=seasons,
    base_url=base_url,
    promoted_teams_by_season=promoted_teams_by_season,
    export_csv=True,
)
print("Team Performance Calculated")
