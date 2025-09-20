# Import necessary libraries/packages
import kagglehub
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from pathlib import Path

# -------------------- DARK THEME (Matplotlib) --------------------
dark_bg = "#0d1b2a"   # deep space
fg      = "#e8edf5"   # light text
grid_c  = "#99aabb"   # subtle grid

plt.rcParams.update({
    "figure.figsize": (10.5, 6),
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.color": grid_c,
    "axes.titleweight": "bold",
    "axes.labelsize": 12,
    "axes.titlesize": 16,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "font.family": "DejaVu Sans",
    # Dark background + light foreground
    "figure.facecolor": dark_bg,
    "axes.facecolor": dark_bg,
    "savefig.facecolor": dark_bg,
    "text.color": fg,
    "axes.labelcolor": fg,
    "xtick.color": fg,
    "ytick.color": fg,
})

# Download dataset -> returns DIRECTORY
dataset_dir = Path(kagglehub.dataset_download(
    "programmerrdai/co2-levels-globally-from-fossil-fuels"
))
print("Path to dataset files:", dataset_dir)

# Find CSVs and load one, throw an error in the case the dataset location is not found or changed
csvs = list(dataset_dir.rglob("*.csv"))
if not csvs:
    raise FileNotFoundError("No CSV files found in the dataset folder.")
print("Found CSVs:", [p.name for p in csvs])  # return the name of all csvs downloaded from this URL

# Load a specific CSV file into a DataFrame and print the first few rows
df = pd.read_csv(dataset_dir / "global.csv")
print(df.head())

# Uncomment to save the DataFrame to a local CSV file (for future & easier reference)
# df.to_csv("historical_CO2_trends_raw_data.csv", index=False)

# 1) Clean types & sort
df['Year']  = pd.to_numeric(df['Year'], errors='coerce')
df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
df = df.dropna(subset=['Year','Total']).sort_values('Year')

# 2) Optional smoothing (rolling mean)
window = 5  # years
df['Total_roll'] = df['Total'].rolling(window=window, center=True, min_periods=1).mean()

# 3) Trendline (ordinary least squares on Year -> Total)
x = df['Year'].values
y = df['Total'].values
coef = np.polyfit(x, y, 1)              # slope, intercept
trend = np.poly1d(coef)(x)
slope, intercept = coef
trend_label = f"Trend: +{slope:,.2f} / year"

# ---- Matplotlib Plot (dark theme applied above) ----
fig, ax = plt.subplots()

# 5) Main line
ax.plot(df['Year'], df['Total'], linewidth=2.0, marker='o', markersize=3, label='Annual')

# 6) Rolling mean (subtle emphasis via line width & alpha)
ax.plot(df['Year'], df['Total_roll'], linewidth=3.0, alpha=0.9, label=f'{window}-yr rolling mean')

# 7) Trendline
ax.plot(df['Year'], trend, linestyle='--', linewidth=2.0, label=trend_label)

# 8) Labels & formatting
ax.set_title("Global CO₂ from Fossil Fuels Over Time")
ax.set_xlabel("Year")
ax.set_ylabel("CO₂ (Total)")
ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))

# 9) Endpoint annotations (use darker box on dark bg)
x0, y0 = df['Year'].iloc[0], df['Total'].iloc[0]
x1, y1 = df['Year'].iloc[-1], df['Total'].iloc[-1]
ann_box = dict(boxstyle="round,pad=0.2", fc="#121a24", ec="none", alpha=0.9)

ax.annotate(f"{int(x0)}: {y0:,.0f}",
            xy=(x0, y0), xytext=(0, 0),
            textcoords="offset points", xycoords='data', fontsize=9,
            bbox=ann_box)
ax.annotate(f"{int(x1)}: {y1:,.0f}",
            xy=(x1, y1), xytext=(0, 10),
            textcoords="offset points", ha="center", fontsize=9,
            bbox=ann_box)

# 10) CAGR (if your data are annual sums, this adds a nice stat)
years = x1 - x0
if years > 0 and y0 > 0:
    cagr = (y1 / y0) ** (1 / years) - 1
    ax.text(0.01, 0.98, f"CAGR: {100*cagr:.2f}% / yr", transform=ax.transAxes,
            va="top", ha="right", fontsize=11, color=fg)

# 11) Legend & layout
leg = ax.legend(frameon=False, loc='upper right')
fig.tight_layout()

# 12) Save (PNG + SVG for slides)
outdir = Path("figures"); outdir.mkdir(exist_ok=True)
plt.savefig(outdir / "co2_trend_dark.png", dpi=300, bbox_inches="tight")
plt.savefig(outdir / "co2_trend_dark.svg", bbox_inches="tight")
plt.show()

# -------------------- Plotly (custom dark "space" theme) --------------------
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Year'], y=df['Total'], mode='lines+markers', name='Annual'))
fig.add_trace(go.Scatter(x=df['Year'], y=df['Total_roll'], mode='lines', name=f'{window}-yr rolling mean'))
fig.add_trace(go.Scatter(x=df['Year'], y=trend, mode='lines', name='Trend', line=dict(dash='dash')))
fig.update_yaxes(zeroline=False)

fig.update_layout(
    title="Global CO₂ from Fossil Fuels Over Time",
    xaxis_title="Year",
    yaxis_title="CO₂ (Total)",
    hovermode="x unified",
    margin=dict(l=60, r=20, t=60, b=50),
    paper_bgcolor=dark_bg,   # deep space
    plot_bgcolor=dark_bg,
    font=dict(color=fg, family="Arial")
)

# subtle grid for readability (light lines on dark bg)
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="rgba(255,255,255,0.08)",
                 tickfont=dict(color=fg), title_font=dict(color=fg))
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="rgba(255,255,255,0.08)",
                 tickformat=",", tickfont=dict(color=fg), title_font=dict(color=fg))

fig.show()