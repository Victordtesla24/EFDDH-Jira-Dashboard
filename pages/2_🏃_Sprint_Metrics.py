"""Sprint metrics page."""

import streamlit as st
from streamlit.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

st.set_page_config(page_title="Sprint Metrics", page_icon="🏃", layout="wide")


def main():
    """Display sprint metrics."""
    try:
        st.title("Sprint Metrics")

        if "data" not in st.session_state or "calculator" not in st.session_state:
            st.error("Please load data from the Home page first")
            return

        # Get sprint metrics
        metrics = st.session_state.calculator.get_sprint_metrics()

        # Display sprint KPIs
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Velocity", f"{metrics['average_velocity']:.1f}")
        with col2:
            st.metric("Sprint Completion Rate", f"{metrics['completion_rate']:.1%}")

        # Display sprint charts
        st.plotly_chart(
            st.session_state.visualizer.create_sprint_velocity(),
            use_container_width=True,
        )
        st.plotly_chart(
            st.session_state.visualizer.create_sprint_burndown(),
            use_container_width=True,
        )
    except Exception as e:
        error_msg = f"Error processing sprint metrics: {str(e)}"
        logger.error(error_msg)
        st.error(error_msg)


if __name__ == "__main__":
    main()
