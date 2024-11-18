import logging
from datetime import datetime

import pandas as pd
from plotly import graph_objects as go

from utils.error_handler import ErrorHandler
from utils.logger import logger

logger = logging.getLogger(__name__)


class Visualizer:
    def __init__(self, df):
        self.df = df
        self.color_scheme = {
            "High": "#ff4d4d",  # Red for high priority
            "Medium": "#ffa64d",  # Orange for medium
            "Low": "#4dff4d",  # Green for low
            "Done": "#2ecc71",  # Green for done
            "In Progress": "#3498db",  # Blue for in progress
            "To Do": "#95a5a6",  # Gray for todo
            "Blocked": "#e74c3c",  # Red for blocked
        }
        self.epic_colors = [
            "#1f77b4",  # Blue
            "#2ecc71",  # Green
            "#e74c3c",  # Red
            "#f39c12",  # Orange
            "#9b59b6",  # Purple
        ]
        self.chart_explanations = {
            "status_distribution": {
                "description": "Distribution of issues across different statuses"
            },
            "velocity_chart": {
                "description": "Story points completed per sprint with trend"
            },
            "burndown_chart": {
                "description": "Remaining work over time vs ideal progress"
            },
            "epic_progress": {"description": "Epic size and completion percentage"},
            "cycle_time": {"description": "Time taken to complete stories over time"},
            "priority_matrix": {
                "description": "Issue distribution across priority levels"
            },
        }

        # Log initialization
        logger.info(f"Visualizer initialized with DataFrame shape: {df.shape}")
        logger.info(f"DataFrame columns: {df.columns.tolist()}")

    def get_chart_explanation(self, chart_type):
        """Get the explanation for a specific chart type"""
        return self.chart_explanations.get(
            chart_type,
            {"description": "No specific explanation available for this chart type."},
        )

    def create_status_distribution(self):
        try:
            status_counts = self.df["Status"].value_counts()
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=status_counts.index,
                        values=status_counts.values,
                        hole=0.3,
                        marker=dict(colors=list(self.color_scheme.values())),
                    )
                ]
            )

            fig.update_layout(
                title="Issue Status Distribution",
                showlegend=True,
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                ),
            )
            return fig
        except Exception as e:
            logger.error(f"Error creating status distribution chart: {str(e)}")
            raise

    def create_velocity_chart(self):
        try:
            velocity_data = (
                self.df.groupby("Sprint")["Story Points"].sum().reset_index()
            )

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=velocity_data["Sprint"],
                    y=velocity_data["Story Points"],
                    name="Velocity",
                    marker_color="#3498DB",
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=velocity_data["Sprint"],
                    y=velocity_data["Story Points"]
                    .rolling(window=3, min_periods=1)
                    .mean(),
                    name="Trend (3-Sprint Average)",
                    line=dict(color="#E74C3C", dash="dash"),
                )
            )

            fig.update_layout(
                title="Sprint Velocity with Trend",
                xaxis_title="Sprint",
                yaxis_title="Story Points",
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                ),
            )
            return fig
        except Exception as e:
            logger.error(f"Error creating velocity chart: {str(e)}")
            raise

    def create_burndown_chart(self, sprint_name=None):
        try:
            df = (
                self.df
                if sprint_name is None
                else self.df[self.df["Sprint"] == sprint_name].copy()
            )
            df["Created"] = pd.to_datetime(df["Created"])

            daily_points = df.groupby("Created")["Story Points"].sum().cumsum()

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=daily_points.index,
                    y=daily_points.values,
                    mode="lines+markers",
                    name="Actual",
                    line=dict(color="#2ECC71"),
                )
            )

            if len(daily_points) > 0:
                ideal_line = pd.Series(
                    [daily_points.iloc[0], 0],
                    index=[daily_points.index[0], daily_points.index[-1]],
                )

                fig.add_trace(
                    go.Scatter(
                        x=ideal_line.index,
                        y=ideal_line.values,
                        mode="lines",
                        name="Ideal",
                        line=dict(dash="dash", color="#E74C3C"),
                    )
                )

            fig.update_layout(
                title="Burndown Chart" + (f" - {sprint_name}" if sprint_name else ""),
                xaxis_title="Date",
                yaxis_title="Remaining Story Points",
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                ),
            )

            return fig
        except Exception as e:
            logger.error(f"Error creating burndown chart: {str(e)}")
            raise

    def create_epic_progress_chart(self):
        try:
            # Group by Epic and calculate progress metrics
            epic_progress = (
                self.df.groupby("Epic")
                .agg(
                    {
                        "Story Points": "sum",
                        "Issue key": "count",
                        "Status": lambda x: (x == "Done").sum() / len(x) * 100,
                    }
                )
                .reset_index()
            )

            # Create progress bar chart
            fig = go.Figure()

            # Add bars for total points
            fig.add_trace(
                go.Bar(
                    name="Total Points",
                    x=epic_progress["Epic"],
                    y=epic_progress["Story Points"],
                    marker_color="lightgray",
                )
            )

            # Add bars for completed points
            fig.add_trace(
                go.Bar(
                    name="Completed",
                    x=epic_progress["Epic"],
                    y=epic_progress["Story Points"] * epic_progress["Status"] / 100,
                    marker_color=self.color_scheme["Done"],
                )
            )

            fig.update_layout(
                title="Epic Progress Overview",
                barmode="overlay",
                height=400,
                margin=dict(t=50, l=25, r=25, b=100),
                xaxis_tickangle=-45,
                hovermode="x unified",
            )

            return fig
        except Exception as e:
            logger.error(f"Error creating epic progress chart: {str(e)}")
            return None

    def create_cycle_time_trend(self):
        try:
            completed_issues = self.df[
                self.df["Status"].isin(["Done", "Closed"])
            ].copy()
            completed_issues["Created"] = pd.to_datetime(completed_issues["Created"])
            completed_issues["Due Date"] = pd.to_datetime(completed_issues["Due Date"])
            completed_issues["Cycle Time"] = (
                completed_issues["Due Date"] - completed_issues["Created"]
            ).dt.days

            cycle_time_trend = (
                completed_issues.groupby("Sprint")["Cycle Time"].mean().reset_index()
            )

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=cycle_time_trend["Sprint"],
                    y=cycle_time_trend["Cycle Time"],
                    mode="lines+markers",
                    name="Average Cycle Time",
                    line=dict(color="#3498DB"),
                )
            )

            fig.update_layout(
                title="Cycle Time Trend",
                xaxis_title="Sprint",
                yaxis_title="Average Cycle Time (Days)",
                showlegend=True,
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                ),
            )

            return fig
        except Exception as e:
            logger.error(f"Error creating cycle time trend chart: {str(e)}")
            raise

    def create_priority_matrix(self):
        try:
            priority_status = (
                self.df.groupby(["Priority", "Status"]).size().unstack(fill_value=0)
            )

            fig = go.Figure(
                data=go.Heatmap(
                    z=priority_status.values,
                    x=priority_status.columns,
                    y=priority_status.index,
                    colorscale="RdYlBu_r",
                )
            )

            fig.update_layout(
                title="Priority-Status Matrix",
                xaxis_title="Status",
                yaxis_title="Priority",
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                ),
            )

            return fig
        except Exception as e:
            logger.error(f"Error creating priority matrix: {str(e)}")
            raise

    def create_epic_status_chart(self):
        try:
            # Validate required columns
            required_columns = ["Epic", "Status", "Story Points"]
            if not ErrorHandler.check_data_requirements(self.df, required_columns):
                return None

            # Group data
            epic_data = (
                self.df.groupby(["Epic", "Status"])
                .agg({"Story Points": "sum", "Issue key": "count"})
                .reset_index()
            )

            # Create sunburst chart
            fig = go.Figure(
                go.Sunburst(
                    ids=[
                        f"{row['Epic']}-{row['Status']}"
                        for _, row in epic_data.iterrows()
                    ],
                    labels=[f"{row['Status']}" for _, row in epic_data.iterrows()],
                    parents=[row["Epic"] for _, row in epic_data.iterrows()],
                    values=epic_data["Story Points"],
                    branchvalues="total",
                    marker=dict(
                        colors=[
                            self.color_scheme.get(status, "#808080")
                            for status in epic_data["Status"]
                        ]
                    ),
                    hovertemplate="""
                    <b>%{parent}</b><br>
                    Status: %{label}<br>
                    Story Points: %{value}<br>
                    Count: %{customdata[0]}<br>
                    <extra></extra>
                """,
                    customdata=epic_data[["Issue key"]].values,
                )
            )

            fig.update_layout(
                title="Epic Status Distribution",
                height=400,
                margin=dict(t=50, l=25, r=25, b=25),
            )

            return fig
        except Exception as e:
            logger.error(f"Error creating epic status chart: {str(e)}")
            ErrorHandler.handle_error(f"Epic status chart creation failed: {str(e)}")
            return None

    def create_workload_chart(self):
        try:
            # Create workload metrics
            workload_data = (
                self.df.groupby(["Assignee", "Status"])
                .agg({"Story Points": "sum", "Issue key": "count"})
                .reset_index()
            )

            # Create heatmap
            fig = go.Figure(
                data=go.Heatmap(
                    z=workload_data.pivot(
                        index="Assignee", columns="Status", values="Story Points"
                    )
                    .fillna(0)
                    .values,
                    x=workload_data["Status"].unique(),
                    y=workload_data["Assignee"].unique(),
                    colorscale="RdYlBu_r",
                    hoverongaps=False,
                    hovertemplate="""
                    <b>%{y}</b><br>
                    Status: %{x}<br>
                    Story Points: %{z}<br>
                    <extra></extra>
                """,
                )
            )

            fig.update_layout(
                title="Team Workload Distribution",
                height=400,
                margin=dict(t=50, l=100, r=25, b=25),
            )

            return fig
        except Exception as e:
            logger.error(f"Error creating workload chart: {str(e)}")
            return None

    def create_priority_distribution(self):
        try:
            # Validate required columns
            required_columns = ["Priority", "Status", "Story Points"]
            if not ErrorHandler.check_data_requirements(self.df, required_columns):
                return None

            # Group data by Priority and Status
            priority_data = (
                self.df.groupby(["Priority", "Status"])
                .agg({"Story Points": "sum", "Issue key": "count"})
                .reset_index()
            )

            # Create treemap
            fig = go.Figure(
                go.Treemap(
                    ids=[
                        f"{row['Priority']}-{row['Status']}"
                        for _, row in priority_data.iterrows()
                    ],
                    labels=[f"{row['Status']}" for _, row in priority_data.iterrows()],
                    parents=[row["Priority"] for _, row in priority_data.iterrows()],
                    values=priority_data["Story Points"],
                    branchvalues="total",
                    marker=dict(
                        colors=[
                            self.color_scheme.get(status, "#808080")
                            for status in priority_data["Status"]
                        ]
                    ),
                    hovertemplate="""
                    <b>%{parent}</b><br>
                    Status: %{label}<br>
                    Story Points: %{value}<br>
                    Count: %{customdata[0]}<br>
                    <extra></extra>
                """,
                    customdata=priority_data[["Issue key"]].values,
                )
            )

            fig.update_layout(
                title="Priority Distribution by Status",
                height=400,
                margin=dict(t=50, l=25, r=25, b=25),
            )

            return fig
        except Exception as e:
            logger.error(f"Error creating priority distribution: {str(e)}")
            ErrorHandler.handle_error(
                f"Priority distribution creation failed: {str(e)}"
            )
            return None

    def create_issue_type_chart(self):
        try:
            # Validate required columns
            required_columns = ["Issue Type", "Status", "Story Points"]
            if not ErrorHandler.check_data_requirements(self.df, required_columns):
                return None

            # Group data
            type_data = (
                self.df.groupby(["Issue Type", "Status"])
                .agg({"Story Points": "sum", "Issue key": "count"})
                .reset_index()
            )

            # Create sunburst chart
            fig = go.Figure(
                go.Sunburst(
                    ids=[
                        f"{row['Issue Type']}-{row['Status']}"
                        for _, row in type_data.iterrows()
                    ],
                    labels=[f"{row['Status']}" for _, row in type_data.iterrows()],
                    parents=[row["Issue Type"] for _, row in type_data.iterrows()],
                    values=type_data["Story Points"],
                    branchvalues="total",
                    marker=dict(
                        colors=[
                            self.color_scheme.get(status, "#808080")
                            for status in type_data["Status"]
                        ]
                    ),
                    hovertemplate="""
                    <b>%{parent}</b><br>
                    Status: %{label}<br>
                    Story Points: %{value}<br>
                    Count: %{customdata[0]}<br>
                    <extra></extra>
                """,
                    customdata=type_data[["Issue key"]].values,
                )
            )

            fig.update_layout(
                title="Issue Type Distribution",
                height=400,
                margin=dict(t=50, l=25, r=25, b=25),
            )

            return fig
        except Exception as e:
            logger.error(f"Error creating issue type chart: {str(e)}")
            ErrorHandler.handle_error(f"Issue type chart creation failed: {str(e)}")
            return None

    def create_bug_trend_chart(self):
        try:
            # Filter bugs and group by date
            bug_data = self.df[self.df["Issue Type"] == "Bug"].copy()
            if bug_data.empty:
                logger.warning("No bug data found for trend chart")
                return None

            bug_data["Created"] = pd.to_datetime(bug_data["Created"])
            bug_trends = (
                bug_data.groupby([bug_data["Created"].dt.to_period("M"), "Priority"])
                .size()
                .unstack(fill_value=0)
            )

            # Create line chart
            fig = go.Figure()
            for priority in bug_trends.columns:
                fig.add_trace(
                    go.Scatter(
                        x=bug_trends.index.astype(str),
                        y=bug_trends[priority],
                        name=priority,
                        mode="lines+markers",
                        line=dict(color=self.color_scheme.get(priority, "#808080")),
                    )
                )

            fig.update_layout(
                title="Bug Trends by Priority",
                xaxis_title="Month",
                yaxis_title="Number of Bugs",
                height=400,
                margin=dict(t=50, l=25, r=25, b=25),
            )

            return fig
        except Exception as e:
            logger.error(f"Error creating bug trend chart: {str(e)}")
            ErrorHandler.handle_error(f"Bug trend chart creation failed: {str(e)}")
            return None
