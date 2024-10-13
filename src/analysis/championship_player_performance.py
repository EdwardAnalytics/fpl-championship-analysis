import pandas as pd
from fuzzywuzzy import process, fuzz

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

    # Drop the rank column
    top_ranked.drop(columns=["Rank"], inplace=True)

    return top_ranked


from fuzzywuzzy import process, fuzz
import pandas as pd


def get_best_match(player_name, choices, scorer, threshold=70):
    """
    Get the best fuzzy match for a player name.

    Parameters
    ----------
    player_name : str
        The name of the player to match.
    choices : list of str
        A list of player names to match against.
    scorer : callable
        The scoring function from fuzzywuzzy to use for matching.
    threshold : int, optional
        The minimum score required for a match to be considered valid (default is 70).

    Returns
    -------
    str or None
        The best match if the score is above the threshold; otherwise, None.
    """
    match, score = process.extractOne(player_name, choices, scorer=scorer)
    return match if score >= threshold else None


def fuzzy_match_players(df, fpl_df, season, scorer):
    """
    Fuzzy match players in the current season's goals DataFrame with FPL player names.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing player goals data with a 'next_season_start' column.
    fpl_df : pandas.DataFrame
        DataFrame containing FPL data with a 'season_start' column.
    season : str
        The season to filter the DataFrames on.
    scorer : callable
        The scoring function from fuzzywuzzy to use for matching.

    Returns
    -------
    pandas.DataFrame, pandas.DataFrame
        The current season's goals DataFrame with fuzzy matches and the filtered FPL DataFrame.
    """
    # Filter df for the current season
    current_season_goals = df[df["next_season_start"] == season].copy()

    # Get unique player names from fpl_df for the current season
    fpl_season_data = fpl_df[fpl_df["season_start"] == season]
    fpl_player_names = fpl_season_data["name"].unique()

    # Apply the fuzzy match function to the current season's goals DataFrame
    current_season_goals["fuzzy_match"] = current_season_goals["Player"].apply(
        get_best_match, choices=fpl_player_names, scorer=scorer
    )

    return current_season_goals, fpl_season_data


def merge_dataframes(season_goals_df, fpl_season_data):
    """
    Merge the fuzzy matched goals DataFrame with FPL data.

    Parameters
    ----------
    season_goals_df : pandas.DataFrame
        DataFrame containing the current season's goals with fuzzy matched player names.
    fpl_season_data : pandas.DataFrame
        DataFrame containing FPL player data for the current season.

    Returns
    -------
    pandas.DataFrame
        Merged DataFrame containing both goals and FPL player data.
    """
    merged_season = pd.merge(
        season_goals_df,
        fpl_season_data[
            [
                "name",
                "team",
                "season_start",
                "season",
                "total_points",
                "goals_scored",
                "assists",
                "position",
            ]
        ],
        how="left",
        left_on=["fuzzy_match", "Team", "next_season_start"],
        right_on=["name", "team", "season_start"],
    )

    # Drop the fuzzy_match column if you don't need it anymore
    merged_season.drop(columns=["fuzzy_match"], inplace=True)

    return merged_season


def match_and_merge_with_fpl_data(df, fpl_df, scorer=process.fuzz.token_sort_ratio):
    """
    Process all unique seasons and return a concatenated DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing player goals data with a 'next_season_start' column.
    fpl_df : pandas.DataFrame
        DataFrame containing FPL data with a 'season_start' column.
    scorer : callable
        The scoring function from fuzzywuzzy to use for matching.

    Returns
    -------
    pandas.DataFrame
        A concatenated DataFrame containing all seasons' merged data.
    """
    season_dfs = []
    unique_seasons = df["next_season_start"].unique()

    for season in unique_seasons:
        current_season_goals, fpl_season_data = fuzzy_match_players(
            df, fpl_df, season, scorer
        )
        merged_season = merge_dataframes(current_season_goals, fpl_season_data)
        season_dfs.append(merged_season)

    # Concatenate all the season DataFrames into one
    return pd.concat(season_dfs, ignore_index=True)


def reorder_columns(df, required_cols):
    """
    Reorder the DataFrame columns according to required_cols.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    required_cols : list
        List of columns to retain in the specified order.

    Returns
    -------
    pd.DataFrame
        The reordered DataFrame.
    """
    return df[required_cols]


def change_season_format(df):
    """
    Change the Championship Season format from 'YYYY-YYYY' to 'YYYY-YY'.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.

    Returns
    -------
    pd.DataFrame
        The DataFrame with updated season format.
    """
    df["Season"] = df["Season"].apply(
        lambda x: f"{x.split('-')[0]}-{x.split('-')[1][2:]}"
    )
    return df


def rename_columns(df, rename_dict):
    """
    Rename columns in the DataFrame according to rename_dict.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    rename_dict : dict
        Dictionary where keys are old column names and values are new column names.

    Returns
    -------
    pd.DataFrame
        The DataFrame with renamed columns.
    """
    return df.rename(columns=rename_dict)


def remove_nulls(df, column_name):
    """
    Remove rows from the DataFrame where the specified column has null values.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    column_name : str
        The name of the column to check for nulls.

    Returns
    -------
    pd.DataFrame
        The DataFrame without nulls in the specified column.
    """
    return df.dropna(subset=[column_name])


def format_dataframe(df, metric, export_csv=False):
    """
    Format the DataFrame by reordering columns, changing season format,
    renaming columns, and removing rows with null values in the specified column.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame to format.

    Returns
    -------
    pd.DataFrame
        The formatted DataFrame.
    """
    # Step 1: Reorder columns
    required_cols = [
        "Player",
        "Team",
        "position",
        "Season",
        metric,
        "season",
        "total_points",
        "goals_scored",
        "assists",
    ]
    df = reorder_columns(df, required_cols)

    # Sort
    df = df.sort_values(metric, ascending=False)

    # Step 2: Change the Championship Season format
    df = change_season_format(df)

    # Step 3: Rename columns
    rename_dict = {
        "Season": "Championship Season",
        "position": "Position",
        metric: f"Championship {metric}",
        "season": "FPL Season",
        "total_points": "FPL Points",
        "goals_scored": "FPL Goals",
        "assists": "FPL Assists",
    }
    df = rename_columns(df, rename_dict)

    # Step 4: Remove rows where FPL Points is null
    df = remove_nulls(df, "FPL Points")

    # Concatenate 'Name' and 'Season' columns
    df["Player (FPL Season)"] = df["Player"] + " (" + df["FPL Season"] + ")"

    df["Player (FPL Season) - Short"] = (
        df["Player"].apply(lambda x: " ".join(x.split(" ")[1:]))
        + ": "
        + df["FPL Season"].str[-5:].replace("-","/")
    )
    df["Player (FPL Season) - Short"]=df["Player (FPL Season) - Short"].str.replace('-', '/', regex=False)


    if export_csv:
        df.to_csv(
            f"data/analysis/{metric.lower()}_championship_fpl_points.csv", index=False
        )

    return df
