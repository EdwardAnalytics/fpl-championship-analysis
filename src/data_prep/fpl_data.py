import pandas as pd
import numpy as np


def fetch_data_from_url(url, encoding="utf-8"):
    """
    Fetch data from a URL and return a DataFrame.

    Parameters
    ----------
    url : str
        The URL to fetch data from.
    encoding : str, optional
        The encoding to use for reading the data (default is 'utf-8').

    Returns
    -------
    df : pd.DataFrame
        The DataFrame containing the fetched data.
    """
    df = pd.read_csv(url, encoding=encoding)
    return df


def process_fpl_data(df, season_year):
    """
    Process the FPL data by merging and calculating columns.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing raw FPL data.
    season_year : str
        The season year in the format "YYYY-YY".

    Returns
    -------
    summary_df : pd.DataFrame
        A DataFrame containing the processed and aggregated FPL data.
    """
    if "position" not in df.columns:
        df_players = fetch_data_from_url(
            f"https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/{season_year}/players_raw.csv"
        )
        df_players = df_players[["id", "team", "element_type"]]
        df = df.merge(df_players, left_on="element", right_on="id", how="left")

        df_teams = fetch_data_from_url(
            "https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/master_team_list.csv"
        )
        df_teams = df_teams[df_teams["season"] == season_year]
        df = df.merge(df_teams, on="team", how="left")

        df.rename(columns={"team": "team_id", "team_name": "team"}, inplace=True)

        df["position"] = (
            df["element_type"]
            .map({1: "GK", 2: "DEF", 3: "MID", 4: "FWD"})
            .fillna("Unknown")
        )

    df["gk_points"] = df["total_points"].where(df["position"] == "GK", 0)
    df["def_points"] = df["total_points"].where(df["position"] == "DEF", 0)
    df["mid_points"] = df["total_points"].where(df["position"] == "MID", 0)
    df["fwd_points"] = df["total_points"].where(df["position"] == "FWD", 0)

    max_gw = df["GW"].max()
    df_max_gw = df[df["GW"] == max_gw]

    # Identify players present in Gameweek 1
    players_gw1 = df[df["GW"] == 1]["name"].unique()

    # Filter the main DataFrame for players who were in Gameweek 1
    df = df[df["name"].isin(players_gw1)]

    player_df = (
        df.groupby("name")
        .agg(
            total_points=("total_points", "sum"),
            goals_scored=("goals_scored", "sum"),
            assists=("assists", "sum"),
            clean_sheets=("clean_sheets", "sum"),
            yellow_cards=("yellow_cards", "sum"),
            red_cards=("red_cards", "sum"),
            goals_conceded=("goals_conceded", "sum"),
            own_goals=("own_goals", "sum"),
            penalties_missed=("penalties_missed", "sum"),
            penalties_saved=("penalties_saved", "sum"),
            saves=("saves", "sum"),
            bonus_points=("bonus", "sum"),
        )
        .reset_index()
    )

    # Identify the minimum gameweek and corresponding value
    min_gameweek_info = df.loc[df.groupby("name")["GW"].idxmin()][["name", "value"]]

    # Merge the minimum gameweek information with the aggregated data
    player_df = pd.merge(
        player_df, min_gameweek_info, on="name", how="left", suffixes=("", "_min")
    )
    player_df = player_df.rename(columns={"value": "value_first_gw"})

    player_df = player_df.sort_values(by="total_points", ascending=False).reset_index(
        drop=True
    )

    # Perform the left join with player_df on 'name'
    player_df = player_df.merge(
        df_max_gw[["name", "position", "team"]], on="name", how="left"
    )

    column_order = [
        "name",
        "team",
        "total_points",
        "position",
        "goals_scored",
        "assists",
        "clean_sheets",
        "yellow_cards",
        "red_cards",
        "goals_conceded",
        "own_goals",
        "penalties_missed",
        "penalties_saved",
        "saves",
        "bonus_points",
        "value_first_gw",
    ]

    # Reorder the DataFrame columns
    player_df = player_df[column_order]

    # Remove _ from names
    player_df["name"] = player_df["name"].str.replace("_", " ")
    player_df["name"] = player_df["name"].str.replace(r"\s\d+$", "", regex=True)

    return player_df


def get_fpl_player_data_aggregated(season_year):
    """
    Fetch and process FPL player data for the given season year.

    Parameters
    ----------
    season_year : str
        The season year in the format "YYYY-YY".

    Returns
    -------
    summary_df : pd.DataFrame
        A DataFrame containing the aggregated FPL player data.
    """
    vaastav_url = f"https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/{season_year}/gws/merged_gw.csv"
    season_start = int(season_year[:4])

    # Set encoding based on season start year
    encoding = "utf-8"

    df = fetch_data_from_url(vaastav_url, encoding=encoding)
    player_df = process_fpl_data(df, season_year)

    return player_df


def fetch_data_for_season(season):
    """Fetch player and team data for a specific season."""
    current_season = f"{season}-{str(season + 1)[2:]}"

    team_data_url = f"https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/{current_season}/teams.csv"

    try:
        player_data = get_fpl_player_data_aggregated(current_season)
        team_data = pd.read_csv(team_data_url)
        return player_data, team_data, current_season
    except Exception as e:
        print(f"Error fetching data for season {current_season}: {e}")
        return None, None, None


def process_team_data(team_data):
    """Process and rename columns of the team data."""
    team_data_selected = team_data[
        [
            "name",
            "strength",
            "strength_overall_home",
            "strength_overall_away",
            "strength_attack_home",
            "strength_attack_away",
            "strength_defence_home",
            "strength_defence_away",
        ]
    ]
    team_data_selected = team_data_selected.rename(
        columns={
            "strength": "team_strength",
            "strength_overall_home": "team_strength_overall_home",
            "strength_overall_away": "team_strength_overall_away",
            "strength_attack_home": "team_strength_attack_home",
            "strength_attack_away": "team_strength_attack_away",
            "strength_defence_home": "team_strength_defence_home",
            "strength_defence_away": "team_strength_defence_away",
        }
    )
    return team_data_selected


def merge_data(player_data, team_data_selected, season):
    """Merge player and team data for a specific season and add season column."""
    team_data_selected = team_data_selected.rename(columns={"name": "team"})
    merged_data = pd.merge(
        player_data, team_data_selected, how="left", left_on="team", right_on="team"
    )
    merged_data["season"] = season
    return merged_data


def process_and_merge_season_data(start_season, end_season):
    """Process and save data for multiple seasons, each in its own CSV file."""
    for season in range(start_season, end_season + 1):
        player_data, team_data, current_season = fetch_data_for_season(season)
        if player_data is not None and team_data is not None:
            team_data_selected = process_team_data(team_data)
            season_data = merge_data(player_data, team_data_selected, current_season)

            encoding = "utf-8"

            # Save the data to a CSV file for each season
            file_path_player = f"data/fpl_data/{current_season}.csv"
            season_data.to_csv(file_path_player, index=False, encoding=encoding)
            print(f"CSV file '{file_path_player}' has been created successfully.")
        else:
            print(f"No data available for season {current_season}.")


def get_season_string(season_start):
    """
    Generate a season string in the format YYYY-YY.

    Parameters
    ----------
    season_start : int
        The start year of the season. Must be a four-digit integer (e.g., 2023).

    Returns
    -------
    season_string : str
        The season string in the format "YYYY-YY".

    Raises
    ------
    ValueError
        If season_start is not a four-digit integer.
    """
    if not (isinstance(season_start, int) and len(str(season_start)) == 4):
        raise ValueError("season_start must be a four-digit integer (e.g., 2023).")

    season_end = season_start + 1
    season_end_string = str(season_end)[-2:]
    return f"{season_start}-{season_end_string}"
