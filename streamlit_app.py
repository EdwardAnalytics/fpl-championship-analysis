import streamlit as st
import pandas as pd
from src.tools.app_tools import top_players_fpl_data

# Set the page configuration to wide mode
st.set_page_config(layout="wide")

# Import data
fpl_data = pd.read_csv("data/fpl_data/joined/seasons_joined.csv")
goals_championship_fpl_points = pd.read_csv(
    "data/analysis/goals_championship_fpl_points.csv"
)
assists_championship_fpl_points = pd.read_csv(
    "data/analysis/assists_championship_fpl_points.csv"
)
team_performance_fpl_points = pd.read_csv(
    "data/analysis/team_performance_fpl_points.csv"
)
welchs_ttest = pd.read_csv("data/analysis/welchs_ttest.csv")

st.title("FPL Championship Analysis")
st.markdown(
    """*How do players in teams promoted from the Chapmionship perform in their first season? Should you pick their players, or players from other teams instead?*"""
)

st.markdown("""
#### Key Findings
* In general, avoid £5.0m midfielders from newly promoted teams; consider players from others teams instead.
* There is no statistically significant difference in player performance from promoted vs existing teams at other price points or positions, by different team strengths.
* Goals and assists in the Championship don’t always translate into Fantasy Premier League (FPL) points the following season.
* Patrick Bamford had a good season in 2020/21.""")

st.markdown("""
#### Background
This analysis looks at the Fantasy Premier League (FPL) performance of players from Championship teams, in their first season after being promoted to the Premier League. See notes and caveats at the end.

The following areas are looked into:
* A comparison of players from promoted teams with players from teams already in the league.
  * Overview of differences for each price point by position ([link to t-test explanation](https://www.youtube.com)) 
  * £5.0m midfielders detail
* An exploratory data analysis of how these players perform.
  * Top performances from players in promoted teams
  * Top total team points from promoted teams
  * Championship goals and assists vs FPL Points in the following season
""")
st.divider()
st.markdown("""#### Players from Promoted Teams vs Existing Teams""")
st.divider()

welchs_ttest_p = welchs_ttest[["Position", "Value", "Avg. Score Promoted"]]
welchs_ttest_np = welchs_ttest[["Position", "Value", "Avg. Score Not Promoted"]]

welchs_ttest_p["Team"] = "Promoted"
welchs_ttest_np["Team"] = "Not Promoted"

welchs_ttest_p.rename(
    columns={"Avg. Score Promoted": "Average Total Points in a Season"}, inplace=True
)
welchs_ttest_np.rename(
    columns={"Avg. Score Not Promoted": "Average Total Points in a Season"},
    inplace=True,
)

# Row-bind the two DataFrames
welchs_ttest_rehsaped = pd.concat(
    [welchs_ttest_p, welchs_ttest_np], axis=0, ignore_index=True
)
welchs_ttest_rehsaped["Position and Value"] = (
    welchs_ttest_rehsaped["Position"]
    + ": "
    + welchs_ttest_rehsaped["Value"].fillna("0").astype(str)
)

st.bar_chart(
    welchs_ttest_rehsaped,
    x="Position and Value",
    y="Average Total Points in a Season",
    color="Team",
    stack=False,
    use_container_width=False,
    width=800,
)

# Move 'Statistically Significant' to the front and reformat
columns = ["Statistically Significant"] + [
    col for col in welchs_ttest.columns if col != "Statistically Significant"
]
welchs_ttest = welchs_ttest.reindex(columns=columns)
welchs_ttest["Statistically Significant"] = welchs_ttest[
    "Statistically Significant"
].replace("Yes", "Yes ⭐")


st.dataframe(welchs_ttest, hide_index=True)
st.text("")


# Load 5.0 mid boxplot
image_path = "assets/mid_50_boxplot.png"
st.image(image_path, use_column_width=False)


st.divider()
st.markdown("""#### Exploratory Data Analysis""")
st.divider()
st.markdown("""##### Players from Promoted Teams by Total FPL Points""")
st.text("")


position = st.selectbox(
    "Filter by Position", ["All", "GK", "DEF", "MID", "FWD"], index=0
)


# Display table
fpl_data_filtered = top_players_fpl_data(
    df=fpl_data, filter_position=position, top_n=1000
)
st.dataframe(fpl_data_filtered, hide_index=True)


st.divider()
st.markdown("""##### Promoted Teams by Total FPL Points""")
st.text("")

# Display table
team_performance_fpl_points_cleaned = team_performance_fpl_points.drop(
    columns=["Team (Season)"]
)
st.dataframe(team_performance_fpl_points_cleaned, hide_index=True)


st.markdown("""#### Notes and Caveats


Other things I assessed 
Experiemneted with different thresholds of definition for games played (mins/gws)
Built models to predict scores to see if championship flag was an important feature/significant. Similar restults to t tests.

Note this isn't looking only at players who played in the chapmionship the season before. It includes new signings that season.

We're only looking at players in teams promoted. 
Not players from promoted teams as that can be influnced by the strength of the club they are going to. 
E.g. When Tottenham signed Bale etc. This would be a seperate piece of analysis assesing the impact of signings 
from dif""")

goals_championship_fpl_points = goals_championship_fpl_points[
    goals_championship_fpl_points["Championship Goals"] >= 5
]
import streamlit as st
import pandas as pd
import altair as alt


# Create a base scatter plot
base = (
    alt.Chart(goals_championship_fpl_points)
    .mark_circle(size=60)
    .encode(
        x="Championship Goals",
        y="FPL Points",
        tooltip=[
            "Player (FPL Season)",
            "Championship Goals",
            "FPL Points",
        ],  # Tooltips for all points
    )
)

# Define points to annotate
players_to_annotate = ["Mitrović: 22/23", "Toney: 21/22", "Pukki: 19/20"]

# Create a DataFrame for annotations with specific offsets
annotations_df = goals_championship_fpl_points[
    goals_championship_fpl_points["Player (FPL Season) - Short"].isin(
        players_to_annotate
    )
]

# Create text annotations for Toney separately (offset to the left)
toney_text = (
    alt.Chart(
        annotations_df[annotations_df["Player (FPL Season) - Short"] == "Toney: 21/22"]
    )
    .mark_text(
        align="right",  # Align text to the right for Toney
        dx=-10,  # Move Toney's label to the left
        dy=-5,  # Vertical offset
        fontSize=12,
        color="white",
    )
    .encode(x="Championship Goals", y="FPL Points", text="Player (FPL Season) - Short")
)

# Create text annotations for the other players (offset to the right)
other_text = (
    alt.Chart(
        annotations_df[annotations_df["Player (FPL Season) - Short"] != "Toney: 21/22"]
    )
    .mark_text(
        align="left",  # Align text to the left for others
        dx=10,  # Move labels to the right
        dy=-5,  # Vertical offset
        fontSize=12,
        color="white",
    )
    .encode(x="Championship Goals", y="FPL Points", text="Player (FPL Season) - Short")
)

# Combine the scatter plot with the annotations
chart = base + toney_text + other_text

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)


import seaborn as sns
import matplotlib.pyplot as plt

# Sample Data
data = {
    "Binary Variable": [
        "Yes",
        "No",
        "Yes",
        "No",
        "Yes",
        "No",
        "Yes",
        "No",
        "Yes",
        "No",
    ],
    "Continuous Variable": [10, 15, 14, 10, 23, 30, 29, 24, 20, 18],
}
df = pd.DataFrame(data)

# Streamlit App
st.title("Box Plot with One Binary Variable")

# Create boxplot
plt.figure(figsize=(8, 5))
sns.boxplot(x="Binary Variable", y="Continuous Variable", data=df)
plt.title("Box Plot of Continuous Variable by Binary Variable")
plt.xlabel("Binary Variable")
plt.ylabel("Continuous Variable")


# Save plot to a buffer
import io

buf = io.BytesIO()
plt.savefig(buf, format="png")
buf.seek(0)

# Use the buffer in Streamlit to display the plot with maximum width
st.image(buf, width=800)  # Set width to a maximum of 800 pixels
