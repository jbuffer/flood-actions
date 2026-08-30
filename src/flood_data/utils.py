"""Utility functions for flood data processing."""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


def extract_coordinates(
    geometry: dict[str, Any],
) -> tuple[Optional[float], Optional[float]]:
    """
    Extract latitude and longitude from GeoJSON geometry.

    Args:
        geometry: GeoJSON geometry dictionary

    Returns:
        Tuple of (longitude, latitude) or (None, None) if extraction fails
    """
    try:
        coords = geometry['coordinates']
        # Try nested array format first
        try:
            long = coords[0][0][0][0]
            lat = coords[0][0][0][1]
        except (TypeError, IndexError):
            # Fallback to simpler format
            long = coords[0][0][0]
            lat = coords[0][0][1]
        return float(long), float(lat)
    except (KeyError, IndexError, TypeError) as e:
        logger.warning(f"Failed to extract coordinates: {e}")
        return None, None


def ensure_data_directory(data_dir: str) -> None:
    """
    Ensure the data directory exists.

    Args:
        data_dir: Path to data directory
    """
    import os

    os.makedirs(data_dir, exist_ok=True)
    logger.debug(f"Data directory ensured at {data_dir}")


def create_empty_flood_dataframe():
    """
    Create an empty flood data dataframe with the correct schema.

    Returns:
        Empty pandas DataFrame with flood data columns
    """
    import pandas as pd

    return pd.DataFrame({
        'date': pd.to_datetime([]),
        'data_status': [],
        'flood_area_id': [],
        'county': [],
        'severity': [],
        'severity_level': [],
        'time_changed': [],
        'flood_id': [],
        'polygon_url': [],
        'riverorsea': []
    })
