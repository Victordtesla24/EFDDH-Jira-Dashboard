"""Pytest configuration and fixtures."""

import pytest
import os
import sys

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(project_root))

@pytest.fixture(scope="session")
def project_path():
    """Return the project root path."""
    return project_root
