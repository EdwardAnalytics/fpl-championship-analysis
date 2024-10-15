import streamlit as st
import pandas as pd
from src.tools.app_tools import top_players_fpl_data
import base64
import altair as alt

from src.tools.yaml_loader import load_yaml_file


# Load parameters
file_path = "conf/parameters.yaml"
parameters = load_yaml_file(file_path)
number_gameweeks_played_min = parameters["number_gameweeks_played_min"]
minutes_played_gameweek_min = parameters["minutes_played_gameweek_min"]

# Set the page configuration
st.set_page_config(
    page_title="FPL Championship Analysis",
    page_icon=":soccer:",  # layout="wide"
)

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
    """How do players from newly promoted Championship teams perform in their first Premier League season? Should you choose players from these teams for your Fantasy Premier League team, or should you opt for players from teams already in the league? Are there any statistical differences between players from these two types of teams?
    """
)


# Add github link and logo
LOGO_IMAGE = "assets//pwt.png"

st.markdown(
    """
    <style>
    .container {
        display: flex;
    }
    .logo-text {
        font-weight: 0 !important;
        font-size: 15px !important;
        padding-top: 0px !important;
        margin-left: 0px;
        font-style: italic; 
    }
    .logo-img {
        float:right;
        width: 28px;
        height: 28px;
        margin-right: 8px; 
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:assets//pwt.png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
        <p class="logo-text"><a href="https://github.com/EdwardAnalytics/fpl-championship-analysis">GitHub Repo</a></p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.text("")
st.divider()
st.markdown("""
### Background
At the start of every season, I like to identify standout players from newly promoted Championship teams who played a key role in their team's promotion, with the hope that their skills will translate to Premier League success and boost my Fantasy Premier League (FPL) performance.

I've often wondered if there's any statistical difference between these players and those from teams already established in the Premier League.

This analysis investigates that question by examining the FPL performance of players from Championship teams in their first Premier League season after being promoted. The following areas are explored:

* Comparison of players from promoted teams vs. established Premier League teams:
  * Average total points in a season by position and value
  * Statistical significance testing (t-test)
  * £5.0m Midfielders total points disbutrion
* Exploratory data analysis:
  * Comparison of FPL points with Championship goals and assists from the previous season
  * Forwards: Championship Goals vs. FPL points vs. FPL Value
  * Top players from promoted teams by total FPL points
  * Promoted teams by total FPL points
* Data collection methodology
* Key findings/TL;DR
* Notes and caveats
""")

st.text("")
st.divider()
key_findings = """
### Key Findings/TL;DR
* Overall, there are limited significant performance differences between players from promoted teams and similarly priced or positioned players from teams already in the league.
* However, in general, it is best to avoid £5.0m midfielders from promoted teams at the start of the season; instead, consider options from other teams. This group shows a statistically significant difference in performance.
* Players who score more goals in the championship do get more FPL points the first season after promotion with their team. However, this is reflected in the players' value, with high scorers costing more.
*Note: This analysis focuses on the start of the season; some players, such as Buonanotte, may exceed expectations as the season progresses and become viable transfer options.*       
            """
st.markdown(key_findings)

st.divider()


st.markdown(f"""### Players from Promoted Teams vs Existing Teams
* This section includes only players who have played at least {minutes_played_gameweek_min} minutes in {number_gameweeks_played_min} games.
* "Value" refers to the player's value at the start of the season.
* The analysis compares players from teams with a strength of 3 or below; similar results are observed when considering all team strengths.
* Data is based on completed FPL seasons from 2016/17 to 2023/24.
*Cole Palmer's data for the 2023/24 season has been excluded as an anomaly. He was valued at £5.0m and scored the most FPL points that season, but this exclusion has minimal impact on the overall analysis.*        """)
st.text("")
st.markdown("""
#### Average Total Points in a Season by Position and Value
The graph below illustrates the differences in FPL scores between players from promoted and non-promoted teams across various positions and values. The only statistically significant difference is observed among midfielders valued at £5.0m, where players in non promoted teams score, on average, 8.6 points higher than players in promoted teams (P = 0.049).
""")


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
    width=650,
)
st.text("")
st.markdown("""
#### Testing Statistical Significance
The table below illustrates the differences between players from promoted and non-promoted teams across various positions and values.
            
This analysis shows that £5.0m midfielders are the only statistically significant group. While there are differences across various groups, these are not statistically significant. Therefore, it is advisable to avoid £5.0m midfielders from promoted teams in favour of players from non-promoted teams. Additionally, the promotion status of a club does not significantly impact player selection at other values and positions.

A statistical test, specifically Welch's t-test, has been conducted to identify which differences are statistically significant.

Further resources on the statistical test carried out are as follows:
* [StatsCast: What is a t-test?](https://www.youtube.com/watch?v=0Pd3dc1GcHc)
* [StatQuest: Using Linear Models for t-tests and ANOVA](https://www.youtube.com/watch?v=NF5_btOaCig)
* [Welch's t-test](https://en.wikipedia.org/wiki/Welch%27s_t-test)
        
            """)


# Move 'Statistically Significant' to the front and reformat
columns = ["Statistically Significant"] + [
    col for col in welchs_ttest.columns if col != "Statistically Significant"
]
# Rename colums:
welchs_ttest = welchs_ttest.reindex(columns=columns)
welchs_ttest["Statistically Significant"] = welchs_ttest[
    "Statistically Significant"
].replace("Yes", "Yes ⭐")


st.dataframe(
    welchs_ttest,
    hide_index=True,
)
st.text("")
st.markdown("""
#### £5.0m Midfielders Total Points Disbutrion
The chart below shows the spread and skewness of the total points across a season for midfielders valued at £5.0m at the start of the season. This is the only statistically significant group.

Overall, players from promoted teams tend to have lower total points, as indicated by lower median and quartile values. However, players from teams that were not promoted show more variability in their total points distribution, with a wider range and the presence of outliers (even with Cole Palmer removed).
            """)


# Load 5.0 mid boxplot
image_path = "assets/mid_50_boxplot.png"
st.image(image_path, use_column_width=False)

st.markdown(
    f"""*Note: if Cole Palmer 23/24 was left in, the impact would have been even more significant*"""
)
st.text("")


st.divider()
st.markdown("""### Exploratory Data Analysis""")

st.markdown("""#### Comparing FPL points with Championship Goals from the Previous Season
This illustrates the goal scorers from the Championship in teams that were subsequently promoted. It compares the players' FPL points in the season following their promotion. Notably, it highlights Bamford's impressive performance in Leeds' first season after promotion, during which he scored 17 goals between his frothy coffees.

Previous performance (goals and assists) correlates with FPL points in the following season; however, this is also reflected in the players' value.         
            """)
st.text("")


goals_championship_fpl_points = goals_championship_fpl_points[
    goals_championship_fpl_points["Championship Goals"] >= 0
]

position = st.selectbox(
    "Filter by Position",
    ["All", "DEF", "MID", "FWD"],
    index=3,
    key="scatter_plot_goals",
)

if position != "All":
    goals_championship_fpl_points = goals_championship_fpl_points[
        goals_championship_fpl_points["Position"] == position
    ]


# Create a base scatter plot
base = (
    alt.Chart(goals_championship_fpl_points)
    .mark_circle(size=60)
    .encode(
        x="Championship Goals",
        y="FPL Points",
        tooltip=[
            "Player (FPL Season)",
            "Position",
            "Championship Goals",
            "FPL Points",
            "FPL Value",
        ],  # Tooltips for all points
    )
)

# Define points to annotate
if position in ["MID"]:
    players_to_annotate = [
        "Jota: 18/19",
        "Harrison: 20/21",
        "Pereira: 20/21",
        "Sessegnon: 18/19",
        "Knockaert: 17/18",
        "Grealish: 19/20",
    ]
else:
    players_to_annotate = [
        "Mitrović: 22/23",
        "Toney: 21/22",
        "Pukki: 19/20",
        "Bamford: 20/21",
    ]

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
        color="#767679",
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
        color="#767679",
    )
    .encode(x="Championship Goals", y="FPL Points", text="Player (FPL Season) - Short")
)

# Combine the scatter plot with the annotations
chart = base + toney_text + other_text


# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=False)
st.markdown("""#### Forwards:  Championship Goals vs. FPL points vs. FPL Value
This shows Championship goals do correlate with FPL Points after promotion. However these players are priced based on this performance in the championship.           
            """)
st.text("")

forwards = goals_championship_fpl_points[
    (goals_championship_fpl_points["Position"] == "FWD")
]

# Calculate correlation matrix
correlation_matrix = forwards[["FPL Points", "FPL Value", "Championship Goals"]].corr()
average_stats = (
    goals_championship_fpl_points.groupby("FPL Value")[
        ["FPL Points", "Championship Goals"]
    ]
    .mean()
    .reset_index()
)

average_stats["FPL Points"] = round(average_stats["FPL Points"], 1)
average_stats["Championship Goals"] = round(average_stats["Championship Goals"], 1)


image_path = "assets/fwd_correlation_heatmap.png"
st.image(image_path, use_column_width=False)
st.text("")
st.markdown("""
Again, here we can see for forwards, as FPL Value increases, FPL Points increases, along with championship goals the previous season.
            """)

st.dataframe(average_stats, hide_index=True)

st.markdown("""#### Comparing FPL points with Championship Assists from the Previous Season
This illustrates players who provided assists in the Championship in teams that were subsequently promoted. It compares the players' FPL points in the season following their promotion. Matheus Pereira's strong performances in the Championship and FPL during the 2019/20 and 2020/21 seasons, respectively, are highlighted in the top right.
            
            """)
st.text("")


assists_championship_fpl_points = assists_championship_fpl_points[
    assists_championship_fpl_points["Championship Assists"] >= 0
]

position = st.selectbox(
    "Filter by Position",
    ["All", "DEF", "MID", "FWD"],
    index=2,
    key="scatter_plot_assists",
)

if position != "All":
    assists_championship_fpl_points = assists_championship_fpl_points[
        assists_championship_fpl_points["Position"] == position
    ]


# Create a base scatter plot
base = (
    alt.Chart(assists_championship_fpl_points)
    .mark_circle(size=60)
    .encode(
        x="Championship Assists",
        y="FPL Points",
        tooltip=[
            "Player (FPL Season)",
            "Position",
            "Championship Assists",
            "FPL Points",
            "FPL Value",
        ],  # Tooltips for all points
    )
)

# Define points to annotate
players_to_annotate = [
    "Wilson: 22/23",
    "Harrison: 20/21",
    "Pereira: 20/21",
]


# Create a DataFrame for annotations with specific offsets
annotations_df = assists_championship_fpl_points[
    assists_championship_fpl_points["Player (FPL Season) - Short"].isin(
        players_to_annotate
    )
]


# Create text annotations for the other players (offset to the right)
other_text = (
    alt.Chart(annotations_df)
    .mark_text(
        align="left",  # Align text to the left
        dx=10,  # Move labels to the right
        dy=-5,  # Vertical offset
        fontSize=12,
        color="#767679",
    )
    .encode(
        x="Championship Assists", y="FPL Points", text="Player (FPL Season) - Short"
    )
)

# Combine the scatter plot with the annotations
chart = base + other_text


# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=False)
st.text("")

st.divider()
st.markdown("""#### Players from Promoted Teams by Total FPL Points""")
st.text("")


# Create two columns: one for the dropdown and one for the slider
col1, col2 = st.columns([1, 1])

# Dropdown in the first column
with col1:
    position = st.selectbox(
        "Filter by Position", ["All", "GK", "DEF", "MID", "FWD"], index=0
    )

# Slider in the second column
with col2:
    value_limit = st.slider(
        "Filter by Player Value*",
        min_value=0.0,
        max_value=10.0,
        value=(0.0, 10.0),
        step=0.1,
        format="£%.1f",
    )

# Filter your data with the selected position and value limit
fpl_data_filtered = top_players_fpl_data(
    df=fpl_data, filter_position=position, top_n=1000, filter_value_first_gw=value_limit
)

# Display filtered data
st.dataframe(fpl_data_filtered, hide_index=True)

st.markdown("""
**Average points per game is the total points, divided by 38 (the number of gameweeks), not the average for games played.*
""")


st.text("")

st.markdown("""#### Promoted Teams by Total FPL Points
This shows the total FPL points for each team during their first season after promotion. It shows the sum of all players' points within each team across the season.            
            """)
st.text("")

# Display table
team_performance_fpl_points_cleaned = team_performance_fpl_points.drop(
    columns=["Team (Season)"]
)
st.dataframe(team_performance_fpl_points_cleaned, hide_index=True)
st.text("")
st.divider()
st.markdown("""### Data Sources
            
All data collection, processing and analysis code is in GitHub Repo here: [FPL-Championship-Analysis](https://github.com/EdwardAnalytics/fpl-championship-analysis)

Data Sources:
* FPL Data:
  * Collected from the FPL API via the aggregated GitHub repositiory created by Anand Vaastav here: [FPL Historical Dataset](https://github.com/vaastav/Fantasy-Premier-League)
* Championship Data:
  * Collected from WordFootball.net via the Beautiful Soup python library. E.g.: https://www.worldfootball.net/goalgetter/eng-championship-2023-2024/. 


            """)


st.text("")
st.divider()
st.markdown(key_findings)
st.text("")
st.divider()
st.markdown("""### Notes and Caveats


Other factors assessed:

* Experimented with different thresholds for defining "games played" (e.g., minutes or gameweeks).
* Built models to predict scores, aiming to determine if the "championship flag" was a significant feature. Results were similar to those from t-tests.
Note: This analysis doesn't solely focus on players who played in the Championship the previous season. It also includes new signings from that season.

We are only looking at players in teams that were promoted, not those joining from promoted teams. The latter can be influenced by the strength of the club they are moving to (e.g., when Tottenham signed Bale).

A separate analysis would be needed to assess the impact of signings from different teams.""")
