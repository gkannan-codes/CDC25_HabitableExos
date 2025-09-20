# ExoHabit — Scoring Exoplanets for Human-Centric Habitability

*A data-challenge project that uses NASA’s Exoplanet Archive to identify planets most likely to support human life (or human-built life-support systems) in the very long term.*

---

## Why this project

Modern Earth is trending toward reduced habitability due to rising heat, sea-level rise, freshwater stress, biodiversity loss, and other pressures. Framing this urgency, Earth-system science tracks **nine planetary boundaries** (life-support processes); multiple are already **transgressed**. Our project quantifies a simple “Earth stress” story and then asks a pragmatic question:

> **Given what keeps humans alive on Earth, which known exoplanets look most promising if we ever had to live beyond Earth?**

We operationalize this by extracting five key planet/star characteristics from NASA’s Exoplanet Archive, normalizing them to **Earth-relative units**, and building a transparent scoring function on \[0, 1\] where **1 ≈ Earth-like**.

---
## Data

- **Source:** NASA Exoplanet Archive — `pscomppars` table (confirmed exoplanets with derived/combined parameters).
- **Core columns used (Earth-relative where possible):**
  - `pl_insol` — **Insolation Flux** (Earth = 1)
  - `pl_rade` — **Planet Radius** (Earth radii)
  - `pl_orbsmax` — **Orbital Distance / Semi-major Axis** (AU)
  - `pl_bmasse` — **Planet Mass** (Earth masses)
  - `pl_eqt` — **Equilibrium Temperature** (K)

> We prefilter to rows with these fields present, and we standardize/normalize to support scoring.

**Programmatic download (reproducible):**
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
