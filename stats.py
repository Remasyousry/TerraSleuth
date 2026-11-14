"""Trend statistics for TerraSleuth.

Self-contained (numpy + scipy only): Mann-Kendall test, Sen's slope,
OLS linear regression with t-test, and a plain-language verdict.

Scope (state this on the About page): linear/monotonic trends only,
no seasonal removal, no causal claims.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np
from scipy import stats as sps

ALPHA = 0.05


@dataclass
class TrendResult:
    n: int
    # Mann-Kendall
    mk_tau: float
    mk_p: float
    mk_trend: str  # "increasing" | "decreasing" | "no trend"
    # Sen's slope (per time unit of x, e.g. per year)
    sen_slope: float
    sen_ci_low: float
    sen_ci_high: float
    # OLS
    ols_slope: float
    ols_p: float
    ols_ci_low: float
    ols_ci_high: float
    r_squared: float
    significant: bool
    verdict: str

    def to_dict(self) -> dict:
        return asdict(self)


def mann_kendall(y: np.ndarray, alpha: float = ALPHA) -> tuple[float, float, str]:
    """Classic Mann-Kendall with tie correction. Returns (tau, p, trend)."""
    y = np.asarray(y, dtype=float)
    n = len(y)
    s = 0
    for i in range(n - 1):
        s += np.sign(y[i + 1:] - y[i]).sum()
    _, counts = np.unique(y, return_counts=True)
    tie_term = (counts * (counts - 1) * (2 * counts + 5)).sum()
    var_s = (n * (n - 1) * (2 * n + 5) - tie_term) / 18.0
    if s > 0:
        z = (s - 1) / np.sqrt(var_s)
    elif s < 0:
        z = (s + 1) / np.sqrt(var_s)
    else:
        z = 0.0
    p = 2 * (1 - sps.norm.cdf(abs(z)))
    n0 = n * (n - 1) / 2
    n1 = n0 - (counts * (counts - 1) / 2).sum()
    tau = s / np.sqrt(n0 * n1) if n1 > 0 else 0.0
    trend = "no trend" if p >= alpha else ("increasing" if z > 0 else "decreasing")
    return float(tau), float(p), trend


def sens_slope(x: np.ndarray, y: np.ndarray, alpha: float = ALPHA):
    """Sen's slope with a confidence interval (per unit of x)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(y)
    i, j = np.triu_indices(n, k=1)
    dx = x[j] - x[i]
    mask = dx != 0
    slopes = (y[j] - y[i])[mask] / dx[mask]
    med = float(np.median(slopes))
    # CI from the variance of S (no tie correction in the CI rank — standard approximation)
    var_s = n * (n - 1) * (2 * n + 5) / 18.0
    z = sps.norm.ppf(1 - alpha / 2)
    c = z * np.sqrt(var_s)
    m = len(slopes)
    lo_rank = int(max(np.floor((m - c) / 2), 0))
    hi_rank = int(min(np.ceil((m + c) / 2), m - 1))
    srt = np.sort(slopes)
    return med, float(srt[lo_rank]), float(srt[hi_rank])


def analyze_trend(x, y, alpha: float = ALPHA) -> TrendResult:
    """Analyze a time series.

    x: numeric time axis in YEARS (e.g. 2005.0, 2005.083, ...). Slopes are per year.
    y: measured values.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    ok = ~(np.isnan(x) | np.isnan(y))
    x, y = x[ok], y[ok]
    n = len(y)
    if n < 8:
        raise ValueError(f"Need at least 8 points for a trend test, got {n}.")

    tau, mk_p, mk_trend = mann_kendall(y, alpha)
    sen, sen_lo, sen_hi = sens_slope(x, y, alpha)

    ols = sps.linregress(x, y)
    tcrit = sps.t.ppf(1 - alpha / 2, n - 2)
    ols_lo = ols.slope - tcrit * ols.stderr
    ols_hi = ols.slope + tcrit * ols.stderr

    significant = mk_p < alpha
    verdict = build_verdict(mk_trend, significant, sen, mk_p)
    return TrendResult(
        n=n, mk_tau=tau, mk_p=mk_p, mk_trend=mk_trend,
        sen_slope=sen, sen_ci_low=sen_lo, sen_ci_high=sen_hi,
        ols_slope=float(ols.slope), ols_p=float(ols.pvalue),
        ols_ci_low=float(ols_lo), ols_ci_high=float(ols_hi),
        r_squared=float(ols.rvalue ** 2),
        significant=significant, verdict=verdict,
    )


def build_verdict(trend: str, significant: bool, slope_per_year: float, p: float) -> str:
    """Plain-language verdict. Says 'statistically significant trend', never 'proof'/'cause'."""
    if not significant:
        return ("Insufficient evidence: no statistically significant trend was detected "
                f"(p = {p:.3f}). Variation is consistent with natural fluctuation, "
                "and a longer record might change this.")
    direction = "rising" if slope_per_year > 0 else "falling"
    per_decade = slope_per_year * 10
    return (f"Statistically significant trend: the variable is {direction} by about "
            f"{abs(per_decade):.3g} units per decade (p = {p:.3g}). "
            "This describes a trend, not its cause.")
