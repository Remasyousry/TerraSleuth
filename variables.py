"""Closed whitelist of variables the LLM translator may choose from.

Keeping this list small (6-8) prevents hallucinated datasets.
NOTE: verify each Earth Engine asset ID / band / scale in the GEE Data Catalog
before the hackathon freeze — catalog versions change.
"""

VARIABLES = {
    "precipitation": {
        "label": "Precipitation",
        "plain": "How much rain and snow falls, measured from space by the GPM mission.",
        "source": "NASA GPM IMERG (monthly)",
        "gee_asset": "NASA/GPM_L3/IMERG_MONTHLY_V06",
        "band": "precipitation",
        "unit": "mm/hr",
        "scale_m": 10000,
        "reducer": "mean",
    },
    "land_temperature": {
        "label": "Land surface temperature (day)",
        "plain": "How hot the ground surface is, measured by MODIS.",
        "source": "MODIS Terra MOD11A2 (8-day)",
        "gee_asset": "MODIS/061/MOD11A2",
        "band": "LST_Day_1km",
        "unit": "K (x0.02 scale factor applied)",
        "scale_factor": 0.02,
        "scale_m": 1000,
        "reducer": "mean",
    },
    "ndvi": {
        "label": "Vegetation greenness (NDVI)",
        "plain": "How green and dense plant cover is. Higher = more vegetation.",
        "source": "MODIS Terra MOD13A2 (16-day)",
        "gee_asset": "MODIS/061/MOD13A2",
        "band": "NDVI",
        "unit": "index (x0.0001 scale factor applied)",
        "scale_factor": 0.0001,
        "scale_m": 1000,
        "reducer": "mean",
    },
    "air_temperature": {
        "label": "Air temperature (2 m)",
        "plain": "Temperature of the air near the ground, from the MERRA-2 model.",
        "source": "MERRA-2 reanalysis",
        "gee_asset": "TODO: confirm MERRA-2 asset in GEE catalog (or use NASA GES DISC / Giovanni)",
        "band": "T2M",
        "unit": "K",
        "scale_m": 50000,
        "reducer": "mean",
    },
    "soil_moisture": {
        "label": "Soil moisture",
        "plain": "How wet the top layer of soil is, from the GLDAS land model.",
        "source": "GLDAS-2.1",
        "gee_asset": "NASA/GLDAS/V021/NOAH/G025/T3H",
        "band": "SoilMoi0_10cm_inst",
        "unit": "kg/m2",
        "scale_m": 27830,
        "reducer": "mean",
    },
    "evapotranspiration": {
        "label": "Evapotranspiration",
        "plain": "Water moving from land and plants into the air.",
        "source": "GLDAS-2.1",
        "gee_asset": "NASA/GLDAS/V021/NOAH/G025/T3H",
        "band": "Evap_tavg",
        "unit": "kg/m2/s",
        "scale_m": 27830,
        "reducer": "mean",
    },
}
