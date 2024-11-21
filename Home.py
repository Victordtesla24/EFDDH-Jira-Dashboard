"""Main Streamlit application."""

import logging

import pandas as pd
import streamlit as st
from streamlit.logger import get_logger

from src.metrics.metrics_calculator import MetricsCalculator
from src.utils.data_processor import DataProcessor
from src.visualizations.program_charts import Visualizer

# Initialize logger
logger = get_logger(__name__)


@st.cache_resource
def setup_logger():
    """Configure logger with cache to prevent duplicate handlers."""
    logger = get_logger(__name__)
    logger.handlers.clear()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def main() -> None:
    """Run the main Streamlit application."""
    try:
        # Setup logger
        logger = setup_logger()

        st.title("Jira Dashboard")

        # Initialize processor
        processor = DataProcessor()
        logger.info("DataProcessor initialized")

        # Add file uploader
        uploaded_file = st.file_uploader(
            "Upload Jira CSV file",
            type=["csv"],
            help="Upload a CSV file containing Jira data",
        )

        # Process uploaded file
        if uploaded_file is not None:
            try:
                # Read CSV file
                data = pd.read_csv(uploaded_file)

                # Standardize column names - Updated mapping
                data.columns = data.columns.str.strip()
                column_mappings = {
                    "Issue key": "Issue Key",
                    "Story points": "Story Points",  # Added lowercase variation
                    "Points": "Story Points",  # Added another common variation
                    "StoryPoints": "Story Points",  # Added camelCase variation
                    "story_points": "Story Points",  # Added snake_case variation
                    "Issue_type": "Issue Type",
                    "Epic_link": "Epic Link",
                }

                # Case-insensitive column mapping
                current_cols = data.columns.str.lower()
                for old_col, new_col in column_mappings.items():
                    if old_col.lower() in current_cols:
                        data = data.rename(
                            columns={
                                data.columns[current_cols == old_col.lower()][
                                    0
                                ]: new_col
                            }
                        )

                # Store in session state
                st.session_state.data = data

                # Initialize calculator and visualizer
                st.session_state.calculator = MetricsCalculator(data)
                st.session_state.visualizer = Visualizer(data)

                logger.info("Data loaded successfully")

            except Exception as e:
                error_msg = f"Error reading file: {str(e)}"
                logger.error(error_msg)
                st.error(error_msg)
                return

        # Display metrics and charts if data is available
        if "data" in st.session_state:
            try:
                # Validate required columns
                required_cols = ["Issue Key", "Story Points", "Status"]
                missing_cols = [
                    col
                    for col in required_cols
                    if col not in st.session_state.data.columns
                ]

                if missing_cols:
                    error_msg = f"Required columns missing: {', '.join(missing_cols)}"
                    logger.error(error_msg)
                    st.error(error_msg)
                    return

                # Calculate and display metrics
                metrics = st.session_state.calculator.get_basic_metrics()

                # Display metrics
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

                # New visualizations with different chart types
                st.subheader("Epic Distribution")
                try:
                    epic_col = next(
                        (
                            col
                            for col in st.session_state.data.columns
                            if col.lower() in ["epic", "epic link"]
                        ),
                        None,
                    )
                    if epic_col:
                        # Using treemap for epic distribution
                        st.plotly_chart(
                            st.session_state.visualizer.create_epic_treemap(epic_col),
                            use_container_width=True,
                        )
                    else:
                        st.warning("Epic data not found in the uploaded file")
                except Exception as e:
                    logger.error(f"Error creating epic distribution: {str(e)}")
                    st.error("Unable to display epic distribution")

                st.subheader("Sprint Health")
                try:
                    # Using radar chart for sprint health metrics
                    st.plotly_chart(
                        st.session_state.visualizer.create_sprint_health_radar(),
                        use_container_width=True,
                    )
                except Exception as e:
                    logger.error(f"Error creating sprint health metrics: {str(e)}")
                    st.error("Unable to display sprint health metrics")

            except Exception as e:
                error_msg = f"Error displaying metrics: {str(e)}"
                logger.error(error_msg)
                st.error(error_msg)
                return

        elif "data" not in st.session_state:
            st.info("Please upload a Jira CSV file")
            return

    except Exception as e:
        error_msg = f"Application error: {str(e)}"
        logger.error(error_msg)
        st.error(error_msg)


if __name__ == "__main__":
    main()
