import pandas as pd
import numpy as np
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


import pandas as pd
import numpy as np


def filter_by_sample_size(result_df, sample_size_threshold):
    """
    Filter the DataFrame based on sample size threshold.

    Parameters
    ----------
    result_df : pd.DataFrame
        The DataFrame containing player statistics.
    sample_size_threshold : int
        The minimum combined sample size for promoted and not promoted players.

    Returns
    -------
    pd.DataFrame
        Filtered DataFrame containing only rows that meet the sample size threshold.
    """
    return result_df[
        result_df["sample_size_promoted"] + result_df["sample_size_not_promoted"]
        >= sample_size_threshold
    ]


def add_statistical_columns(result_df):
    """
    Add statistically significant and difference columns to the DataFrame.

    Parameters
    ----------
    result_df : pd.DataFrame
        The DataFrame to be modified.

    Returns
    -------
    pd.DataFrame
        Modified DataFrame with added columns for significance and score difference.
    """
    result_df["statistically_significant"] = np.where(
        result_df["p_value"] <= 0.05, "Yes", "No"
    )
    result_df["difference"] = (
        result_df["average_score_promoted"] - result_df["average_score_not_promoted"]
    )
    return result_df


def reorder_columns(result_df):
    """
    Reorder the columns in the DataFrame.

    Parameters
    ----------
    result_df : pd.DataFrame
        The DataFrame to be modified.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns reordered.
    """
    column_order = [
        "position",
        "value_first_gw",
        "average_score_promoted",
        "average_score_not_promoted",
        "difference",
        "statistically_significant",
        "sample_size_promoted",
        "sample_size_not_promoted",
        "t_test",
        "p_value",
    ]
    return result_df[column_order]


def set_position_order(result_df):
    """
    Set custom categorical order for the position column and sort the DataFrame.

    Parameters
    ----------
    result_df : pd.DataFrame
        The DataFrame to be modified.

    Returns
    -------
    pd.DataFrame
        Sorted DataFrame based on position and value_first_gw.
    """
    position_order = ["GK", "DEF", "MID", "FWD"]
    result_df["position"] = pd.Categorical(
        result_df["position"], categories=position_order, ordered=True
    )
    return result_df.sort_values(["position", "value_first_gw"])


def round_columns(result_df):
    """
    Round specific columns in the DataFrame to defined decimal places.

    Parameters
    ----------
    result_df : pd.DataFrame
        The DataFrame to be modified.

    Returns
    -------
    pd.DataFrame
        DataFrame with specified columns rounded.
    """
    result_df["average_score_promoted"] = result_df["average_score_promoted"].round(1)
    result_df["average_score_not_promoted"] = result_df[
        "average_score_not_promoted"
    ].round(1)
    result_df["difference"] = result_df["difference"].round(1)
    result_df["p_value"] = result_df["p_value"].round(3)
    result_df["t_test"] = result_df["t_test"].round(2)
    return result_df


def rename_columns(result_df):
    """
    Rename specific columns in the DataFrame.

    Parameters
    ----------
    result_df : pd.DataFrame
        The DataFrame to be modified.

    Returns
    -------
    pd.DataFrame
        DataFrame with renamed columns.
    """
    column_rename_dict = {
        "position": "Position",
        "value_first_gw": "Value",
        "average_score_promoted": "Avg. Score Promoted",
        "average_score_not_promoted": "Avg. Score Not Promoted",
        "difference": "Difference",
        "statistically_significant": "Statistically Significant",
        "sample_size_promoted": "Num. Players Promoted",
        "sample_size_not_promoted": "Num. Players Not Promoted",
        "t_test": "T-Test",
        "p_value": "P-Value",
    }
    return result_df.rename(columns=column_rename_dict)


def format_result(result_df, sample_size_threshold=20, export_csv=False):
    """
    Format the result DataFrame by filtering, adding columns, sorting, rounding, and renaming.

    Parameters
    ----------
    result_df : pd.DataFrame
        The DataFrame containing player statistics to be formatted.
    sample_size_threshold : int, optional
        The minimum combined sample size for promoted and not promoted players (default is 20).

    Returns
    -------
    pd.DataFrame
        Formatted DataFrame ready for analysis and output.
    """
    result_df = filter_by_sample_size(result_df, sample_size_threshold)
    result_df = add_statistical_columns(result_df)
    result_df = reorder_columns(result_df)
    result_df = set_position_order(result_df)
    result_df = round_columns(result_df)
    result_df = rename_columns(result_df)

    if export_csv:
        # Save to CSV
        result_df.to_csv("data/analysis/welchs_ttest.csv", index=False)

    return result_df
