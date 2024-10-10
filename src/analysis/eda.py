import pandas as pd


def filter_players_fpl(
    df,
    position,
    value_first_gw,
    team_strength_threshold,
    promoted_from_championship=None,
    head=None,
):
    """
    Filters the dataframe based on specified conditions for players, selects relevant columns,
    and sorts the result by total points. Optionally returns the top X rows.

    Parameters
    ----------
    df : pandas.DataFrame
        The input dataframe containing player data.
    position : str
        The player's position to filter (e.g., 'FWD').
    value_first_gw : int
        The player's value for the first game week.
    promoted_from_championship : int, optional
        Whether the player was promoted from the championship (1 for yes, 0 for no).
        If None, this filter is ignored.
    team_strength_threshold : int
        The strength rating of the player's team (e.g., 1).
    head : int, optional
        Number of top rows to return after sorting by total points. If None, returns all rows (default is None).

    Returns
    -------
    pandas.DataFrame
        A filtered and sorted dataframe containing players based on the given criteria.
    """

    # Start with a base filter
    df_filtered = df[
        (df["position"] == position)
        & (df["value_first_gw"] == value_first_gw)
        & (df["team_strength"] <= team_strength_threshold)
    ]

    # Apply promoted_from_championship filter if specified
    if promoted_from_championship is not None:
        df_filtered = df_filtered[
            df_filtered["promoted_from_championship"] == promoted_from_championship
        ]

    # Select relevant columns
    df_filtered = df_filtered[
        [
            "name_season",
            "team",
            "total_points",
            "goals_scored",
            "promoted_from_championship",
        ]
    ]

    # Sort by total points
    df_filtered = df_filtered.sort_values(by="total_points", ascending=False)

    # Return top X rows if head is provided, otherwise return all rows
    if head is not None:
        return df_filtered.head(head)

    return df_filtered
