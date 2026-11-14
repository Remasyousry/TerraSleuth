"""Natural-language question -> (variable, region). Closed-list, with offline fallback.

The LLM may only return a key from VARIABLES; anything else is rejected.
TODO(C): wire Gemini/OpenAI in `_llm_translate`. Keep the keyword fallback —
the hackathon network is unreliable.
"""
from __future__ import annotations

import json

from .variables import VARIABLES

REGIONS = {
    "california": (-124.4, 32.5, -114.1, 42.0),
    "florida": (-87.6, 24.5, -80.0, 31.0),
    "aral sea": (58.0, 43.0, 61.5, 46.8),
    "greenland": (-55.0, 60.0, -20.0, 83.0),
    "cairo": (31.0, 29.8, 31.6, 30.3),
    "egypt": (24.7, 22.0, 36.9, 31.7),
}

KEYWORDS = {
    "precipitation": ["rain", "precip", "drought", "جفاف", "مطر", "أمطار", "امطار"],
    "land_temperature": ["hot", "heat", "temperature", "warming", "حرارة", "سخن", "حر"],
    "ndvi": ["green", "vegetation", "forest", "plant", "نبات", "اخضرار", "غطاء"],
    "soil_moisture": ["soil", "تربة"],
    "evapotranspiration": ["evapor", "تبخر"],
}


def translate(question: str) -> dict:
    """Return {"variable": key, "region": name, "bbox": (...), "method": str}."""
    try:
        result = _llm_translate(question)
        if result and result.get("variable") in VARIABLES:
            return result
    except Exception:  # noqa: BLE001
        pass
    return _keyword_translate(question)


def _llm_translate(question: str) -> dict | None:
    """TODO(C): call the LLM with a prompt listing VARIABLES keys and REGIONS keys,
    ask for JSON {"variable": ..., "region": ...}, validate, return dict.
    Returning None triggers the keyword fallback."""
    return None


def _keyword_translate(question: str) -> dict:
    q = question.lower()
    variable = next((k for k, words in KEYWORDS.items() if any(w in q for w in words)), "land_temperature")
    region = next((r for r in REGIONS if r in q), None)
    if region is None:
        region = "egypt" if any(w in q for w in ["مصر", "egypt"]) else "california"
    return {"variable": variable, "region": region, "bbox": REGIONS[region], "method": "keyword-fallback"}


if __name__ == "__main__":
    print(json.dumps(translate("Is drought getting worse in California?"), indent=2))
