"""Epic tracking page."""

import streamlit as st
from streamlit.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

st.set_page_config(page_title="Epic Tracking", page_icon="🎯", layout="wide")


def main():
    """Display epic tracking metrics."""
    try:
        st.title("Epic Tracking")

        if "data" not in st.session_state or "calculator" not in st.session_state:
            st.error("Please load data from the Home page first")
            return

        data = st.session_state.data
        calculator = st.session_state.calculator

        # Check for Epic column
        epic_column = next(
            (col for col in data.columns if col.lower() in ["epic", "epic link"]), None
        )
        if not epic_column:
            st.error(
                "Epic data not found. Please ensure your data includes an Epic or Epic Link column."
            )
            return

        # Get epic metrics
        metrics = {
            "total_epics": len(data[epic_column].unique()),
            "avg_completion": calculator.get_basic_metrics()["completion_rate"],
        }

        # Display epic KPIs
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Epics", metrics["total_epics"])
        with col2:
            st.metric("Average Completion", f"{metrics['avg_completion']:.1%}")

        # Display epic charts
        st.plotly_chart(
            st.session_state.visualizer.create_epic_progress(epic_column),
            use_container_width=True,
        )
        st.plotly_chart(
            st.session_state.visualizer.create_epic_status(epic_column),
            use_container_width=True,
        )

    except Exception as e:
        error_msg = f"Error in epic tracking: {str(e)}"
        logger.error(error_msg)
        st.error(error_msg)


if __name__ == "__main__":
    main()
