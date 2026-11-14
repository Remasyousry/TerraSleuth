"""Time-series retrieval with automatic CSV fallback.

Public API:
    get_timeseries(variable_key, bbox, start_year, end_year) -> pandas.DataFrame
        columns: date (datetime64), year (float), value (float)

bbox = (west, south, east, north) in degrees.

Primary source: Google Earth Engine. If GEE is not installed/authenticated or
the call fails, falls back to data/fallback/<variable_key>__<region>.csv
(or a synthetic demo series if no CSV exists, clearly flagged).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .variables import VARIABLES

FALLBACK_DIR = Path(__file__).resolve().parent.parent / "data" / "fallback"


def get_timeseries(variable_key: str, bbox, start_year: int, end_year: int,
                   region_name: str = "custom") -> tuple[pd.DataFrame, str]:
    """Return (dataframe, source_note). Never raises on network problems."""
    if variable_key not in VARIABLES:
        raise KeyError(f"Unknown variable: {variable_key}")
    try:
        df = _from_gee(variable_key, bbox, start_year, end_year)
        return df, "Google Earth Engine (live)"
    except Exception as exc:  # noqa: BLE001 - fallback by design
        note = f"GEE unavailable ({type(exc).__name__}); "
    csv = FALLBACK_DIR / f"{variable_key}__{region_name}.csv"
    if csv.exists():
        df = pd.read_csv(csv, parse_dates=["date"])
        df["year"] = df["date"].dt.year + (df["date"].dt.dayofyear - 1) / 365.25
        return df, note + f"using cached CSV {csv.name}"
    return _synthetic(start_year, end_year), note + "no cached CSV — showing SYNTHETIC demo data"


def _from_gee(variable_key, bbox, start_year, end_year) -> pd.DataFrame:
    import ee  # imported lazily so the app runs without it

    ee.Initialize()  # TODO(A): add project= and service-account auth for deployment
    spec = VARIABLES[variable_key]
    region = ee.Geometry.Rectangle(list(bbox))
    scale_factor = spec.get("scale_factor", 1.0)

    ic = (ee.ImageCollection(spec["gee_asset"])
          .filterDate(f"{start_year}-01-01", f"{end_year}-12-31")
          .select(spec["band"]))

    def to_feature(img):
        val = img.reduceRegion(ee.Reducer.mean(), region, spec["scale_m"], maxPixels=1e9).get(spec["band"])
        return ee.Feature(None, {"t": img.date().millis(), "v": val})

    feats = ic.map(to_feature).filter(ee.Filter.notNull(["v"])).getInfo()["features"]
    df = pd.DataFrame({
        "date": pd.to_datetime([f["properties"]["t"] for f in feats], unit="ms"),
        "value": [f["properties"]["v"] * scale_factor for f in feats],
    }).sort_values("date")
    df["year"] = df["date"].dt.year + (df["date"].dt.dayofyear - 1) / 365.25
    if len(df) == 0:
        raise ValueError("empty GEE result")
    return df.reset_index(drop=True)


def _synthetic(start_year: int, end_year: int) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    dates = pd.date_range(f"{start_year}-01-01", f"{end_year}-12-01", freq="MS")
    t = np.arange(len(dates))
    values = 20 + 0.01 * t + 3 * np.sin(2 * np.pi * t / 12) + rng.normal(0, 1, len(t))
    df = pd.DataFrame({"date": dates, "value": values})
    df["year"] = df["date"].dt.year + (df["date"].dt.dayofyear - 1) / 365.25
    return df
