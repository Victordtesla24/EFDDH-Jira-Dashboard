"""Team analysis page."""

import streamlit as st
from streamlit.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

st.set_page_config(page_title="Team Analysis", page_icon="👥", layout="wide")


def main():
    """Display team analysis metrics."""
    try:
        st.title("Team Analysis")

        if "data" not in st.session_state or "calculator" not in st.session_state:
            st.error("Please load data from the Home page first")
            return

        # Calculate team metrics
        data = st.session_state.data
        calculator = st.session_state.calculator
        basic_metrics = calculator.get_basic_metrics()

        metrics = {
            "active_members": len(data["Assignee"].unique()),
            "avg_points": basic_metrics["total_stories"]
            / len(data["Assignee"].unique()),
        }

        # Display team KPIs
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Active Team Members", metrics["active_members"])
        with col2:
            st.metric("Average Points per Member", f"{metrics['avg_points']:.1f}")

        # Display team charts
        st.plotly_chart(
            st.session_state.visualizer.create_team_workload(), use_container_width=True
        )
        st.plotly_chart(
            st.session_state.visualizer.create_team_velocity(), use_container_width=True
        )

    except Exception as e:
        error_msg = f"Error in team analysis: {str(e)}"
        logger.error(error_msg)
        st.error(error_msg)


if __name__ == "__main__":
    main()
