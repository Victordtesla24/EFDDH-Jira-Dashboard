import logging
from datetime import datetime

import pandas as pd

logger = logging.getLogger(__name__)


class MetricsCalculator:
    def __init__(self, df):
        self.df = df
        # Add color scheme for consistency
        self.color_scheme = {
            "High": "#ff4d4d",  # Red for high priority
            "Medium": "#ffa64d",  # Orange for medium
            "Low": "#4dff4d",  # Green for low
            "Done": "#2ecc71",  # Green for done
            "In Progress": "#3498db",  # Blue for in progress
            "To Do": "#95a5a6",  # Gray for todo
            "Blocked": "#e74c3c",  # Red for blocked
        }

        # Enhanced metric calculations for better tooltips
        if "Story Points" in self.df.columns:
            self.df["Story Points"] = pd.to_numeric(
                self.df["Story Points"], errors="coerce"
            )
        else:
            self.df["Story Points"] = 0

        # Add percentage calculations
        self.df["Progress"] = self.df.apply(
            lambda x: (
                100
                if x["Status"] in ["Done", "Closed"]
                else 50 if x["Status"] == "In Progress" else 0
            ),
            axis=1,
        )

        # Ensure date columns are datetime
        date_columns = ["Created", "Updated"]
        for col in date_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors="coerce")

        self.metric_explanations = {
            "story_points": "Total effort estimation for the story",
            "completion_rate": "Percentage of completed stories in the project",
            "sprint_velocity": "Average story points completed per sprint",
            "epic_progress": "Completion percentage of epic based on story points",
            "cycle_time": "Average days to complete a story",
            "defect_rate": "Percentage of issues marked as bugs",
        }

    def get_total_stories(self):
        try:
            return len(self.df)
        except Exception as e:
            logger.error(f"Error calculating total stories: {str(e)}")
            raise

    def get_avg_story_points(self):
        try:
            return self.df["Story Points"].mean()
        except Exception as e:
            logger.error(f"Error calculating average story points: {str(e)}")
            raise

    def get_completion_rate(self):
        try:
            completed = self.df[self.df["Status"].isin(["Done", "Closed"])].shape[0]
            total = len(self.df)
            return completed / total if total > 0 else 0
        except Exception as e:
            logger.error(f"Error calculating completion rate: {str(e)}")
            raise

    def get_sprint_velocity(self):
        try:
            return self.df.groupby("Sprint")["Story Points"].sum()
        except Exception as e:
            logger.error(f"Error calculating sprint velocity: {str(e)}")
            raise

    def get_assignee_workload(self):
        try:
            return self.df.groupby("Assignee")["Story Points"].sum()
        except Exception as e:
            logger.error(f"Error calculating assignee workload: {str(e)}")
            raise

    def get_epic_progress(self):
        try:
            epic_stats = (
                self.df.groupby("Epic")
                .agg(
                    {
                        "Story Points": "sum",
                        "Status": lambda x: (x == "Done").sum() / len(x) * 100,
                    }
                )
                .round(2)
            )
            epic_stats.columns = ["Total Points", "Completion Percentage"]
            return epic_stats
        except Exception as e:
            logger.error(f"Error calculating epic progress: {str(e)}")
            raise

    def get_sprint_burndown(self, sprint_name):
        try:
            sprint_data = self.df[self.df["Sprint"] == sprint_name].copy()
            sprint_data["Created"] = pd.to_datetime(sprint_data["Created"])
            daily_points = sprint_data.groupby("Created")["Story Points"].sum().cumsum()
            return daily_points
        except Exception as e:
            logger.error(f"Error calculating sprint burndown: {str(e)}")
            raise

    def get_cycle_time(self):
        try:
            completed_issues = self.df[
                self.df["Status"].isin(["Done", "Closed"])
            ].copy()
            completed_issues["Created"] = pd.to_datetime(completed_issues["Created"])
            completed_issues["Due Date"] = pd.to_datetime(completed_issues["Due Date"])
            completed_issues["Cycle Time"] = (
                completed_issues["Due Date"] - completed_issues["Created"]
            ).dt.days
            return completed_issues.groupby("Epic")["Cycle Time"].mean()
        except Exception as e:
            logger.error(f"Error calculating cycle time: {str(e)}")
            raise

    def get_priority_distribution(self):
        try:
            return self.df.groupby(["Priority", "Status"]).size().unstack(fill_value=0)
        except Exception as e:
            logger.error(f"Error calculating priority distribution: {str(e)}")
            raise

    def get_sprint_health(self, sprint_name):
        try:
            sprint_data = self.df[self.df["Sprint"] == sprint_name]
            total_points = sprint_data["Story Points"].sum()
            completed_points = sprint_data[
                sprint_data["Status"].isin(["Done", "Closed"])
            ]["Story Points"].sum()
            scope_changes = len(
                sprint_data[sprint_data["Created"] > sprint_data["Created"].min()]
            )

            return {
                "total_points": total_points,
                "completed_points": completed_points,
                "completion_percentage": (
                    (completed_points / total_points * 100) if total_points > 0 else 0
                ),
                "scope_changes": scope_changes,
            }
        except Exception as e:
            logger.error(f"Error calculating sprint health: {str(e)}")
            raise

    def get_metric_explanation(self, metric_name):
        """Get the explanation for a specific metric"""
        return self.metric_explanations.get(metric_name, "No explanation available")
