import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
FILE_PATH = "nasa_exoplanets_raw_data.csv"
df = pd.read_csv(FILE_PATH, comment='#', low_memory=False)

# Select and clean relevant columns 
df = df[["pl_name", "hostname", "pl_orbsmax", "pl_masse", "disc_year"]].copy()

# Convert to numeric
df["pl_orbsmax"] = pd.to_numeric(df["pl_orbsmax"], errors="coerce")
df["pl_masse"] = pd.to_numeric(df["pl_masse"], errors="coerce")

# Drop missing values
df = df.dropna(subset=["pl_orbsmax", "pl_masse"])

# Remove duplicates
df = df.drop_duplicates(subset="pl_name", keep="first")

print("After cleaning:", df.shape)
print(df.head(5))

# Filter based on scientifically informed but looser ranges
candidates = df[
    (df["pl_orbsmax"].between(0.5, 3.5)) &
    (df["pl_masse"].between(0.3, 10.0))
].copy()

print(f"Number of filtered candidates: {candidates.shape[0]}")

# Create habitability score 
candidates["distance_score"] = (candidates["pl_orbsmax"] - 1.0).abs()
candidates["mass_score"] = (candidates["pl_masse"] - 1.0).abs()
candidates["habitability_score"] = candidates["distance_score"] + candidates["mass_score"]

# Sort by best score
candidates_sorted = candidates.sort_values("habitability_score").reset_index(drop=True)

# Save output
output_file = "exoplanet_habitable_candidates_orbital_mass.csv"
candidates_sorted.to_csv(output_file, index=False)
print(f"Saved sorted candidates to {output_file}")

# Display top 10 most Earth-like planets
print("\nTop 10 Candidate Exoplanets (Orbit & Mass):\n")
print(candidates_sorted.head(10)[["pl_name", "hostname", "pl_orbsmax", "pl_masse", "habitability_score"]])


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

# Plot all planets for context
sns.scatterplot(
    data=df,
    x="pl_orbsmax",
    y="pl_masse",
    color="gray",
    alpha=0.2,
    s=30,
    ax=ax,
    label="All Planets"
)

# Plot filtered candidates 
scatter = ax.scatter(
    candidates_sorted["pl_orbsmax"],
    candidates_sorted["pl_masse"],
    c=candidates_sorted["habitability_score"],
    cmap="coolwarm",
    s=150,
    edgecolors='white',
    linewidths=1.2,
    alpha=0.9,
    label="Filtered Candidates"
)

# Highlight top 10 candidates 
top10 = candidates_sorted.head(10)
ax.scatter(
    top10["pl_orbsmax"],
    top10["pl_masse"],
    s=300,
    facecolors='none',
    edgecolors='cyan',
    linewidths=2.5,
    alpha=0.6,
    label="Top 10 Candidates"
)

# Add planet name labels for top 10 
#  Custom label placement for top 10 
for _, row in top10.iterrows():
    name = row["pl_name"]
    
    # Default: directly to the right
    x_offset = 0.12
    y_offset = 0.0
    
    # Custom adjustments
    if name == "MOA-2007-BLG-192L b":
        x_offset = -0.35 
        y_offset = -0.35 
    elif name == "Kepler-47 c":
        x_offset = 0.12   
        y_offset = -0.15  

    ax.text(
        row["pl_orbsmax"] + x_offset,
        row["pl_masse"] + y_offset,
        name,
        fontsize=7,
        color='cyan'
    )



# Dynamically adjust zoom to include all filtered candidates
buffer_x = 0.8
buffer_y = 1.0

x_min = max(0, candidates_sorted["pl_orbsmax"].min() - buffer_x)
x_max = candidates_sorted["pl_orbsmax"].max() + buffer_x
y_min = max(0, candidates_sorted["pl_masse"].min() - buffer_y)
y_max = candidates_sorted["pl_masse"].max() + buffer_y

ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# Axis customization
ax.set_xlabel("Orbital Distance (AU)", fontsize=16, labelpad=12)
ax.set_ylabel("Planet Mass (Earth Masses)", fontsize=16, labelpad=12)
ax.set_title("Exoplanet Habitability Candidates (Orbit & Mass)", fontsize=24, pad=25)

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
plt.savefig("habitability_plot_orbital_mass_top10.png", dpi=300, bbox_inches='tight')

plt.show()
