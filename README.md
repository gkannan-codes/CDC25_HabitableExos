# ExoHabit — Scoring Exoplanets for Habitability

---

## Why this project

Earth is trending toward reduced habitability due to rising heat, sea-level rise, freshwater stress, biodiversity loss, and other pressures. Moreover, scientists have been actively researching possible extraterrestrial life since the 1950s. Our project quantifies this concern and research by proposing an important question:

> **If we ever had to live beyond Earth, which known exoplanets would be the best places to live in?**

We address this question by extracting 5 key planet/star characteristics from the NASA Exoplanet Archive, normalizing them to Earth-relative units, and building a scoring function where 1 ≈ Earth-like.

---
## Data

- **Source:** NASA Exoplanet Archive.
- **Core columns used (Earth-relative where possible):**
  - `pl_insol` — **Insolation Flux** (Earth = 1)
  - `pl_rade` — **Planet Radius** (Earth radii)
  - `pl_orbsmax` — **Orbital Distance / Semi-major Axis** (AU)
  - `pl_bmasse` — **Planet Mass** (Earth masses)
  - `pl_eqt` — **Equilibrium Temperature** (K)

> We prefilter to rows with these fields present, and we normalize to support scoring.

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
*This research has made use of the NASA Exoplanet Archive, which is operated by the California Institute of Technology, under contract with the National Aeronautics and Space Administration under the Exoplanet Exploration Program.*
