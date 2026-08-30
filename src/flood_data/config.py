"""Configuration settings for flood data collection."""

import os

# API Configuration
FLOOD_API_URL: str = "http://environment.data.gov.uk/flood-monitoring/id/floods"

# Data paths
DATA_DIR: str = os.getenv("DATA_DIR", "data")
CSV_FILENAME: str = "flood-data.csv"
CSV_PATH: str = os.path.join(DATA_DIR, CSV_FILENAME)

# Request settings
REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "10"))

# Column definitions for the flood data
FLOOD_COLUMNS: list[str] = [
    "date",
    "data_status",
    "flood_area_id",
    "county",
    "severity",
    "severity_level",
    "time_changed",
    "flood_id",
    "polygon_url",
    "riverorsea",
]

POLYGON_COLUMNS: list[str] = ["coords", "long", "lat", "description", "CTY19NM"]
