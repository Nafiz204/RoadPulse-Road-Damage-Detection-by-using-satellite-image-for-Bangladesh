"""
Project configuration, constants, and parameters for RoadPulse.
"""
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_VECTORS_DIR = DATA_DIR / "raw_vectors"
PROCESSED_VECTORS_DIR = DATA_DIR / "processed_vectors"
GROUND_TRUTH_DIR = DATA_DIR / "ground_truth"
FEATURES_DIR = DATA_DIR / "features"

# Coordinate Reference Systems
CRS_WGS84 = "EPSG:4326"
CRS_UTM45N = "EPSG:32645"  # Western Bangladesh
CRS_UTM46N = "EPSG:32646"  # Eastern Bangladesh (Sylhet, Sunamganj, Chittagong)

# Road Corridor Parameters
ROAD_SEGMENT_LENGTH_M = 100.0  # Length of each sub-segment in meters
ROAD_BUFFER_DISTANCE_M = 15.0  # Corridor buffer radius in meters

# Road Types to Extract from OpenStreetMap
TARGET_HIGHWAY_TYPES = [
    "trunk",
    "primary",
    "secondary",
    "tertiary",
    "unclassified",
    "trunk_link",
    "primary_link",
    "secondary_link",
]

# Pilot Upazilas (Bounding Boxes in WGS84: [min_lon, min_lat, max_lon, max_lat])
PILOT_UPAZILAS = {
    "sunamganj_sadar": {
        "name": "Sunamganj Sadar",
        "district": "Sunamganj",
        "division": "Sylhet",
        "utm_crs": CRS_UTM46N,
        "bbox": [91.30, 24.98, 91.50, 25.15],
    },
    "chhatak": {
        "name": "Chhatak",
        "district": "Sunamganj",
        "division": "Sylhet",
        "utm_crs": CRS_UTM46N,
        "bbox": [91.55, 24.95, 91.75, 25.12],
    },
    "kurigram_sadar": {
        "name": "Kurigram Sadar",
        "district": "Kurigram",
        "division": "Rangpur",
        "utm_crs": CRS_UTM45N,
        "bbox": [89.55, 25.75, 89.75, 25.90],
    },
}

# Sentinel-2 Bands & Resolutions
SENTINEL2_BANDS = {
    "B02": {"name": "Blue", "resolution_m": 10},
    "B03": {"name": "Green", "resolution_m": 10},
    "B04": {"name": "Red", "resolution_m": 10},
    "B08": {"name": "NIR", "resolution_m": 10},
    "B11": {"name": "SWIR1", "resolution_m": 20},
    "B12": {"name": "SWIR2", "resolution_m": 20},
    "SCL": {"name": "SceneClassification", "resolution_m": 20},
}

# SCL Cloud & Invalid Pixel Mask Values
# (3: Cloud shadow, 8: Cloud med prob, 9: Cloud high prob, 10: Cirrus, 11: Snow/Ice)
SCL_INVALID_VALUES = [0, 1, 3, 8, 9, 10, 11]

# Seasonal Time Windows (2024 Monsoon Flood Year)
SEASONAL_WINDOWS = {
    "dry_baseline": {
        "start_date": "2024-02-01",
        "end_date": "2024-04-30",
        "max_cloud_cover": 15,
    },
    "wet_monsoon": {
        "start_date": "2024-07-01",
        "end_date": "2024-10-31",
        "max_cloud_cover": 40,
    },
}

# Road Damage Classification Targets
CONDITION_CLASSES = {
    0: {"label": "Intact / Paved", "color": "#28a745", "hex_rgb": (40, 167, 69)},
    1: {"label": "Degraded / Earthen", "color": "#ffc107", "hex_rgb": (255, 193, 7)},
    2: {"label": "Submerged / Washed Out", "color": "#dc3545", "hex_rgb": (220, 53, 69)},
}
