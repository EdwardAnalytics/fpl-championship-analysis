from src.analysis.comparison_box_plot import filter_fpl_data, plot_boxplot
from src.tools.yaml_loader import load_yaml_file
import pandas as pd

# Load parameters
file_path = "conf/parameters.yaml"
parameters = load_yaml_file(file_path)
number_gameweeks_played_min = parameters["number_gameweeks_played_min"]

fpl_data = pd.read_csv("data/fpl_data/joined/seasons_joined.csv")
goals_championship_fpl_points = pd.read_csv(
    "data/analysis/goals_championship_fpl_points.csv"
)

# Drop Cole Palmer anomoly season
fpl_data = fpl_data.drop(
    fpl_data[
        (fpl_data["name"] == "Cole Palmer") & (fpl_data["season"] == "2023-24")
    ].index
)

fpl_data_filtered = filter_fpl_data(
    fpl_data=fpl_data, number_gameweeks_played_min=number_gameweeks_played_min
)

plot_boxplot(fpl_data=fpl_data_filtered)
