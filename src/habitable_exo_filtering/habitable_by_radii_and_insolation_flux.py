import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Loading dataset / previewing columns
FILE_PATH = "nasa_exoplanets_raw_data.csv"
df = pd.read_csv(FILE_PATH, comment='#', low_memory=False)

print("Dataset shape:", df.shape)
print("Columns available:", list(df.columns)[:15])  # show first 15 column names
print(df.head(5))  # preview first 5 rows




# Cleaning and converting important columns
#     Converting relevant rows to numeric
numeric_cols = ["pl_rade", "pl_insol", "pl_orbper", "pl_orbsma", "st_teff", "st_rad"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

#     Drop rows missing earth radius, insolation flux
df = df.dropna(subset=["pl_rade", "pl_insol"])

#     Remove duplicates based on exoplanet names
df = df.drop_duplicates(subset=["pl_name"], keep="first")

print("After cleaning:", df.shape)




# Filtering exoplanets for Earth-like ranges
#         Planetary radius between 0.5 -- 1.6 Earth radii
#         Insolation flux between 0.3 - 1.7 Earth flux
candidates = df[
    (df["pl_rade"].between(0.5, 1.6)) &
    (df["pl_insol"].between(0.3, 1.7))
].copy()

# Create a "habitability score"
candidates["radius_score"] = (candidates["pl_rade"] - 1.0).abs()
candidates["flux_score"] = (candidates["pl_insol"] - 1.0).abs()
candidates["habitability_score"] = candidates["radius_score"] + candidates["flux_score"]

# Sort by best score
candidates_sorted = candidates.sort_values("habitability_score").reset_index(drop=True)

# Save output
output_file = "exoplanet_habitable_candidates_conservative.csv"
candidates_sorted.to_csv(output_file, index=False)
print(f"Saved sorted candidates to {output_file}")



# Displaying the top 10 most Earth-like planets
columns_to_show = [
    "pl_name", "hostname", "pl_rade", "pl_insol", "pl_orbper", "pl_orbsma", "disc_year", "habitability_score"
]
columns_to_show = [c for c in columns_to_show if c in candidates_sorted.columns]

print("\nTop 10 Candidate Exoplanets:\n")
print(candidates_sorted[columns_to_show].head(10))



# Visualization and MatPlotLib graphs
dark_bg = "#0d1b2a"

# Set Seaborn theme with dark background
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

# Create figure
fig, ax = plt.subplots(figsize=(14, 10))

# Plot all planets
sns.scatterplot(
    data=df,
    x="pl_rade",
    y="pl_insol",
    color="gray",
    alpha=0.2,
    s=30,
    ax=ax,
    label="All Planets"
)

# Plot habitable candidates
scatter = ax.scatter(
    candidates_sorted["pl_rade"],
    candidates_sorted["pl_insol"],
    c=candidates_sorted["habitability_score"],
    cmap="coolwarm",
    s=150,
    edgecolors='white',
    linewidths=1.2,
    alpha=0.9
)

# Highlight top 10 candidates
best_candidates = candidates_sorted.head(10)
ax.scatter(
    best_candidates["pl_rade"],
    best_candidates["pl_insol"],
    s=300,
    facecolors='none',
    edgecolors='cyan',
    linewidths=2.5,
    alpha=0.6,
    label="Top Candidates"
)

# Add planet name labels for top 10 (all left with custom y-offsets)
for _, row in best_candidates.iterrows():
    y_offset = 0.0
    
    # Custom adjustments
    if row["pl_name"] == "TOI-700 d":
        y_offset = 0.12   # slightly higher
    elif row["pl_name"] == "LP 890-9 c":
        y_offset = 0.05   # slightly higher
    elif row["pl_name"] == "K2-72 e":
        y_offset = -0.08  # slightly lower

    ax.text(
        row["pl_rade"] - 0.25,         
        row["pl_insol"] + y_offset,     
        row["pl_name"],
        fontsize=7,
        color='cyan'
    )



# Axes customization
ax.set_xlim(0, 3)
ax.set_ylim(0.1, 3)
ax.set_yscale('log')
ax.set_xlabel("Planet Radius (Earth radii)", fontsize=16, labelpad=12)
ax.set_ylabel("Insolation Flux (Earth = 1.0)", fontsize=16, labelpad=12)
ax.set_title("Exoplanet Habitability Candidates", fontsize=24, pad=25)

# Grid
ax.grid(True, which='both', linestyle='--', alpha=0.3)

# Colorbar
cbar = plt.colorbar(scatter, ax=ax, pad=0.02)
cbar.set_label("Habitability Score", fontsize=14, color='white')
cbar.ax.yaxis.set_tick_params(color='white')
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

# Legend
legend = ax.legend(frameon=True, facecolor=dark_bg, edgecolor='white', fontsize=12)
for text in legend.get_texts():
    text.set_color("white")

# Save high-res figure
plt.savefig("habitability_plot_sleek.png", dpi=300, bbox_inches='tight')

plt.show()



