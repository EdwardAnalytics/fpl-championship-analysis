import pandas as pd
from src.analysis.championship_player_performance import get_top_ranked_players


def top_players_fpl_data(df, filter_position, filter_value_first_gw, top_n):
    """
    Filter FPL data by player position and return the top ranked players based on total points,
    with renamed columns and calculated points per game.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing FPL player data.
    filter_position : str
        The player position to filter by (e.g., 'GK', 'DEF', 'MID', 'FWD'). Use 'All' for all positions.
    top_n : int
        The number of top-ranked players to return based on total points.

    Returns
    -------
    pandas.DataFrame
        A filtered and renamed DataFrame with selected columns, including calculated total points per game.

    Notes
    -----
    - Assumes that the DataFrame contains columns like 'name', 'season', 'position', 'team', 'total_points',
      'goals_scored', 'assists', 'saves', and 'goals_conceded'.
    - The 'total_points_per_38' column is calculated as total points divided by 38, rounded to 1 decimal place.
    """

    # Filter data by position and whether promoted from championship
    if filter_position == "All":
        df_filtered = df[df["promoted_from_championship"] == 1]
    else:
        df_filtered = df[
            (df["position"] == filter_position)
            & (df["promoted_from_championship"] == 1)
        ]

    # Filter by the value range selected using the slider
    df_filtered = df_filtered[
        (df_filtered["value_first_gw"] >= 10 * filter_value_first_gw[0])
        & (df_filtered["value_first_gw"] <= 10 * filter_value_first_gw[1])
    ]

    # Get top N ranked players by total points
    df_filtered = get_top_ranked_players(
        df=df_filtered, metric="total_points", top_n=top_n
    )

    # Calculate total points per 38 games
    df_filtered["total_points_per_38"] = round(df_filtered["total_points"] / 38, 1)

    # Select specific columns
    df_filtered = df_filtered[
        [
            "name",
            "season",
            "total_points",
            "position",
            "team",
            "value_first_gw",
            "total_points_per_38",
            "goals_scored",
            "assists",
            "saves",
            "goals_conceded",
            "minutes_played",
        ]
    ]

    # Create the renaming dictionary
    column_rename_dict = {
        "name": "Player",
        "position": "Position",
        "season": "Season",
        "team": "Team",
        "value_first_gw": "Value",
        "total_points": "Total Points",
        "total_points_per_38": "Avg. Points per Game*",
        "goals_scored": "Goals",
        "assists": "Assists",
        "goals_conceded": "Goals Conceded",
        "minutes_played": "Minutes Played",
    }

    # Rename columns
    df_filtered = df_filtered.rename(columns=column_rename_dict)

    return df_filtered
