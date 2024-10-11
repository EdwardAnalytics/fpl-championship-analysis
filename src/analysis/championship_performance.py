import pandas as pd

# Create a mapping of actual team names to the ones used in the promotion dictionary
team_name_mapping = {
    "Burnley FC": "Burnley",
    "Fulham FC": "Fulham",
    "Hull City": "Hull",
    "Brighton & Hove Albion": "Brighton",
    "Huddersfield Town": "Huddersfield",
    "Middlesbrough FC": "Middlesbrough",
    "Wolverhampton Wanderers": "Wolves",
    "Sheffield United": "Sheffield Utd",
    "Leeds United": "Leeds",
    "Watford FC": "Watford",
    "Brentford FC": "Brentford",
    "Cardiff City": "Cardiff",
    "Ipswich Town": "Ipswich",
    "Nottingham Forest": "Nott'm Forest",
    "Newcastle United": "Newcastle",
    "Norwich City": "Norwich",
    "Luton Town": "Luton",
    "Leicester City": "Leicester",
    "AFC Bournemouth": "Bournemouth",
    "Southampton FC": "Southampton",
    "West Bromwich Albion": "West Brom",
}


def check_promoted_next_season(row, promoted_teams_by_season):
    """Check if a team was promoted in the next season.

    Parameters
    ----------
    row : pandas.Series
        A row from the DataFrame containing team information.
    promoted_teams_by_season : dict
        A dictionary where keys are seasons and values are lists of promoted teams.

    Returns
    -------
    int
        1 if the team was promoted next season, otherwise 0.
    """
    current_season = row["season_start"]
    next_season = current_season + 1
    team_name = row["Team"]

    # Check if the next season exists in the dictionary
    if next_season in promoted_teams_by_season:
        # Check if the team is in the promoted list for the next season
        return 1 if team_name in promoted_teams_by_season[next_season] else 0
    return 0


def process_promotions(df, promoted_teams_by_season):
    """Process team promotions by replacing team names and checking for next season promotions.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing team and season information.
    promoted_teams_by_season : dict
        A dictionary where keys are seasons and values are lists of promoted teams.

    Returns
    -------
    pandas.DataFrame
        The modified DataFrame with the new column indicating next season promotions.
    """
    # Replace team names using the mapping
    df["Team"] = df["Team"].replace(team_name_mapping)

    # Apply the function to create the new column
    df["promoted_next_season"] = df.apply(
        check_promoted_next_season,
        axis=1,
        promoted_teams_by_season=promoted_teams_by_season,
    )

    # Get only promoted players
    df = df[df["promoted_next_season"] == 1]

    # Add next season start year
    df["next_season_start"] = df["season_start"] + 1

    # Remove latest season as we do not have this years fpl data
    # Find the maximum value in the 'season_start' column
    max_season = df["season_start"].max()

    # Remove rows where 'season_start' is the maximum value
    df = df[df["season_start"] != max_season]

    return df


def get_top_ranked_players(df, metric, top_n=25):
    """Get top ranked players based on a specified metric, including ties, using a Rank column.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing player information.
    metric : str, optional
        The name of the column to rank by (default is 'Goals').
    top_n : int, optional
        The number of top entries to return based on the specified metric (default is 25).

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the top ranked players based on the specified metric.
    """
    # Create a Rank column based on the specified metric
    df["Rank"] = df[metric].rank(method="min", ascending=False)

    # Filter for the top N ranked players (including ties)
    top_ranked = df[df["Rank"] <= top_n]

    # Optional: Sort the top ranked players by the specified metric for better readability
    top_ranked = top_ranked.sort_values(by=metric, ascending=False)

    return top_ranked
