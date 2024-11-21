"""Program overview page."""

import pandas as pd
import streamlit as st

from src.metrics.metrics_calculator import MetricsCalculator
from src.visualizations.program_charts import Visualizer

st.set_page_config(page_title="Program Overview", page_icon="📊", layout="wide")


def main():
    """Display program overview."""
    st.title("Program Overview")

    if "data" not in st.session_state:
        st.error("Please load data from the Home page first")
        return

    calculator = MetricsCalculator(st.session_state.data)
    visualizer = Visualizer(st.session_state.data)

    # Display KPIs
    metrics = calculator.get_basic_metrics()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Stories", metrics["total_stories"])
    with col2:
        st.metric("Completed Stories", metrics["completed_stories"])
    with col3:
        st.metric("Total Points", f"{metrics['total_points']:.0f}")
    with col4:
        st.metric("Completion Rate", f"{metrics['completion_rate']:.1%}")

    # Display charts
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(visualizer.create_sprint_velocity(), use_container_width=True)
    with col2:
        st.plotly_chart(
            visualizer.create_status_distribution(), use_container_width=True
        )


if __name__ == "__main__":
    main()
