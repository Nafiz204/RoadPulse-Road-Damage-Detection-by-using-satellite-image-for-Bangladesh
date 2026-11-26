"""
Data Ingestion Module for RoadPulse:
- Queries road networks from OpenStreetMap (via OSMnx or Overpass API)
- Queries Sentinel-2 Level-2A multi-spectral scenes via Microsoft Planetary Computer STAC
"""
import requests
from typing import Dict, Any, List, Optional
import json

from src.config import PILOT_UPAZILAS, TARGET_HIGHWAY_TYPES, SEASONAL_WINDOWS


def fetch_osm_roads_overpass(bbox: List[float], output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Query OpenStreetMap road vectors for a bounding box using the Overpass API.
    
    Args:
        bbox: [min_lon, min_lat, max_lon, max_lat] in WGS84
        output_path: Optional file path to save raw GeoJSON response
        
    Returns:
        Dict: Overpass GeoJSON / JSON response containing road LineStrings and tags
    """
    min_lon, min_lat, max_lon, max_lat = bbox
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    highway_filter = "|".join(TARGET_HIGHWAY_TYPES)
    query = f"""
    [out:json][timeout:60];
    (
      way["highway"~"^({highway_filter})$"]({min_lat},{min_lon},{max_lat},{max_lon});
    );
    out body;
    >;
    out skel qt;
    """
    
    print(f"[OSM Ingestion] Querying Overpass API for bbox {bbox}...")
    response = requests.post(overpass_url, data={"data": query})
    response.raise_for_status()
    data = response.json()
    
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[OSM Ingestion] Saved raw OSM data to {output_path}")
        
    return data


def query_planetary_computer_stac(
    bbox: List[float],
    season: str = "dry_baseline",
    max_items: int = 10
) -> List[Any]:
    """
    Query Microsoft Planetary Computer STAC endpoint for Sentinel-2 L2A tiles.
    
    Args:
        bbox: [min_lon, min_lat, max_lon, max_lat] in WGS84
        season: "dry_baseline" or "wet_monsoon"
        max_items: Maximum items to retrieve
        
    Returns:
        List of signed STAC items ready for band streaming / downloading
    """
    try:
        from pystac_client import Client
        import planetary_computer
    except ImportError:
        raise ImportError(
            "pystac-client and planetary-computer packages are required. "
            "Install via: pip install pystac-client planetary-computer"
        )
        
    cfg = SEASONAL_WINDOWS.get(season, SEASONAL_WINDOWS["dry_baseline"])
    datetime_range = f"{cfg['start_date']}/{cfg['end_date']}"
    
    catalog_url = "https://planetarycomputer.microsoft.com/api/stac/v1"
    catalog = Client.open(catalog_url, modifier=planetary_computer.sign_inplace)
    
    print(f"[STAC Query] Searching Sentinel-2 L2A for season '{season}' ({datetime_range})...")
    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime=datetime_range,
        query={"eo:cloud_cover": {"lt": cfg["max_cloud_cover"]}},
        max_items=max_items,
    )
    
    items = list(search.items())
    print(f"[STAC Query] Found {len(items)} matching Sentinel-2 scenes.")
    return items


if __name__ == "__main__":
    pilot = PILOT_UPAZILAS["sunamganj_sadar"]
    print(f"Testing data ingestion configuration for pilot: {pilot['name']}")
    print(f"Bounding box: {pilot['bbox']}")
