"""Quality metrics visualization page."""

import streamlit as st
from streamlit.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

st.set_page_config(page_title="Quality Metrics", page_icon="🔍", layout="wide")


def main() -> None:
    """Run the quality metrics dashboard."""
    try:
        st.title("Quality Metrics Dashboard")

        if "data" not in st.session_state or "calculator" not in st.session_state:
            st.error("Please load data from the Home page first")
            return

        # Calculate metrics
        metrics = st.session_state.calculator.get_basic_metrics()

        # Display metrics in 3 columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label="Total Stories",
                value=metrics["total_stories"],
                help="Total number of stories",
            )
        with col2:
            st.metric(
                label="Completed Stories",
                value=metrics["completed_stories"],
                help="Number of completed stories",
            )
        with col3:
            st.metric(
                label="Completion Rate",
                value=f"{metrics['completion_rate']:.1%}",
                help="Percentage of completed stories",
            )

        # Quality Metrics Charts
        st.subheader("Quality Trends")
        col1, col2 = st.columns(2)

        with col1:
            try:
                velocity_chart = st.session_state.visualizer.create_velocity_chart()
                st.plotly_chart(velocity_chart, use_container_width=True)
            except Exception as e:
                logger.error(f"Error creating velocity chart: {str(e)}")
                st.error("Unable to create velocity chart")

        with col2:
            try:
                # Check if Issue Type column exists
                if not any(
                    col.lower() in ["issue type", "issuetype", "type"]
                    for col in st.session_state.data.columns
                ):
                    st.warning("Issue Type column not found in data")
                else:
                    type_chart = (
                        st.session_state.visualizer.create_issue_type_distribution()
                    )
                    st.plotly_chart(type_chart, use_container_width=True)
            except Exception as e:
                logger.error(f"Error creating issue type chart: {str(e)}")
                st.error("Unable to create issue type distribution chart")

        # Additional Quality Insights
        st.subheader("Sprint Performance")
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(
                st.session_state.visualizer.create_sprint_burndown(),
                use_container_width=True,
            )
        with col2:
            st.plotly_chart(
                st.session_state.visualizer.create_defect_trend(),
                use_container_width=True,
            )

    except Exception as e:
        error_msg = f"Error in quality metrics visualization: {str(e)}"
        logger.error(error_msg)
        st.error(error_msg)


if __name__ == "__main__":
    main()
