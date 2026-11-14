# 🌍 TerraSleuth



NASA Space Apps Challenge 2026 — **Be an Earth System Trend Detective**.

TerraSleuth turns anyone into a "data detective": ask a plain-language question about your environment, and the app fetches NASA Earth-science time series for your region, plots them, and tests whether the change is **statistically significant** — showing both a simple verdict and the raw numbers.

## How it works
1. **File a report** — ask a question (Arabic or English); a closed-list translator maps it to a variable + region.
2. **Gather evidence** — time series from NASA missions/models via Google Earth Engine (CSV fallback offline).
3. **Verdict** — Mann-Kendall test, Sen's slope, OLS + confidence intervals, in plain language.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
earthengine authenticate      # one-time
pytest                        # stats tests
streamlit run app.py
```

## Layout
```
app.py                    Streamlit UI
terrasleuth/stats.py      Mann-Kendall, Sen's slope, OLS, verdict
terrasleuth/variables.py  Closed whitelist of variables
terrasleuth/data_sources.py  GEE fetch + CSV fallback
terrasleuth/translator.py Question -> variable/region
data/fallback/            Cached CSVs
docs/TEAM_TASKS.md        Roles + Definition of Done
```



## Data
NASA GPM, MODIS, MERRA-2, GLDAS via Google Earth Engine.


