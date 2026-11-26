"""
Preprocessing Module for RoadPulse:
- Metric reprojection (UTM Zone 45N / 46N)
- Road linestring segmentation into uniform 100m intervals
- 15m corridor buffer generation
- Scene Classification Layer (SCL) cloud masking
"""
from typing import List
import numpy as np

try:
    import geopandas as gpd
    from shapely.geometry import LineString, Point, Polygon
    from shapely.ops import substring
except ImportError:
    pass

from src.config import ROAD_SEGMENT_LENGTH_M, ROAD_BUFFER_DISTANCE_M, SCL_INVALID_VALUES


def segment_linestring(geom: "LineString", segment_length_m: float = ROAD_SEGMENT_LENGTH_M) -> List["LineString"]:
    """
    Subdivide a continuous LineString geometry into uniform metric length intervals.
    
    Args:
        geom: Shapely LineString (must be in a metric projection like UTM)
        segment_length_m: Target length per sub-segment in meters (default 100m)
        
    Returns:
        List of Shapely LineString objects
    """
    total_length = geom.length
    if total_length <= segment_length_m:
        return [geom]
    
    segments = []
    current_dist = 0.0
    while current_dist < total_length:
        end_dist = min(current_dist + segment_length_m, total_length)
        sub_geom = substring(geom, current_dist, end_dist)
        if sub_geom.length > 5.0:  # Exclude tiny residue segments under 5m
            segments.append(sub_geom)
        current_dist = end_dist
        
    return segments


def create_road_corridor_buffers(
    gdf_roads: "gpd.GeoDataFrame",
    target_utm_crs: str,
    buffer_distance_m: float = ROAD_BUFFER_DISTANCE_M,
    segment_length_m: float = ROAD_SEGMENT_LENGTH_M,
) -> "gpd.GeoDataFrame":
    """
    Transform raw road geometries into uniform 100m segments with 15m corridor buffers.
    
    Args:
        gdf_roads: GeoPandas DataFrame of roads (WGS84 EPSG:4326)
        target_utm_crs: Target UTM CRS (e.g. EPSG:32646)
        buffer_distance_m: Radius of buffer in meters (default 15m)
        segment_length_m: Segment subdivision length in meters (default 100m)
        
    Returns:
        GeoDataFrame containing segmented centerlines and 15m buffer polygons
    """
    # 1. Reproject to metric UTM
    gdf_utm = gdf_roads.to_crs(target_utm_crs)
    
    records = []
    for idx, row in gdf_utm.iterrows():
        geom = row.geometry
        if geom.geom_type == "LineString":
            sub_segments = segment_linestring(geom, segment_length_m)
            for seg_idx, sub_seg in enumerate(sub_segments):
                corridor_poly = sub_seg.buffer(buffer_distance_m)
                rec = {
                    "orig_id": row.get("id", idx),
                    "highway": row.get("highway", "unclassified"),
                    "name": row.get("name", "Unknown"),
                    "seg_index": seg_idx,
                    "length_m": sub_seg.length,
                    "centerline": sub_seg,
                    "geometry": corridor_poly,  # Primary geometry is the 15m buffer
                }
                records.append(rec)
                
    gdf_corridors = gpd.GeoDataFrame(records, crs=target_utm_crs)
    return gdf_corridors


def apply_scl_cloud_mask(band_array: np.ndarray, scl_array: np.ndarray) -> np.ndarray:
    """
    Mask cloud, shadow, and invalid pixels using Sentinel-2 Scene Classification Layer (SCL).
    
    Args:
        band_array: 2D or 3D multi-spectral reflectance array
        scl_array: 2D array of SCL classes
        
    Returns:
        np.ndarray with invalid pixels replaced by NaN
    """
    mask = np.isin(scl_array, SCL_INVALID_VALUES)
    masked = band_array.astype(float).copy()
    masked[mask] = np.nan
    return masked
