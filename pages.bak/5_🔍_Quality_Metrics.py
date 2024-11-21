"""Quality metrics visualization page."""

import logging
from typing import Optional

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.metrics.metrics_calculator import MetricsCalculator
from src.visualizations.program_charts import Visualizer

logger = logging.getLogger(__name__)


def display_metrics_cards(metrics: dict, sprint_metrics: dict) -> None:
    """Display metrics in cards.

    Args:
        metrics: Basic metrics dictionary
        sprint_metrics: Sprint metrics dictionary
    """
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Bug Resolution Rate",
            f"{metrics['completion_rate']:.1%}",
            help="Percentage of bugs resolved vs total bugs",
        )
    with col2:
        st.metric(
            "Average Sprint Velocity",
            f"{sprint_metrics['average_velocity']:.1f}",
            help="Average story points completed per sprint",
        )
    with col3:
        st.metric(
            "First-Time-Right Rate",
            f"{metrics['completion_rate']:.1%}",
            help="Percentage of issues resolved without reopening",
        )


def display_charts(visualizer: Visualizer) -> None:
    """Display quality metrics charts.

    Args:
        visualizer: Chart visualization instance
    """
    # Display sprint velocity trend
    st.subheader("Sprint Velocity Trend")
    st.plotly_chart(visualizer.create_sprint_velocity(), use_container_width=True)

    # Display quality metrics
    st.subheader("Quality Metrics Overview")
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            visualizer.create_status_distribution(), use_container_width=True
        )
    with col2:
        st.plotly_chart(visualizer.create_epic_progress(), use_container_width=True)


def main() -> None:
    """Run the quality metrics dashboard."""
    try:
        st.title("Quality Metrics Dashboard")

        if "data" not in st.session_state:
            st.error("Please load data from the Home page first")
            return

        calculator = MetricsCalculator(st.session_state.data)
        visualizer = Visualizer(st.session_state.data)

        # Display metrics
        metrics = calculator.get_basic_metrics()
        sprint_metrics = calculator.get_sprint_metrics()

        display_metrics_cards(metrics, sprint_metrics)
        display_charts(visualizer)

    except Exception as e:
        logger.error("Error in quality metrics visualization: %s", str(e))
        st.error("An error occurred while displaying quality metrics.")


if __name__ == "__main__":
    main()
