"""Metrics calculation module."""

from typing import Any, Dict

import pandas as pd


class MetricsCalculator:
    """Calculate metrics from Jira data."""

    def __init__(self, data: pd.DataFrame):
        """Initialize calculator with data."""
        self.data = data.copy()
        # Standardize column names
        self.data = self.data.rename(
            columns={"Story_Points": "Story Points", "Issue_Key": "Issue Key"}
        )

    def get_basic_metrics(self) -> Dict[str, Any]:
        """Calculate basic metrics."""
        story_points_col = (
            "Story Points" if "Story Points" in self.data.columns else "Story_Points"
        )
        completed = len(self.data[self.data["Status"] == "Done"])
        total = len(self.data)
        return {
            "total_stories": total,
            "completed_stories": completed,
            "total_points": self.data[story_points_col].fillna(0).sum(),
            "completion_rate": completed / total if total > 0 else 0,
        }

    def get_sprint_velocity(self) -> pd.Series:
        """Calculate sprint velocity."""
        story_points_col = (
            "Story Points" if "Story Points" in self.data.columns else "Story_Points"
        )
        return (
            self.data[self.data["Status"] == "Done"]
            .groupby("Sprint")[story_points_col]
            .sum()
        )

    def get_sprint_metrics(self) -> Dict[str, Any]:
        """Get sprint metrics."""
        velocity = self.get_sprint_velocity()
        return {
            "average_velocity": velocity.mean() if not velocity.empty else 0,
            "completion_rate": self.get_basic_metrics()["completion_rate"],
        }
