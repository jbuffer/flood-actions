![flood-api-call](https://github.com/jbuffer/flood-actions/actions/workflows/api-daily-call.yml/badge.svg)
![linting](https://github.com/jbuffer/flood-actions/actions/workflows/flake8.yml/badge.svg)

# Flood API Call Data Warehousing

<img src="https://media.giphy.com/media/if4XHBAIKurDohCbZF/giphy.gif" width="50px"/>

## Overview

A repository that uses GitHub Actions to schedule daily requests of flood data from the [Environment Agency API](https://www.gov.uk/topic/environmental-management/flooding-coastal-change) and appends the data to a CSV file. The data collection is automated through CI/CD workflows, and the resulting dataset can be used for further analysis and visualization.

## Features

- **Automated Data Collection**: Daily GitHub Actions workflow fetches latest flood alerts
- **Polygon Data**: Retrieves geographic boundaries and coordinates for each flood area
- **Duplicate Handling**: Automatically removes duplicate entries based on flood area IDs
- **Historical Tracking**: Maintains a time-series dataset of all flood alerts
- **Comprehensive Testing**: Unit tests for data fetching and processing logic
- **Type Hints**: Python 3.9+ type annotations for better code clarity

## Project Structure

```
flood-actions/
├── .github/
│   └── workflows/
│       ├── api-daily-call.yml      # GitHub Actions workflow for daily data fetch
│       └── flake8.yml               # Linting workflow
├── src/
│   ├── __init__.py
│   └── flood_data/
│       ├── __init__.py
│       ├── config.py                # Configuration settings
│       ├── fetch.py                 # Main data fetching logic
│       └── utils.py                 # Utility functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Pytest fixtures
│   ├── test_fetch.py                # Tests for fetch module
│   ├── test_utils.py                # Tests for utils module
│   └── test_config.py               # Tests for config module
├── data/
│   └── flood-data.csv               # Historical flood data (auto-generated)
├── notebooks/
│   └── Testing.ipynb                # Data exploration notebook
├── .env.example                     # Example environment variables
├── .flake8                          # Flake8 linting configuration
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml                   # Project metadata and tool configuration
├── pytest.ini                       # Pytest configuration
├── requirements.txt                 # Production dependencies
├── requirements-dev.txt             # Development dependencies
└── setup.py                         # Package setup configuration
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip or conda package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/jbuffer/flood-actions.git
   cd flood-actions
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   # Using venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Or using conda
   conda create -n flood-actions python=3.9
   conda activate flood-actions
   ```

3. **Install dependencies**
   ```bash
   # For production use
   pip install -r requirements.txt
   
   # For development (includes testing and linting tools)
   pip install -r requirements-dev.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your desired settings (optional, defaults are provided)
   ```

## Usage

### Running Data Collection

**As a standalone script:**
```bash
python -m src.flood_data.fetch
```

**As a module:**
```python
from src.flood_data.fetch import get_data

get_data()
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src

# Run specific test file
pytest tests/test_fetch.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Run linting
flake8 src/ tests/

# Format code with black
black src/ tests/

# Check type hints
mypy src/

# Sort imports
isort src/ tests/
```

## Data Schema

### flood-data.csv

| Column | Type | Description |
|--------|------|-------------|
| date | datetime | Date when the data was fetched |
| data_status | string | Status of data ('Data available' or 'No Flood Data') |
| flood_area_id | string | Unique identifier for the flood area |
| county | string | County name |
| severity | string | Severity level (e.g., Warning, Alert) |
| severity_level | integer | Numeric severity level |
| time_changed | datetime | When the severity status changed |
| flood_id | string | Unique flood ID |
| polygon_url | string | URL to geographic polygon data |
| riverorsea | string | Whether the flood is from river or sea |
| coords | object | GeoJSON geometry coordinates |
| long | float | Longitude coordinate |
| lat | float | Latitude coordinate |
| description | string | Geographic area description |
| CTY19NM | string | Local authority name |

## API Reference

### Environment Agency Flood Monitoring API

- **Base URL**: http://environment.data.gov.uk/flood-monitoring/id/floods
- **Documentation**: [Environment Agency API Docs](https://www.gov.uk/government/organisations/environment-agency)
- **Data License**: [Open Government License](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)

## Configuration

Environment variables can be set in `.env` file:

- `DATA_DIR`: Directory to store CSV data (default: `data`)
- `REQUEST_TIMEOUT`: API request timeout in seconds (default: `10`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

## GitHub Actions Workflow

The repository includes two automated workflows:

1. **api-daily-call.yml**: Runs daily to fetch new flood data
2. **flake8.yml**: Runs linting checks on code changes

## Future Enhancements

1. This data will be used in the [flood application](https://github.com/jbuffer/flood-dashboard)
2. The data will be migrated from CSV to a PostgreSQL database
3. Add data visualization dashboard
4. Implement real-time alerts via webhooks
5. Add support for historical data archives

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or suggestions, please open an [issue](https://github.com/jbuffer/flood-actions/issues) on GitHub.
