"""Tests for config module."""

from src.flood_data import config


def test_api_url_configured():
    """Test that API URL is configured."""
    assert config.FLOOD_API_URL == "http://environment.data.gov.uk/flood-monitoring/id/floods"


def test_csv_path_configured():
    """Test that CSV path is configured."""
    assert config.CSV_PATH.endswith('flood-data.csv')


def test_columns_defined():
    """Test that columns are properly defined."""
    assert len(config.FLOOD_COLUMNS) > 0
    assert 'date' in config.FLOOD_COLUMNS
    assert len(config.POLYGON_COLUMNS) > 0
    assert 'long' in config.POLYGON_COLUMNS
