import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from src.tools.yaml_loader import load_yaml_file


def filter_fpl_data(fpl_data, number_gameweeks_played_min):
    """
    Filter FPL data for midfield players with specific conditions.

    Parameters
    ----------
    fpl_data : DataFrame
        The DataFrame containing FPL player data.
    number_gameweeks_played_min : int
        Minimum number of gameweeks played to filter players.

    Returns
    -------
    DataFrame
        Filtered DataFrame of midfield players.
    """
    # Filter for midfield players with value_first_gw of 50
    fpl_data_filtered = fpl_data[
        (fpl_data["value_first_gw"] == 50) & (fpl_data["position"] == "MID")
    ]

    # Filter to only players who have played more than the specified number of gameweeks
    fpl_data_filtered = fpl_data_filtered[
        fpl_data_filtered["count_gws_min_minutes"] >= number_gameweeks_played_min
    ]

    return fpl_data_filtered


def plot_boxplot(fpl_data):
    """
    Create and save a boxplot comparing total points of promoted vs not promoted players.

    Parameters
    ----------
    fpl_data : DataFrame
        The DataFrame containing filtered FPL player data.
    """
    # Set font properties to match Streamlit
    plt.rcParams["font.family"] = "sans-serif"  # Use a sans-serif font
    plt.rcParams["font.sans-serif"] = "Arial"
    plt.rcParams["font.size"] = 12  # Set a default font size

    plt.figure(figsize=(3, 6))

    # Create the boxplot with light grey boxes and black lines
    sns.boxplot(
        data=fpl_data,
        x="promoted_from_championship",
        y="total_points",
        flierprops={"marker": "x"},
        color="lightgrey",
        boxprops=dict(edgecolor="black"),  # Black edges for the box
        medianprops=dict(color="black"),  # Black median line
        whiskerprops=dict(color="black"),  # Black whiskers
        capprops=dict(color="black"),
    )  # Black caps on the whiskers

    # Relabel the x and y axes
    plt.xlabel("")
    plt.ylabel("Total Points")

    # Replace 0 with 'Not Promoted' and 1 with 'Promoted' on the x-axis
    plt.xticks(ticks=[0, 1], labels=["Not Promoted", "Promoted"])

    # Add grey horizontal gridlines
    plt.grid(axis="y", color="grey", linewidth=0.5)

    # Save the plot
    plt.savefig("assets/mid_50_boxplot.png", bbox_inches="tight")
