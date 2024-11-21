"""Streamlit pages initialization."""

from typing import Dict

# Page registry
PAGES: Dict[str, str] = {
    "Program Overview": "1_📊_Program_Overview.py",
    "Sprint Metrics": "2_🏃_Sprint_Metrics.py",
    "Epic Tracking": "3_🎯_Epic_Tracking.py",
    "Team Analysis": "4_👥_Team_Analysis.py",
    "Quality Metrics": "5_🔍_Quality_Metrics.py",
}

__all__ = ["PAGES"]
