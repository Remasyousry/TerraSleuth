# Team split & Definition of Done

## Roles
| Person | Owns | Files |
|---|---|---|
| **A — Backend** | GEE auth, real data fetch, verify asset IDs, stats | `terrasleuth/data_sources.py`, `variables.py`, `stats.py` |
| **B — Frontend** | Streamlit UI, map, Plotly charts, cold-case presets, two-region compare | `app.py` |
| **C — AI + Content** | LLM translator, NewsAPI witnesses, README, demo video, About page | `translator.py`, `README.md`, `docs/` |

## Urgent (before anything else)
- [ ] A: register for Earth Engine and pull ONE real time series end-to-end
- [ ] A: verify every `gee_asset` / `band` / `scale_m` in `variables.py` (MERRA-2 is a TODO)
- [ ] All: agree on the Definition of Done below; **no new features after the halfway point**

## Definition of Done (the app works if…)
- [ ] User types a question and gets a variable + region (LLM or keyword fallback)
- [ ] Time series of 10+ years is plotted for that region
- [ ] Mann-Kendall + Sen's slope + OLS shown with p-value, tau, slope, CI
- [ ] Plain-language verdict shown WITH the raw numbers
- [ ] 3 cold-case presets load instantly from cached CSV
- [ ] Every data source has a CSV fallback; app never crashes offline
- [ ] About page states limits: linear trends, no seasonal removal, no causation
- [ ] README + 2–3 min demo video

## Stretch (only if ahead)
Two-region compare · NDVI cross-variable overlay · news "witnesses"

## Git workflow
- `main` is always runnable. Work on branches: `feat/backend-gee`, `feat/ui`, `feat/ai-news`.
- Small PRs, merge often. Don't commit keys.
