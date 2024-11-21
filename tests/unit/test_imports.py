"""Test module imports."""


def test_utils_imports():
    """Test utils package imports."""
    from src.utils import DataProcessor, ErrorHandler, logger

    assert all([DataProcessor, ErrorHandler, logger])


def test_visualizations_imports():
    """Test visualizations package imports."""
    from src.visualizations import create_program_charts, create_program_overview

    assert all([create_program_charts, create_program_overview])


def test_package_all_exports():
    """Test package exports are complete."""
    import src

    expected = {
        "ErrorHandler",
        "logger",
        "DataProcessor",
        "create_program_charts",
        "create_program_overview",
    }
    assert set(src.__all__) == expected
