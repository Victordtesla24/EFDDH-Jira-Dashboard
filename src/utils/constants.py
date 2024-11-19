"""Shared constants and types for the dashboard."""
from typing import Final, TypeAlias, Dict, Any, Literal
from enum import Enum
import plotly.graph_objects as go
import pandas as pd

# Type Aliases
JiraDataFrame = pd.DataFrame
ChartFigure = go.Figure

# Status Types
StatusLiteral = Literal["To Do", "In Progress", "Done", "Blocked"]
PriorityLiteral = Literal["High", "Medium", "Low"]

class StatusType(str, Enum):
    """Valid status types for Jira issues."""
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"
    BLOCKED = "Blocked"

class PriorityType(str, Enum):
    """Valid priority levels for Jira issues."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

# Chart colors
COLOR_SCHEME: Final[Dict[str, str]] = {
    PriorityType.HIGH.value: "#ff4b4b",
    PriorityType.MEDIUM.value: "#ffb84d",
    PriorityType.LOW.value: "#36b37e"
}

# Date formats
DATE_FORMAT: Final[str] = "%Y-%m-%d"

# Data validation
REQUIRED_COLUMNS: Final[list[str]] = [
    "Issue_Key",
    "Story_Points",
    "Status",
    "Sprint",
    "Created",
    "Due_Date",
    "Priority",
    "Epic"
]

# Chart configuration
CHART_CONFIG: Final[Dict[str, Any]] = {
    "displayModeBar": True,
    "displaylogo": False,
    "modeBarButtonsToRemove": ["lasso2d", "select2d"]
} 