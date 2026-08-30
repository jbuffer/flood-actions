"""Fetch and process flood data from Environment Agency API."""

import logging
from datetime import datetime
from typing import Any

import numpy as np
import pandas as pd
import requests

from src.flood_data.config import FLOOD_API_URL, CSV_PATH, REQUEST_TIMEOUT, DATA_DIR
from src.flood_data.utils import extract_coordinates, ensure_data_directory

logger = logging.getLogger(__name__)


def fetch_flood_data() -> pd.DataFrame:
    """
    Fetch current flood data from the Environment Agency API.

    Returns:
        DataFrame containing current flood alerts with empty data_status
        column if no floods are reported.

    Raises:
        requests.RequestException: If API request fails
    """
    data: list[dict[str, Any]] = []

    try:
        response = requests.get(FLOOD_API_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        logger.info("Successfully fetched flood data from API")

        api_data = response.json()

        for item in api_data.get("items", []):
            flood_record = {
                "date": datetime.today(),
                "data_status": "Data available",
                "flood_area_id": item.get("floodAreaID"),
                "county": item.get("floodArea", {}).get("county"),
                "severity": item.get("severity"),
                "severity_level": item.get("severityLevel"),
                "time_changed": item.get("timeSeverityChanged"),
                "flood_id": item.get("floodArea", {}).get("@id"),
                "polygon_url": item.get("floodArea", {}).get("polygon"),
                "riverorsea": item.get("floodArea", {}).get("riverOrSea"),
            }
            data.append(flood_record)

        df = pd.DataFrame(data)

    except requests.RequestException as e:
        logger.error(f"Failed to connect to API: {e}")
        df = pd.DataFrame()

    # Create empty dataframe if no data received
    if df.empty:
        logger.info("No flood data available, creating empty dataframe")
        df = pd.DataFrame(
            {
                "date": [datetime.today()],
                "data_status": ["No Flood Data"],
                "flood_area_id": [np.nan],
                "county": [np.nan],
                "severity": [np.nan],
                "severity_level": [np.nan],
                "time_changed": [np.nan],
                "flood_id": [np.nan],
                "polygon_url": [np.nan],
                "riverorsea": [np.nan],
            }
        )

    return df


def fetch_polygon_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fetch additional polygon geometry data for each flood area.

    Args:
        df: DataFrame with flood data containing polygon_url column

    Returns:
        DataFrame with polygon data (coords, long, lat, description, CTY19NM)
    """
    poly_data: list[dict[str, Any]] = []

    for idx, row in df.iterrows():
        poly_record: dict[str, Any] = {}

        if pd.isna(row["flood_area_id"]):
            # No flood data, set NaN values
            poly_record = {
                "coords": np.nan,
                "long": np.nan,
                "lat": np.nan,
                "description": np.nan,
                "CTY19NM": np.nan,
            }
        else:
            try:
                url = row["polygon_url"]
                logger.debug(f"Fetching polygon data from {url}")
                response = requests.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                geo_data = response.json()

                features = geo_data.get("features", [])
                if features:
                    feature = features[0]
                    geometry = feature.get("geometry", {})
                    properties = feature.get("properties", {})

                    long, lat = extract_coordinates(geometry)

                    poly_record = {
                        "coords": geometry,
                        "long": long,
                        "lat": lat,
                        "description": properties.get("DESCRIP"),
                        "CTY19NM": properties.get("LA_NAME"),
                    }
                else:
                    poly_record = {
                        "coords": np.nan,
                        "long": np.nan,
                        "lat": np.nan,
                        "description": np.nan,
                        "CTY19NM": np.nan,
                    }
                    flood_id = row["flood_area_id"]
                    logger.warning(
                        f"No features found in polygon response for " f"{flood_id}"
                    )

            except (requests.RequestException, KeyError, IndexError) as e:
                logger.error(f"Error fetching polygon data: {e}")
                poly_record = {
                    "coords": np.nan,
                    "long": np.nan,
                    "lat": np.nan,
                    "description": np.nan,
                    "CTY19NM": np.nan,
                }

        poly_data.append(poly_record)

    return pd.DataFrame(poly_data)


def get_data() -> None:
    """
    Main function to fetch flood data and append to historical dataset.

    This function:
    1. Fetches current flood alerts from the API
    2. Fetches polygon geometry data for each alert
    3. Combines the data
    4. Removes duplicates
    5. Appends to historical CSV file
    6. Saves the updated dataset
    """
    logger.info("Starting flood data collection")

    try:
        # Ensure data directory exists
        ensure_data_directory(DATA_DIR)

        # Fetch current flood data
        df_floods = fetch_flood_data()

        # Fetch polygon data
        df_poly = fetch_polygon_data(df_floods)

        # Combine flood and polygon data
        df_current = pd.concat([df_floods, df_poly], axis=1)

        # Remove duplicates
        df_current = df_current.drop_duplicates(subset=["flood_area_id"])

        # Read historical data
        try:
            df_historical = pd.read_csv(CSV_PATH)
            logger.info(f"Loaded historical data from {CSV_PATH}")
        except FileNotFoundError:
            msg = f"No historical data found at {CSV_PATH}, creating new file"
            logger.warning(msg)
            df_historical = df_current.copy()

        # Append new data
        df_updated = pd.concat([df_historical, df_current], ignore_index=True)

        # Process dates
        df_updated["date"] = pd.to_datetime(df_updated["date"])
        df_updated = df_updated.sort_values("date", ascending=False)

        # Save updated file
        df_updated.to_csv(CSV_PATH, index=False)
        logger.info(f"Updated dataset saved to {CSV_PATH}")

    except Exception as e:
        logger.error(f"Error in get_data: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    get_data()
