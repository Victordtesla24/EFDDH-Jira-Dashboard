from typing import Optional, Dict, Any
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from ..utils.logger import get_logger
from ..utils.data_processor import DataProcessor

logger = get_logger(__name__)


class Visualizer:
    """Class for creating program visualizations."""
    
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.processor = DataProcessor()
        self.color_scheme: Dict[str, str] = {
            "High": "#ff4b4b",
            "Medium": "#ffb84d",
            "Low": "#36b37e"
        }
        
    def create_chart(self, chart_type: str) -> Optional[go.Figure]:
        """Factory method for creating charts."""
        chart_methods = {
            'status': self.create_status_distribution,
            'velocity': self.create_velocity_chart,
            'epic': self.create_epic_progress_chart,
            'cycle': self.create_cycle_time_trend,
            'priority': self.create_priority_matrix,
            'workload': self.create_workload_chart,
            'bugs': self.create_bug_trend_chart
        }
        
        try:
            return chart_methods[chart_type]()
        except KeyError:
            logger.error(f"Invalid chart type: {chart_type}")
            return None
        except Exception as e:
            logger.error(f"Error creating {chart_type} chart: {str(e)}")
            return None
