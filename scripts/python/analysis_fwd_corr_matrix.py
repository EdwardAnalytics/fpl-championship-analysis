import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

goals_championship_fpl_points = pd.read_csv(
    "data/analysis/goals_championship_fpl_points.csv"
)


forwards = goals_championship_fpl_points[
    (goals_championship_fpl_points["Position"] == "FWD")
]

# Calculate correlation matrix
correlation_matrix = forwards[["FPL Points", "FPL Value", "Championship Goals"]].corr()

fig, ax = plt.subplots(figsize=(3, 3))
sns.heatmap(correlation_matrix, ax=ax, annot=True, cmap="crest")

plt.savefig("assets/fwd_correlation_heatmap.png", bbox_inches="tight")
