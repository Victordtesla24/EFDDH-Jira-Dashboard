"""Test package imports and initialization."""

import pytest
import os
import sys

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

def test_utils_imports():
    """Test utils package imports."""
    from src.utils import ErrorHandler, logger, DataProcessor
    assert ErrorHandler is not None
    assert logger is not None
    assert DataProcessor is not None

def test_visualizations_imports():
    """Test visualizations package imports."""
    from src.visualizations import create_program_overview, create_program_charts
    assert create_program_overview is not None
    assert create_program_charts is not None

def test_package_all_exports():
    """Test package exports are complete."""
    import src
    expected = {
        "ErrorHandler",
        "logger",
        "DataProcessor",
        "create_program_overview",
        "create_program_charts"
    }
    assert set(src.__all__) == expected
