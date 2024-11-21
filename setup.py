"""Setup script for backward compatibility."""

from setuptools import find_packages, setup

setup(
    name="jira-dashboard",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "pandas",
        "plotly",
        "setuptools",
    ],
    python_requires=">=3.8",
)
