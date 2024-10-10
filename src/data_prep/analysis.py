import pandas as pd


def load_combine_fpl_data(season_years):
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
    return df
