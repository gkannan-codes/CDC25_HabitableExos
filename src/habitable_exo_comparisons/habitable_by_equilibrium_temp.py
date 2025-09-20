import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Reading data 
FILE_PATH = "nasa_exoplanets_raw_data.csv"
df = pd.read_csv(FILE_PATH, comment='#', low_memory=False)

# Select relevant columns
df_eqt = df[["pl_name", "pl_eqt"]].copy()

# Remove 'null' or missing values
df_eqt = df_eqt[df_eqt["pl_eqt"] != 'null']

# Convert pl_eqt to numeric
df_eqt["pl_eqt"] = pd.to_numeric(df_eqt["pl_eqt"], errors='coerce')

# Drop rows where pl_eqt could not be converted
df_eqt = df_eqt.dropna()

# Remove duplicates by exoplanet names
df_eqt = df_eqt.drop_duplicates(subset = "pl_name", keep = "first")

print("After cleaning:", df_eqt.shape)
print(df_eqt.head(20))


# Filtering based on scientific ranges
candidates = df_eqt[
    (df_eqt["pl_eqt"].between(175, 310))
].copy()

print(f"Number of filtered candidates: {candidates.shape[0]}")

# Sort candidates by how close they are to Earth-like temperature (~255K)
candidates["temp_score"] = (candidates["pl_eqt"] - 255).abs()
candidates_sorted = candidates.sort_values("temp_score").reset_index(drop=True)

# Save top candidates
output_file = "exoplanet_habitable_candidates_eqt.csv"
candidates_sorted.to_csv(output_file, index=False)
top10 = candidates_sorted.head(10).reset_index(drop=True)

print("Top 10 Candidate Exoplanets (Equilibrium Temperature in K):")
print(candidates_sorted.head(10)[["pl_name", "pl_eqt"]])

# Visualization
dark_bg = "#0d1b2a"
sns.set_theme(style="darkgrid", context="talk", rc={
    "axes.facecolor": dark_bg,
    "figure.facecolor": dark_bg,
    "grid.color": "gray",
    "grid.alpha": 0.3,
    "font.family": "DejaVu Sans",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "text.color": "white"
})

fig, ax = plt.subplots(figsize=(14, 10))

# X-axis: top 10 planets
x_vals = np.arange(len(top10))

# Plot top 10 candidates
scatter = ax.scatter(
    x_vals,
    top10["pl_eqt"],
    c=top10["temp_score"],
    cmap="coolwarm",
    s=250,
    edgecolors='white',
    linewidths=1.5,
    alpha=0.9
)

# Axes customization
ax.set_xticks(x_vals)
ax.set_xticklabels(top10["pl_name"], rotation=45, ha='right', fontsize=10)
ax.set_ylabel("Equilibrium Temperature (K)", fontsize=16, labelpad=12)
ax.set_title("Top 10 Exoplanets by Earth-like Equilibrium Temperature", fontsize=24, pad=25)

# Grid
ax.grid(True, which='both', linestyle='--', alpha=0.3)

# Colorbar
cbar = plt.colorbar(scatter, ax=ax, pad=0.02)
cbar.set_label("Temperature Score (|T - 288K|)", fontsize=14, color='white')
cbar.ax.yaxis.set_tick_params(color='white')
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

# Save figure
plt.savefig("habitability_plot_eqt_top10_scaled.png", dpi=300, bbox_inches='tight')
plt.show()