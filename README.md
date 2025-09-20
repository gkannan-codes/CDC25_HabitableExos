# ExoHabit — Scoring Exoplanets for Human-Centric Habitability

*A data-challenge project that uses NASA’s Exoplanet Archive to identify planets most likely to support human life (or human-built life-support systems) in the very long term.*

---

## Why this project

Modern Earth is trending toward reduced habitability due to rising heat, sea-level rise, freshwater stress, biodiversity loss, and other pressures. Framing this urgency, Earth-system science tracks **nine planetary boundaries** (life-support processes); multiple are already **transgressed**. Our project quantifies a simple “Earth stress” story and then asks a pragmatic question:

> **Given what keeps humans alive on Earth, which known exoplanets look most promising if we ever had to live beyond Earth?**

We operationalize this by extracting five key planet/star characteristics from NASA’s Exoplanet Archive, normalizing them to **Earth-relative units**, and building a transparent scoring function on \[0, 1\] where **1 ≈ Earth-like**.

---
## Limitations & Assumptions

- **Observational incompleteness & bias.** The confirmed exoplanet sample is biased toward short-period and/or larger planets around bright stars (transit/RV selection effects). Many rows lack one or more features, so filtering can skew the sample further.

- **Proxy features, not surface conditions.**  
  - `pl_eqt` (equilibrium temperature) assumes zero/constant albedo and full heat redistribution; true surface temps can differ by tens of K or more.  
  - “Orbital distance” and “insolation flux” are correlated; we reduce double-counting by down-weighting distance when `pl_insol` is present.

- **Planet composition uncertainty.** Similar mass–radius pairs can be rocky, water-rich, or mini-Neptunes. We do not infer bulk composition or interior structure beyond simple mass/radius preferences.

- **Stellar environment not fully modeled.** We don’t explicitly account for stellar activity (flares, UV/X-ray), magnetospheres, atmospheric escape, tidal locking climate effects, or long-term orbital stability—each can be decisive for habitability.

- **Anthropocentric scoring.** We target human-centric constraints (Earth-like gravity, moderate temperatures/light cycles) rather than biosignature likelihood. A high score ≠ “habitable”—it’s a **prioritization signal for follow-up**.

- **Point estimates, limited uncertainty.** Measurement errors and asymmetric posteriors are not propagated through the score; rankings can shift as the Archive updates values.

- **Heuristic weights.** Weights are literature-informed but ultimately chosen by us; rankings are sensitive to these choices (the UI exposes sliders to make this explicit).

- **Catalog drift & reproducibility.** The NASA Exoplanet Archive is updated frequently. Results reflect the snapshot time of our TAP query; see `data/README_sources.md` for the exact query and date.

### Mitigations & Future Work

- Add **uncertainty-aware scoring** (Monte Carlo draws over reported intervals) and show rank stability bands.  
- Incorporate **stellar activity proxies** (e.g., flare rates, `log R'_{HK}`), metallicity priors, and simple **atmospheric escape** checks for small M-dwarf planets.  
- Use **conservative/optimistic habitable-zone edges** (e.g., Kopparapu et al.) to derive a more physical insolation window.  
- Explore **composition classification** from mass–radius relations to down-weight likely mini-Neptunes.  
- Log data snapshots (DOI or hash) to make results **reproducible** across Archive updates.

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
