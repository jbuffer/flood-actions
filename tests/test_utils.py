"""Tests for utils module."""

import os
import tempfile

from src.flood_data.utils import create_empty_flood_dataframe, ensure_data_directory


class TestEnsureDataDirectory:
    """Test data directory creation."""

    def test_create_directory(self):
        """Test that directory is created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = os.path.join(tmpdir, "test_data")
            ensure_data_directory(test_dir)
            assert os.path.exists(test_dir)

    def test_existing_directory(self):
        """Test that existing directory is handled gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ensure_data_directory(tmpdir)
            assert os.path.exists(tmpdir)


class TestCreateEmptyFloodDataframe:
    """Test empty dataframe creation."""

    def test_empty_dataframe_structure(self):
        """Test that empty dataframe has correct structure."""
        df = create_empty_flood_dataframe()
        assert df.empty
        assert "flood_area_id" in df.columns
        assert "date" in df.columns
        assert "county" in df.columns
