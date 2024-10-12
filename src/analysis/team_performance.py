import pandas as pd


def load_fpl_data(season, base_url):
    """
    Load Premier League data for a specific season from a CSV file.

    Parameters
    ----------
    season : str
        The season in the format 'YYYY-YY'.
    base_url : str
        Base URL for the CSV file.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the data for the specified season.
    """
    csv_url = f"{base_url}{season}.csv"
    df = pd.read_csv(csv_url)
    df["season"] = season
    return df


def check_if_promoted(row, promoted_teams_by_season):
    """
    Check if a team was promoted from the Championship in a given season.

    Parameters
    ----------
    row : pd.Series
        A row from the DataFrame containing team and season information.
    promoted_teams_by_season : dict
        A dictionary where keys are season start years and values are lists of teams promoted in that season.

    Returns
    -------
    bool
        True if the team was promoted in that season, otherwise False.
    """
    season_start = int(row["season"][:4])
    return row["team"] in promoted_teams_by_season.get(season_start, [])


def process_fpl_data(combined_df, promoted_teams_by_season):
    """
    Process the combined DataFrame to filter promoted teams and sort by total points.

    Parameters
    ----------
    combined_df : pd.DataFrame
        DataFrame containing combined data for all seasons.
    promoted_teams_by_season : dict
        A dictionary where keys are season start years and values are lists of teams promoted in that season.

    Returns
    -------
    pd.DataFrame
        A processed DataFrame containing only promoted teams sorted by total points.
    """
    combined_df["promoted_from_championship"] = combined_df.apply(
        lambda row: check_if_promoted(row, promoted_teams_by_season), axis=1
    )

    combined_df = combined_df[combined_df["promoted_from_championship"]].sort_values(
        "total_points", ascending=False
    )

    column_order = [
        "team",
        "season",
        "total_points",
        "gk_points",
        "def_points",
        "mid_points",
        "fwd_points",
        "goals_scored",
        "assists",
        "clean_sheets",
    ]

    combined_df = combined_df[column_order]

    rename_columns = {
        "team": "Team",
        "season": "Season",
        "total_points": "Total Points",
        "gk_points": "GK Points",
        "def_points": "DEF Points",
        "mid_points": "MID Points",
        "fwd_points": "FWD Points",
        "goals_scored": "Goals Scored",
        "assists": "Assists",
        "clean_sheets": "Clean Sheets",
    }

    combined_df = combined_df.rename(columns=rename_columns)

    return combined_df


def load_and_process_fpl_data(
    seasons, base_url, promoted_teams_by_season, export_csv=False
):
    """
    Load and process Premier League data from CSV files for specified seasons.

    Parameters
    ----------
    seasons : list of str
        List of seasons in the format 'YYYY-YY'.
    base_url : str
        Base URL for the CSV files.
    promoted_teams_by_season : dict
        A dictionary where keys are season start years and values are lists of teams promoted in that season.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing teams promoted from the Championship, sorted by total points,
        with columns renamed for clarity.
    """
    df_list = []

    for season in seasons:
        df_list.append(load_fpl_data(season, base_url))

    combined_df = pd.concat(df_list, ignore_index=True)

    combined_df = process_fpl_data(combined_df, promoted_teams_by_season)

    if export_csv:
        combined_df.to_csv(
            f"data/analysis/team_performance_fpl_points.csv", index=False
        )

    return combined_df
