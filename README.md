# HabitableExos — Scoring Exoplanets for Habitability

---

## Why this project

Earth is trending toward reduced habitability due to rising heat, sea-level rise, freshwater stress, biodiversity loss, and other pressures. Moreover, scientists have been actively researching possible extraterrestrial life since the 1950s. Our project quantifies this by proposing this question:

> **If we ever had to live beyond Earth, which known exoplanets would be the best places to live in?**

We address this question by extracting 5 key planet/star characteristics from the NASA Exoplanet Archive, normalizing them to Earth-relative units, and building a scoring function where 1 ≈ Earth-like.

---
## Data

- **Source:** NASA Exoplanet Archive.
- **Core columns used:**
  - `pl_insol` — **Insolation Flux** (Earth = 1) - the amount of incoming radiation from a host star
  - `pl_rade` — **Planet Radius** (Earth radii) 
  - `pl_orbsmax` — **Orbital Distance / Semi-major Axis** (AU) - the average distance between a planet and its host star
  - `pl_bmasse` — **Planet Mass** (Earth masses)
  - `pl_eqt` — **Equilibrium Temperature** (K) - the temperature of a planet if it emits as much energy as it absorbs from its host star.

We prefilter the data to rows with these fields present and we normalize to support scoring. In addition, we design charts to extract valuable insights from the data: (1) finding the top 10 exoplanets with the most Earth-like Equilibrium Temperature, (2) plotting exoplanet habitability candidates based on planet mass and orbital distance, and (3) plotting exoplanet habitability candidates against planet radius and insolation flux. Finally, we calculate a habitability score by designing a weighted 6 dimensional equation by designing weights for these five factors based on relative importance. These weights are as follows: (1) Insolation Flux - 0.30 (which defines the habitable zone, where liquid water can exist on a planet's surface), (2) Planetary Radius - 0.25 (determines whether a planet is rocky, which is necessary for habitability), (3) Planetary Mass - 0.20, determining whether a planet can maintain an atmosphere and tectonic plates, (4) Equilibrium Temperature - 0.15 (determines surface temperature, although it ignores the greenhouse effect), and (5) Orbital Distance - 0.10 (is important to determine how far a planet is from its host star, though not as important as insolation flux and hence, weighed the lowest). This equation is represented by:

> H = 0.30F + 0.25R + 0.20M + 0.15T + 0.10D
where H represents habitability score, F represents insolation flux, R represents planetary radius, M represents planetary mass, T represents equilibrium temperature, and D represents orbital distance.

All figures can be found in the *figures* folder. All modified datasets, including the raw dataset, can be accessed through the *data* folder. Code to analyze historical earth trends and filter habitable exoplanet comparisons to create the figures can be found in the *src* folder, under the *historical_earth_trends* and *habitable_exo_comparisons* folders respectively. The code to edit the data and develop and test the equation can be accessed under *src/main*. Lastly, website presenting the results of the equation using sliders for each variable can be accessed using this link: https://gkannan-codes.github.io/CDC25_HabitableExos/, and its source code can be found in the *docs/index.html*.

**Programmatic download:**
```python
import pandas as pd, urllib.parse as up
sql = """
select pl_name, hostname, pl_insol, pl_rade, pl_orbsmax, pl_bmasse, pl_eqt
from pscomppars
"""
url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=" + up.quote_plus(sql) + "&format=csv"
df = pd.read_csv(url)
```

## Credits
*This project has made use of the NASA Exoplanet Archive, which is operated by the California Institute of Technology, under contract with the National Aeronautics and Space Administration under the Exoplanet Exploration Program.*
