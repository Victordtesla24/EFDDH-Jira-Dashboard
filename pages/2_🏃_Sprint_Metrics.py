import streamlit as st
import plotly.express as px
from src.utils.logger import logger
from src.utils.error_handler import ErrorHandler
from src.utils.data_processor import process_sprint_data
from Home import load_data
from typing import Union, Optional
from src.utils.custom_exceptions import DataProcessingError

def render_sprint_metrics() -> None:
    """Render sprint metrics dashboard."""
    try:
        st.title("Sprint Metrics 🏃")
        
        # Load and process data
        with ErrorHandler().handle_operation("data_loading"):
            df = load_data()
            if df is None:
                return
            
            sprint_data = process_sprint_data(df)
            
        # Sprint Velocity Chart
        st.subheader("Sprint Velocity")
        fig_velocity = px.line(
            sprint_data, 
            x="Sprint", 
            y="Story Points",
            title="Sprint Velocity Trend"
        )
        st.plotly_chart(fig_velocity, use_container_width=True)
        
        # Sprint Burndown
        st.subheader("Sprint Burndown")
        col1, col2 = st.columns(2)
        
        with col1:
            selected_sprint = st.selectbox(
                "Select Sprint",
                options=sprint_data["Sprint"].unique()
            )
            
        burndown_data = sprint_data[sprint_data["Sprint"] == selected_sprint]
        fig_burndown = px.line(
            burndown_data,
            x="Date",
            y=["Remaining Points", "Ideal Burndown"],
            title=f"Burndown Chart - {selected_sprint}"
        )
        st.plotly_chart(fig_burndown, use_container_width=True)
        
    except DataProcessingError as e:
        logger.error("Data processing error: %s", str(e))
    except Exception as e:
        logger.error("Unexpected error in sprint metrics: %s", str(e))

if __name__ == "__main__":
    render_sprint_metrics() 