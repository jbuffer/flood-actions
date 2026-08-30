"""Unit tests for flood data fetching."""

from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np

from src.flood_data.fetch import fetch_flood_data, fetch_polygon_data, get_data
from src.flood_data.utils import extract_coordinates


class TestExtractCoordinates:
    """Test coordinate extraction from GeoJSON."""

    def test_extract_nested_coordinates(self):
        """Test extraction from nested coordinate array."""
        geometry = {
            'coordinates': [[[-1.5, 52.5], [-1.4, 52.6]]]
        }
        long, lat = extract_coordinates(geometry)
        assert long == -1.5
        assert lat == 52.5

    def test_extract_simple_coordinates(self):
        """Test extraction from simple coordinate array."""
        geometry = {
            'coordinates': [[-1.5, 52.5]]
        }
        long, lat = extract_coordinates(geometry)
        assert long == -1.5
        assert lat == 52.5

    def test_extract_coordinates_invalid(self):
        """Test extraction from invalid geometry."""
        geometry = {'coordinates': []}
        long, lat = extract_coordinates(geometry)
        assert long is None
        assert lat is None


class TestFetchFloodData:
    """Test flood data fetching."""

    @patch('src.flood_data.fetch.requests.get')
    def test_fetch_flood_data_success(self, mock_get, mock_flood_response):
        """Test successful API response."""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_flood_response
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        df = fetch_flood_data()

        assert not df.empty
        assert 'flood_area_id' in df.columns
        assert df['data_status'].iloc[0] == 'Data available'

    @patch('src.flood_data.fetch.requests.get')
    def test_fetch_flood_data_empty_response(self, mock_get):
        """Test empty API response."""
        mock_response = MagicMock()
        mock_response.json.return_value = {'items': []}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        df = fetch_flood_data()

        assert not df.empty
        assert df['data_status'].iloc[0] == 'No Flood Data'

    @patch('src.flood_data.fetch.requests.get')
    def test_fetch_flood_data_api_error(self, mock_get):
        """Test API connection error."""
        mock_get.side_effect = Exception("Connection error")

        df = fetch_flood_data()

        assert df['data_status'].iloc[0] == 'No Flood Data'


class TestFetchPolygonData:
    """Test polygon data fetching."""

    @patch('src.flood_data.fetch.requests.get')
    def test_fetch_polygon_data_success(
        self, mock_get, sample_flood_dataframe, mock_polygon_response
    ):
        """Test successful polygon data fetching."""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_polygon_response
        mock_get.return_value = mock_response

        df_poly = fetch_polygon_data(sample_flood_dataframe)

        assert not df_poly.empty
        assert 'coords' in df_poly.columns
        assert df_poly['CTY19NM'].iloc[0] == 'Test Council'

    def test_fetch_polygon_data_no_flood_area(self):
        """Test polygon data with no flood area."""
        df = pd.DataFrame({
            'flood_area_id': [np.nan],
            'polygon_url': [None]
        })

        df_poly = fetch_polygon_data(df)

        assert df_poly['long'].isna().all()
        assert df_poly['lat'].isna().all()


class TestGetData:
    """Test main get_data function."""

    @patch('src.flood_data.fetch.fetch_polygon_data')
    @patch('src.flood_data.fetch.fetch_flood_data')
    @patch('src.flood_data.fetch.pd.read_csv')
    def test_get_data_new_file(
        self, mock_read_csv, mock_fetch_flood, mock_fetch_poly
    ):
        """Test get_data when CSV doesn't exist."""
        mock_read_csv.side_effect = FileNotFoundError()
        mock_fetch_flood.return_value = pd.DataFrame({
            'flood_area_id': ['test-1'],
            'date': pd.to_datetime(['2024-01-01'])
        })
        mock_fetch_poly.return_value = pd.DataFrame({
            'long': [-1.5],
            'lat': [52.5]
        })

        with patch('src.flood_data.fetch.df.to_csv'):
            get_data()

        mock_fetch_flood.assert_called_once()
        mock_fetch_poly.assert_called_once()
