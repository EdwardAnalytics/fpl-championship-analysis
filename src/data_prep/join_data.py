import pandas as pd
from src.tools.yaml_loader import load_yaml_file

# Load parameters
file_path = "conf/parameters.yaml"
parameters = load_yaml_file(file_path)
number_gameweeks_played_min = parameters["number_gameweeks_played_min"]


def load_combine_fpl_data(season_years, export_csv=False):
    # Initialize an empty list to store the DataFrames
    data_frames = []

    # Loop through the season years and read each CSV file using f-strings
    for season in season_years:
        file_path = f"data/fpl_data/{season}.csv"
        df = pd.read_csv(file_path)

        # Filter to only players who have played more than the specified number of games
        df = df[df["count_gws_min_minutes"] >= number_gameweeks_played_min]
        data_frames.append(df)

    # Concatenate all DataFrames into a single DataFrame
    df = pd.concat(data_frames, ignore_index=True)
    df["season_start"] = df["season"].str[:4].astype(int)

    # Concatenate 'Name' and 'Season' columns
    df["name_season"] = df["name"] + " (" + df["season"] + ")"

    if export_csv:
        df.to_csv("data/fpl_data/joined/seasons_joined.csv", index=False)
    return df
