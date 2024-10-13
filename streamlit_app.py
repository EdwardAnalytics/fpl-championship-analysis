import streamlit as st
import pandas as pd

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


goals_championship_fpl_points = goals_championship_fpl_points[
    goals_championship_fpl_points["Championship Goals"] >= 5
]
import streamlit as st
import pandas as pd
import altair as alt


# Create a base scatter plot
base = alt.Chart(goals_championship_fpl_points).mark_circle(size=60).encode(
    x='Championship Goals',
    y='FPL Points',
    tooltip=['Player (FPL Season)', 'Championship Goals', 'FPL Points']  # Tooltips for all points
)

# Define points to annotate
players_to_annotate = ['Mitrović: 22/23', 'Toney: 21/22', 'Pukki: 19/20']

# Create a DataFrame for annotations with specific offsets
annotations_df = goals_championship_fpl_points[goals_championship_fpl_points['Player (FPL Season) - Short'].isin(players_to_annotate)]

# Create text annotations for Toney separately (offset to the left)
toney_text = alt.Chart(annotations_df[annotations_df['Player (FPL Season) - Short'] == 'Toney: 21/22']).mark_text(
    align='right',  # Align text to the right for Toney
    dx=-10,         # Move Toney's label to the left
    dy=-5,          # Vertical offset
    fontSize=12,
    color='white'
).encode(
    x='Championship Goals',
    y='FPL Points',
    text='Player (FPL Season) - Short'
)

# Create text annotations for the other players (offset to the right)
other_text = alt.Chart(annotations_df[annotations_df['Player (FPL Season) - Short'] != 'Toney: 21/22']).mark_text(
    align='left',   # Align text to the left for others
    dx=10,          # Move labels to the right
    dy=-5,          # Vertical offset
    fontSize=12,
    color='white'
).encode(
    x='Championship Goals',
    y='FPL Points',
    text='Player (FPL Season) - Short'
)

# Combine the scatter plot with the annotations
chart = base + toney_text + other_text

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)
