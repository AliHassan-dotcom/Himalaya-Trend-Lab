"""
Calibrated Multi-Decade Regional Time-Series, Teleconnection, and Spatial Grid Generator.
Synthesizes physically realistic monthly Earth observation series anchored to published
Karakoram, Hindu Kush, and Western Himalaya glaciological benchmarks (including the
Karakoram Anomaly, May 2022 Shisper heatwave, 2022 monsoon extreme, and elevation lapse rates).
"""
import hashlib
from typing import Dict, Any, Optional
import numpy as np
import pandas as pd

from config.regions import get_region
from config.variables import get_variable, VARIABLES_CATALOGUE


def _deterministic_seed(key_str: str) -> int:
    """Generate a reproducible integer seed from any string identifier."""
    return int(hashlib.sha256(key_str.encode("utf-8")).hexdigest()[:8], 16)


def generate_teleconnection_series(start_year: int = 1981, end_year: int = 2026) -> pd.DataFrame:
    """
    Generate realistic monthly NAO, ENSO (Niño 3.4), and IOD indices from 1981 to 2026,
    capturing major historical events (1997/98 & 2015/16 El Niño, 2010 & 2022 La Niña).
    """
    dates = pd.date_range(f"{start_year}-01-01", f"{end_year}-10-01", freq="MS")
    n = len(dates)
    rng = np.random.default_rng(_deterministic_seed("teleconnections_global_v1"))

    t = np.arange(n) / 12.0
    years = dates.year.values
    months = dates.month.values

    # 1. North Atlantic Oscillation (NAO): multi-year winter-active oscillation
    nao = (
        0.55 * np.sin(2 * np.pi * t / 7.5 + 0.4)
        + 0.35 * np.cos(2 * np.pi * t / 3.8)
        + rng.normal(0, 0.55, n)
    )
    # Stronger winter westerlies in late 1990s / 2000s (Karakoram Anomaly phase)
    nao += np.where((years >= 1995) & (years <= 2012) & np.isin(months, [12, 1, 2, 3]), 0.42, 0.0)

    # 2. ENSO (Niño 3.4): ~3.5-5 year quasi-periodic cycle + historical spikes
    enso = (
        0.75 * np.sin(2 * np.pi * t / 4.3 - 0.8)
        + 0.40 * np.sin(2 * np.pi * t / 2.7 + 1.1)
        + rng.normal(0, 0.35, n)
    )
    # Historical El Niño peaks (1997-98, 2015-16, 2023-24) and La Niña troughs (2010-11, 2021-22)
    enso += np.where((years == 1997) | (years == 2015) | (years == 2023), 1.35, 0.0)
    enso -= np.where((years == 2010) | (years == 2022), 1.25, 0.0)

    # 3. Indian Ocean Dipole (IOD): slow warming tendency + 2.5-4 year oscillation
    iod = (
        0.08 * (years - 1990) / 10.0
        + 0.45 * np.sin(2 * np.pi * t / 3.4 + 0.3)
        + rng.normal(0, 0.32, n)
    )

    return pd.DataFrame({
        "date": dates,
        "year": years,
        "month": months,
        "nao_index": np.round(nao, 3),
        "enso_index": np.round(enso, 3),
        "iod_index": np.round(iod, 3),
    })


def _variable_baseline_params(
    region: Dict[str, Any],
    variable_id: str,
    glacier_only: bool = False,
) -> Dict[str, float]:
    """
    Compute physically consistent baseline mean, seasonal amplitude, peak month,
    decadal trend, noise std, and lag-1 autocorrelation for a (region, variable) pair.
    """
    dyn = region["baseline_dynamics"]
    elev_km = region["mean_elevation_m"] / 1000.0
    if glacier_only:
        # Glacier mask restricts to higher RGI glacier polygons (+550m mean elevation)
        elev_km += 0.55

    temp_slope = dyn["temp_trend_per_decade_c"]
    snow_slope = dyn["snow_cover_trend_per_decade_pct"]
    precip_slope = dyn["precip_trend_per_decade_mm"]
    swe_slope = dyn["swe_trend_per_decade_mm"]

    if variable_id == "t2m_merra2":
        # Lapse rate: ~15°C at sea level minus 6.2°C per km elevation
        base_mean = 15.5 - 6.1 * elev_km
        return {
            "mean": base_mean,
            "seasonal_amp": 11.8,
            "peak_month": 7.2,  # July peak
            "slope_per_decade": temp_slope * (1.08 if glacier_only else 1.0),
            "noise_std": 0.72,
            "ar1_phi": 0.34,
            "min_clip": -35.0,
            "max_clip": 35.0,
        }
    elif variable_id == "lst_modis":
        base_mean = 16.8 - 6.3 * elev_km
        return {
            "mean": base_mean,
            "seasonal_amp": 13.4,
            "peak_month": 7.0,
            "slope_per_decade": temp_slope * 1.12,
            "noise_std": 0.85,
            "ar1_phi": 0.30,
            "min_clip": -38.0,
            "max_clip": 42.0,
        }
    elif variable_id == "snow_cover_modis":
        base_mean = min(88.0, 22.0 + 10.5 * elev_km + (14.0 if glacier_only else 0.0))
        return {
            "mean": base_mean,
            "seasonal_amp": 26.0 if not glacier_only else 18.5,
            "peak_month": 2.5,  # Feb-Mar maximum snow extent
            "slope_per_decade": snow_slope * (0.85 if glacier_only else 1.0),
            "noise_std": 3.4,
            "ar1_phi": 0.42,
            "min_clip": 2.0,
            "max_clip": 99.5,
        }
    elif variable_id == "snow_depth_meteomatics":
        base_mean = max(15.0, (elev_km - 2.2) * 48.0 + (35.0 if glacier_only else 0.0))
        return {
            "mean": base_mean,
            "seasonal_amp": base_mean * 0.68,
            "peak_month": 3.0,  # March peak depth
            "slope_per_decade": snow_slope * 3.8,
            "noise_std": 9.5,
            "ar1_phi": 0.48,
            "min_clip": 0.0,
            "max_clip": 600.0,
        }
    elif variable_id == "precip_imerg":
        is_monsoon = "Himalaya" in region["parent_range"]
        base_mean = 68.0 if is_monsoon else 46.0
        return {
            "mean": base_mean,
            "seasonal_amp": 38.0 if is_monsoon else 24.0,
            "peak_month": 7.5 if is_monsoon else 3.2,
            "slope_per_decade": precip_slope,
            "noise_std": 16.5,  # High inter-annual mountain precipitation noise
            "ar1_phi": 0.16,
            "min_clip": 1.0,
            "max_clip": 350.0,
        }
    elif variable_id == "snowfall_merra2":
        base_mean = max(12.0, 14.0 + 6.5 * elev_km + (8.0 if glacier_only else 0.0))
        return {
            "mean": base_mean,
            "seasonal_amp": base_mean * 0.78,
            "peak_month": 2.2,
            "slope_per_decade": snow_slope * 1.45,
            "noise_std": 6.2,
            "ar1_phi": 0.25,
            "min_clip": 0.0,
            "max_clip": 220.0,
        }
    elif variable_id == "swe_gldas":
        base_mean = max(45.0, (elev_km - 2.0) * 82.0 + (55.0 if glacier_only else 0.0))
        return {
            "mean": base_mean,
            "seasonal_amp": base_mean * 0.62,
            "peak_month": 3.4,
            "slope_per_decade": swe_slope,
            "noise_std": 14.0,
            "ar1_phi": 0.52,
            "min_clip": 0.0,
            "max_clip": 950.0,
        }
    elif variable_id == "runoff_gldas":
        # Meltwater runoff increases in summer as glaciers ablate faster ("peak water" effect)
        base_mean = 52.0 + (12.0 if glacier_only else 0.0)
        runoff_slope = temp_slope * 14.5  # Accelerated summer melt runoff
        return {
            "mean": base_mean,
            "seasonal_amp": 48.0,
            "peak_month": 7.4,  # July-August peak melt runoff
            "slope_per_decade": runoff_slope,
            "noise_std": 8.8,
            "ar1_phi": 0.36,
            "min_clip": 1.0,
            "max_clip": 320.0,
        }
    elif variable_id == "humidity_airs":
        base_mean = 54.0 if "Himalaya" not in region["parent_range"] else 63.0
        return {
            "mean": base_mean,
            "seasonal_amp": 12.5,
            "peak_month": 7.8,
            "slope_per_decade": 0.65,
            "noise_std": 3.8,
            "ar1_phi": 0.28,
            "min_clip": 15.0,
            "max_clip": 96.0,
        }
    else:  # aerosols_omi (AOD 550nm)
        base_mean = 0.21 - 0.018 * elev_km
        return {
            "mean": max(0.08, base_mean),
            "seasonal_amp": 0.09,
            "peak_month": 5.8,  # Pre-monsoon / summer dust & soot transport
            "slope_per_decade": 0.024,  # Rising regional black-carbon/dust loading
            "noise_std": 0.022,
            "ar1_phi": 0.33,
            "min_clip": 0.02,
            "max_clip": 0.85,
        }


def generate_regional_series(
    region_id: str,
    variable_id: str,
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
    glacier_only: bool = False,
    custom_region: Optional[Dict[str, Any]] = None,
) -> pd.DataFrame:
    """
    Generate a calibrated monthly time series for a region and variable.
    Includes realistic AR(1) serial autocorrelation, seasonal harmonics,
    teleconnection couplings (NAO/ENSO), and documented historical extremes
    (e.g., May 2022 heatwave & August 2022 monsoon flood).
    """
    region = custom_region if custom_region else get_region(region_id)
    var_info = get_variable(variable_id)

    s_year = max(1981, start_year or var_info["start_year"])
    e_year = min(2026, end_year or var_info["end_year"])

    tele_df = generate_teleconnection_series(1981, 2026)
    tele_df = tele_df[(tele_df["year"] >= s_year) & (tele_df["year"] <= e_year)].reset_index(drop=True)

    dates = tele_df["date"]
    years = tele_df["year"].values
    months = tele_df["month"].values
    n = len(dates)

    params = _variable_baseline_params(region, variable_id, glacier_only=glacier_only)
    seed_key = f"{region['id']}_{variable_id}_{glacier_only}_v2"
    rng = np.random.default_rng(_deterministic_seed(seed_key))

    # Time in decades relative to start of record
    t_decades = (years + (months - 0.5) / 12.0 - s_year) / 10.0

    # 1. Seasonal cycle (primary annual + secondary semi-annual harmonic for realistic shape)
    phase = 2 * np.pi * (months - params["peak_month"]) / 12.0
    seasonal = (
        params["seasonal_amp"] * np.cos(phase)
        + 0.18 * params["seasonal_amp"] * np.sin(2 * phase)
    )

    # 2. Long-term secular trend + slight post-2006 non-linear acceleration
    trend = params["slope_per_decade"] * t_decades
    if variable_id in ("t2m_merra2", "lst_modis", "runoff_gldas"):
        post_2008 = np.maximum(0.0, (years - 2008) / 10.0)
        trend += 0.06 * params["slope_per_decade"] * (post_2008 ** 1.3)

    # 3. Physical Teleconnection Coupling (NAO boosts winter snow; ENSO/IOD modulate temp & monsoon)
    nao = tele_df["nao_index"].values
    enso = tele_df["enso_index"].values
    iod = tele_df["iod_index"].values

    tele_signal = np.zeros(n)
    if variable_id in ("snow_cover_modis", "snow_depth_meteomatics", "snowfall_merra2", "swe_gldas"):
        tele_signal = 0.35 * params["noise_std"] * nao - 0.20 * params["noise_std"] * iod
    elif variable_id in ("t2m_merra2", "lst_modis"):
        tele_signal = 0.25 * params["noise_std"] * enso + 0.22 * params["noise_std"] * iod
    elif variable_id == "precip_imerg":
        tele_signal = 0.30 * params["noise_std"] * nao - 0.28 * params["noise_std"] * enso

    # 4. AR(1) autocorrelated red noise
    ar_noise = np.zeros(n)
    phi = params["ar1_phi"]
    innovation_sd = params["noise_std"] * np.sqrt(max(0.1, 1.0 - phi ** 2))
    eps = rng.normal(0.0, innovation_sd, n)
    for i in range(1, n):
        ar_noise[i] = phi * ar_noise[i - 1] + eps[i]

    values = params["mean"] + seasonal + trend + tele_signal + ar_noise

    # 5. Inject Real Historical Compound Extremes (May 2022 Heatwave / Aug 2022 Monsoon / July 2010)
    for i in range(n):
        yr, mo = years[i], months[i]
        # March-May 2022 Extreme Heatwave (Triggered May 7, 2022 Shisper GLOF)
        if yr == 2022 and mo in (3, 4, 5):
            if variable_id in ("t2m_merra2", "lst_modis"):
                values[i] += 3.4 if mo == 5 else 2.6
            elif variable_id == "runoff_gldas":
                values[i] += 34.0
            elif variable_id in ("snow_cover_modis", "swe_gldas"):
                values[i] -= 1.8 * params["noise_std"]
        # July-August 2022 Pakistan Super-Flood Monsoon Intrusion
        if yr == 2022 and mo in (7, 8):
            if variable_id == "precip_imerg":
                values[i] += 68.0
            elif variable_id == "runoff_gldas":
                values[i] += 45.0
        # July-August 2010 Extreme Monsoon Event
        if yr == 2010 and mo in (7, 8) and variable_id in ("precip_imerg", "runoff_gldas"):
            values[i] += 52.0

    values = np.clip(values, params["min_clip"], params["max_clip"])

    # Quality flag (100% valid except occasional simulated MODIS cloud gap flags that are interpolated)
    quality_flag = np.where(
        (variable_id in ("snow_cover_modis", "lst_modis")) & (rng.random(n) < 0.03),
        "cloud_interpolated",
        "good",
    )

    return pd.DataFrame({
        "date": dates,
        "year": years,
        "month": months,
        "value": np.round(values, 3),
        "region_id": region["id"],
        "region_name": region["name"],
        "variable_id": variable_id,
        "variable_name": var_info["name"],
        "units": var_info["units"],
        "glacier_only": glacier_only,
        "quality_flag": quality_flag,
        "nao_index": tele_df["nao_index"].values,
        "enso_index": tele_df["enso_index"].values,
        "iod_index": tele_df["iod_index"].values,
    })


def generate_multivariate_series(
    region_id: str,
    start_year: int = 2000,
    end_year: int = 2026,
    glacier_only: bool = False,
    custom_region: Optional[Dict[str, Any]] = None,
) -> pd.DataFrame:
    """
    Generate an aligned monthly DataFrame containing all 10 Earth science variables
    plus NAO, ENSO, and IOD indices with physically coupled cryosphere anomalies
    (where temperature, snowfall, precipitation, humidity, and aerosols physically
    drive snow cover, snow depth, SWE, and meltwater runoff anomalies).
    """
    base_df: Optional[pd.DataFrame] = None
    for var_id in VARIABLES_CATALOGUE.keys():
        series_df = generate_regional_series(
            region_id=region_id,
            variable_id=var_id,
            start_year=start_year,
            end_year=end_year,
            glacier_only=glacier_only,
            custom_region=custom_region,
        )
        if base_df is None:
            base_df = series_df[["date", "year", "month", "nao_index", "enso_index", "iod_index"]].copy()
        base_df[var_id] = series_df["value"].values

    # Couple cryosphere response variables (snow_cover, snow_depth, swe, runoff)
    # to physical forcing anomalies (t2m, lst, snowfall, precip, aerosols, nao)
    t2m_anom = base_df["t2m_merra2"] - base_df.groupby("month")["t2m_merra2"].transform("mean")
    lst_anom = base_df["lst_modis"] - base_df.groupby("month")["lst_modis"].transform("mean")
    snowf_anom = base_df["snowfall_merra2"] - base_df.groupby("month")["snowfall_merra2"].transform("mean")
    precip_anom = base_df["precip_imerg"] - base_df.groupby("month")["precip_imerg"].transform("mean")
    aod_anom = base_df["aerosols_omi"] - base_df.groupby("month")["aerosols_omi"].transform("mean")

    # Physical coupling into Snow Cover Fraction (%)
    sc_clim = base_df.groupby("month")["snow_cover_modis"].transform("mean")
    sc_orig_anom = base_df["snow_cover_modis"] - sc_clim
    coupled_sc_anom = (
        -1.65 * t2m_anom
        - 0.75 * lst_anom
        + 0.28 * snowf_anom
        - 18.0 * aod_anom
        + 0.70 * base_df["nao_index"]
        + 0.28 * sc_orig_anom
    )
    base_df["snow_cover_modis"] = np.round(np.clip(sc_clim + coupled_sc_anom, 2.0, 99.5), 3)

    # Physical coupling into Snow Water Equivalent (SWE, mm)
    swe_clim = base_df.groupby("month")["swe_gldas"].transform("mean")
    swe_orig_anom = base_df["swe_gldas"] - swe_clim
    coupled_swe_anom = (
        -7.2 * t2m_anom
        - 2.8 * lst_anom
        + 1.35 * snowf_anom
        + 0.22 * precip_anom
        - 65.0 * aod_anom
        + 2.5 * base_df["nao_index"]
        + 0.25 * swe_orig_anom
    )
    base_df["swe_gldas"] = np.round(np.clip(swe_clim + coupled_swe_anom, 0.0, 950.0), 3)

    # Physical coupling into Meltwater Runoff (mm/month)
    run_clim = base_df.groupby("month")["runoff_gldas"].transform("mean")
    run_orig_anom = base_df["runoff_gldas"] - run_clim
    coupled_run_anom = (
        +5.4 * t2m_anom
        + 2.2 * lst_anom
        + 0.32 * precip_anom
        + 42.0 * aod_anom
        + 0.25 * run_orig_anom
    )
    base_df["runoff_gldas"] = np.round(np.clip(run_clim + coupled_run_anom, 1.0, 350.0), 3)

    return base_df


def generate_spatial_grid_data(
    region_id: str,
    variable_id: str,
    glacier_only: bool = False,
    grid_size: int = 10,
    custom_region: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Generate a 2D spatial grid over the region's bounding box with per-pixel
    elevation (m), RGI glacier mask boolean, decadal trend slope, p-value,
    and lag-1 autocorrelation for Spatial Trend Maps with FDR Significance Stippling.
    """
    region = custom_region if custom_region else get_region(region_id)
    bbox = region["bbox"]
    params = _variable_baseline_params(region, variable_id, glacier_only=glacier_only)

    lats = np.linspace(bbox["lat_min"], bbox["lat_max"], grid_size)
    lons = np.linspace(bbox["lon_min"], bbox["lon_max"], grid_size)
    lon_grid, lat_grid = np.meshgrid(lons, lats)

    rng = np.random.default_rng(_deterministic_seed(f"spatial_{region['id']}_{variable_id}_{grid_size}"))

    # Normalized north-south and east-west gradients (higher elevation towards NE Karakoram)
    norm_lat = (lat_grid - bbox["lat_min"]) / max(0.01, (bbox["lat_max"] - bbox["lat_min"]))
    norm_lon = (lon_grid - bbox["lon_min"]) / max(0.01, (bbox["lon_max"] - bbox["lon_min"]))

    # Synthetic SRTM/ALOS terrain elevation grid (m)
    elev_grid = (
        region["mean_elevation_m"]
        + 950.0 * (norm_lat - 0.45)
        + 650.0 * (norm_lon - 0.45)
        + rng.normal(0, 260.0, size=lat_grid.shape)
    )
    elev_grid = np.clip(elev_grid, region["elevation_range_m"][0], region["elevation_range_m"][1])

    # RGI Glacier Mask: high elevation cells have higher glacier probability
    glacier_threshold = np.percentile(elev_grid, max(15.0, 100.0 - region["glacier_fraction_pct"] * 1.8))
    rgi_mask = elev_grid >= glacier_threshold

    # Spatial variation in decadal trend:
    # Higher elevations (>4800m) show stronger Karakoram buffering for snow cover,
    # whereas lower valley tongues (<4000m) show steeper snow loss and warming.
    elev_anomaly_km = (elev_grid - region["mean_elevation_m"]) / 1000.0
    if variable_id in ("snow_cover_modis", "snow_depth_meteomatics", "swe_gldas", "snowfall_merra2"):
        slope_grid = (
            params["slope_per_decade"]
            + 0.85 * abs(params["slope_per_decade"]) * elev_anomaly_km
            + rng.normal(0, max(0.15, abs(params["slope_per_decade"]) * 0.22), size=lat_grid.shape)
        )
    else:
        slope_grid = (
            params["slope_per_decade"]
            + 0.14 * params["slope_per_decade"] * elev_anomaly_km
            + rng.normal(0, max(0.03, abs(params["slope_per_decade"]) * 0.20), size=lat_grid.shape)
        )

    # Compute realistic per-pixel Mann-Kendall p-values based on signal-to-noise ratio
    snr = np.abs(slope_grid) / (params["noise_std"] * 0.35 + 1e-6)
    raw_p_grid = np.exp(-1.45 * (snr ** 1.35)) + rng.uniform(0.0001, 0.025, size=lat_grid.shape)
    raw_p_grid = np.clip(raw_p_grid, 0.0001, 0.99)

    return {
        "region_id": region["id"],
        "region_name": region["name"],
        "variable_id": variable_id,
        "lats": lats.tolist(),
        "lons": lons.tolist(),
        "lat_grid": np.round(lat_grid, 4).tolist(),
        "lon_grid": np.round(lon_grid, 4).tolist(),
        "elevation_m": np.round(elev_grid, 1).tolist(),
        "rgi_glacier_mask": rgi_mask.tolist(),
        "slope_per_decade": np.round(slope_grid, 4).tolist(),
        "raw_p_value": np.round(raw_p_grid, 5).tolist(),
    }
