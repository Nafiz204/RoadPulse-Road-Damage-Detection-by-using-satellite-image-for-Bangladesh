"""
Feature Extraction Module for RoadPulse:
- Multi-spectral index formulas (NDWI, MNDWI, NDBI, BSI, NDVI)
- Temporal delta features between dry baseline and wet monsoon
- Corridor buffer zonal statistics aggregation
"""
import numpy as np
from typing import Dict, Any


def compute_spectral_indices(bands: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    """
    Compute standard remote sensing indices from Sentinel-2 surface reflectance bands.
    Bands required: B02 (Blue), B03 (Green), B04 (Red), B08 (NIR), B11 (SWIR1).
    """
    b2 = bands["B02"].astype(float)
    b3 = bands["B03"].astype(float)
    b4 = bands["B04"].astype(float)
    b8 = bands["B08"].astype(float)
    b11 = bands.get("B11", np.zeros_like(b8)).astype(float)
    
    eps = 1e-7  # Prevent division by zero
    
    # 1. Normalized Difference Vegetation Index (NDVI)
    ndvi = (b8 - b4) / (b8 + b4 + eps)
    
    # 2. Normalized Difference Water Index (NDWI - McFeeters)
    ndwi = (b3 - b8) / (b3 + b8 + eps)
    
    # 3. Modified NDWI (MNDWI - Xu) for enhanced open surface water
    mndwi = (b3 - b11) / (b3 + b11 + eps)
    
    # 4. Normalized Difference Built-up Index (NDBI - Zha et al.)
    ndbi = (b11 - b8) / (b11 + b8 + eps)
    
    # 5. Bare Soil Index (BSI - Diek et al.)
    bsi_num = (b11 + b4) - (b8 + b2)
    bsi_den = (b11 + b4) + (b8 + b2) + eps
    bsi = bsi_num / bsi_den
    
    return {
        "NDVI": ndvi,
        "NDWI": ndwi,
        "MNDWI": mndwi,
        "NDBI": ndbi,
        "BSI": bsi,
    }


def compute_temporal_deltas(
    dry_indices: Dict[str, np.ndarray],
    wet_indices: Dict[str, np.ndarray]
) -> Dict[str, np.ndarray]:
    """
    Compute temporal difference metrics between dry baseline and wet monsoon period.
    """
    deltas = {}
    for key in dry_indices:
        if key in wet_indices:
            deltas[f"delta_{key}"] = wet_indices[key] - dry_indices[key]
    return deltas


def extract_corridor_zonal_stats(values_1d: np.ndarray, prefix: str = "") -> Dict[str, float]:
    """
    Compute robust summary statistics over road corridor pixel values.
    Filters out NaN values caused by cloud masking.
    """
    valid = values_1d[~np.isnan(values_1d)]
    pfx = f"{prefix}_" if prefix else ""
    
    if len(valid) == 0:
        return {
            f"{pfx}mean": np.nan,
            f"{pfx}std": np.nan,
            f"{pfx}p10": np.nan,
            f"{pfx}p90": np.nan,
            f"{pfx}valid_count": 0,
        }
        
    return {
        f"{pfx}mean": float(np.mean(valid)),
        f"{pfx}std": float(np.std(valid)),
        f"{pfx}p10": float(np.percentile(valid, 10)),
        f"{pfx}p90": float(np.percentile(valid, 90)),
        f"{pfx}valid_count": int(len(valid)),
    }
