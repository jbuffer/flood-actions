"""Shared pytest fixtures and configuration."""

import pandas as pd
import pytest


@pytest.fixture
def mock_flood_response():
    """Mock API response for flood data."""
    return {
        "items": [
            {
                "floodAreaID": "test-area-1",
                "floodArea": {
                    "county": "Test County",
                    "@id": "flood-id-1",
                    "polygon": "http://example.com/poly1.json",
                    "riverOrSea": "River",
                },
                "severity": "Warning",
                "severityLevel": 2,
                "timeSeverityChanged": "2024-01-01T12:00:00",
            }
        ]
    }


@pytest.fixture
def mock_polygon_response():
    """Mock API response for polygon data."""
    return {
        "features": [
            {
                "geometry": {"coordinates": [[[-1.5, 52.5], [-1.4, 52.6]]]},
                "properties": {
                    "DESCRIP": "Test area description",
                    "LA_NAME": "Test Council",
                },
            }
        ]
    }


@pytest.fixture
def sample_flood_dataframe():
    """Sample flood data dataframe."""
    return pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01"]),
            "data_status": ["Data available"],
            "flood_area_id": ["test-area-1"],
            "county": ["Test County"],
            "severity": ["Warning"],
            "severity_level": [2],
            "time_changed": ["2024-01-01T12:00:00"],
            "flood_id": ["flood-id-1"],
            "polygon_url": ["http://example.com/poly1.json"],
            "riverorsea": ["River"],
        }
    )
