import pandas as pd
from scipy import stats


def create_subset(df, team_strength_threshold=5):
    """
    Create a subset of the DataFrame based on the team strength threshold.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing the data.
    team_strength_threshold : int, optional
        The maximum value of 'team_strength' to include in the subset (default is 5).

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing rows where 'team_strength' is less than or equal to the given threshold.
    """
    return df[df["team_strength"] <= team_strength_threshold]


def filter_data(df, position, value):
    """
    Filter the DataFrame based on position and value in the first game week.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing the data.
    position : str
        The position of the players to filter (e.g., 'Midfielder', 'Forward').
    value : float or int
        The value of the player in the first game week.

    Returns
    -------
    pandas.DataFrame
        A DataFrame filtered by the given position and value for the first game week.
    """
    return df[(df["position"] == position) & (df["value_first_gw"] == value)]


def perform_ttest(filtered_df):
    """
    Perform a t-test on the filtered DataFrame to compare total points of promoted vs non-promoted teams.

    Parameters
    ----------
    filtered_df : pandas.DataFrame
        The filtered DataFrame on which to perform the t-test. Must contain 'promoted_from_championship' and 'total_points' columns.

    Returns
    -------
    dict or None
        A dictionary with t-test statistics and group means if enough data is present, otherwise None.
        The dictionary contains:
        - 'sample_size_promoted': Number of promoted players.
        - 'sample_size_not_promoted': Number of non-promoted players.
        - 'average_score_promoted': Mean total points of promoted players.
        - 'average_score_not_promoted': Mean total points of non-promoted players.
        - 't_test': The t-statistic value.
        - 'p_value': The p-value of the t-test.
    """
    group1 = filtered_df[filtered_df["promoted_from_championship"] == 1]["total_points"]
    group2 = filtered_df[filtered_df["promoted_from_championship"] == 0]["total_points"]

    if len(group1) > 0 and len(group2) > 0:
        avg_promoted = group1.mean()
        avg_not_promoted = group2.mean()
        sample_size_promoted = len(group1)
        sample_size_not_promoted = len(group2)

        # Perform independent t-test (Welch's t-test)
        t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)

        return {
            "sample_size_promoted": sample_size_promoted,
            "sample_size_not_promoted": sample_size_not_promoted,
            "average_score_promoted": avg_promoted,
            "average_score_not_promoted": avg_not_promoted,
            "t_test": t_stat,
            "p_value": p_value,
        }
    else:
        return None


def loop_combinations(df):
    """
    Loop through unique combinations of position and value_first_gw and perform t-tests.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing the data. Must include 'position', 'value_first_gw', and 'promoted_from_championship'.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing t-test results and statistics for each position and value combination.
    """
    results = []

    unique_positions = df["position"].unique()
    unique_values = df["value_first_gw"].unique()

    for position in unique_positions:
        for value in unique_values:
            filtered_df = filter_data(df, position, value)
            result = perform_ttest(filtered_df)

            if result:  # Only append if there is valid t-test data
                result.update({"position": position, "value_first_gw": value})
                results.append(result)

    return pd.DataFrame(results)


def perform_ttest_on_df(df, team_strength_threshold=5):
    """
    Perform t-tests on the subset of the DataFrame based on team strength threshold.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing the data.
    team_strength_threshold : int, optional
        The maximum value of 'team_strength' to include in the subset (default is 5).

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing t-test results for each unique position and value combination within the subset.
    """
    df_subset = create_subset(df, team_strength_threshold)
    return loop_combinations(df_subset)
