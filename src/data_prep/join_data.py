import pandas as pd


def load_combine_fpl_data(season_years, export_csv=False):
    # Initialize an empty list to store the DataFrames
    data_frames = []

    # Loop through the season years and read each CSV file using f-strings
    for season in season_years:
        file_path = f"data/fpl_data/{season}.csv"
        df = pd.read_csv(file_path)
        data_frames.append(df)

    # Concatenate all DataFrames into a single DataFrame
    df = pd.concat(data_frames, ignore_index=True)
    df["season_start"] = df["season"].str[:4].astype(int)

    # Concatenate 'Name' and 'Season' columns
    df["name_season"] = df["name"] + " (" + df["season"] + ")"

    if export_csv:
        df.to_csv("data/fpl_data/joined/seasons_joined.csv", index=False)
    return df


def load_combine_championship_goals_data(season_years, export_csv=False):
    # Initialize an empty list to store the DataFrames
    data_frames = []

    # Loop through the season years and read each CSV file using f-strings
    for season in season_years:
        file_path = f"data/championship_goals/{season}.csv"
        df = pd.read_csv(file_path)
        data_frames.append(df)

    # Concatenate all DataFrames into a single DataFrame
    df = pd.concat(data_frames, ignore_index=True)
    df["season_start"] = df["Season"].str[:4].astype(int)

    if export_csv:
        df.to_csv("data/championship_goals/joined/seasons_joined.csv", index=False)
    return df


def load_combine_championship_assists_data(season_years, export_csv=False):
    # Initialize an empty list to store the DataFrames
    data_frames = []

    # Loop through the season years and read each CSV file using f-strings
    for season in season_years:
        file_path = f"data/championship_assists/{season}.csv"
        df = pd.read_csv(file_path)
        data_frames.append(df)

    # Concatenate all DataFrames into a single DataFrame
    df = pd.concat(data_frames, ignore_index=True)
    df["season_start"] = df["Season"].str[:4].astype(int)

    if export_csv:
        df.to_csv("data/championship_assists/joined/seasons_joined.csv", index=False)
    return df
