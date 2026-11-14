import numpy as np
import pytest

from terrasleuth.stats import analyze_trend


def test_detects_known_positive_trend():
    rng = np.random.default_rng(0)
    x = np.arange(2005, 2025, 1 / 12)
    y = 10 + 0.12 * (x - 2005) + rng.normal(0, 0.5, len(x))
    r = analyze_trend(x, y)
    assert r.significant and r.mk_trend == "increasing"
    assert r.sen_slope == pytest.approx(0.12, abs=0.03)
    assert r.sen_ci_low <= r.sen_slope <= r.sen_ci_high


def test_pure_noise_is_not_significant():
    rng = np.random.default_rng(1)
    x = np.arange(2005, 2025, 1 / 12)
    r = analyze_trend(x, rng.normal(0, 1, len(x)))
    assert not r.significant
    assert "Insufficient evidence" in r.verdict


def test_too_few_points_raises():
    with pytest.raises(ValueError):
        analyze_trend([1, 2, 3], [1, 2, 3])
