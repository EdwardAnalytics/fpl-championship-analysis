from src.data_prep.join_data import load_combine_fpl_data
from src.analysis.ttest import perform_ttest_on_df, format_result

from src.tools.yaml_loader import load_yaml_file

# Load parameters
file_path = "conf/parameters.yaml"
parameters = load_yaml_file(file_path)
number_gameweeks_played_min = parameters["number_gameweeks_played_min"]

season_years = [
    "2016-17",
    "2017-18",
    "2018-19",
    "2019-20",
    "2020-21",
    "2021-22",
    "2022-23",
    "2023-24",
]

# Load and save data
df = load_combine_fpl_data(season_years=season_years, export_csv=True)

# Filter to only players who have played more than the specified
df = df[df["count_gws_min_minutes"] >= number_gameweeks_played_min]

# Drop Cole Palmer anomoly season
df = df.drop(df[(df["name"] == "Cole Palmer") & (df["season"] == "2023-24")].index)

# Perform t-tests
team_strength_threshold = 3
result_df = perform_ttest_on_df(df, team_strength_threshold=team_strength_threshold)

# Sample size filter
sample_size_threshold = 20
result_df = format_result(
    result_df=result_df, sample_size_threshold=sample_size_threshold, export_csv=True
)
