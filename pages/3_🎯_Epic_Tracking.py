import streamlit as st
import plotly.express as px
from src.utils.logger import logger
from src.utils.error_handler import ErrorHandler
from src.utils.data_processor import process_epic_data
from Home import load_data

def render_epic_tracking():
    try:
        st.title("Epic Tracking 🎯")
        
        # Load and process data
        with ErrorHandler().handle_operation("data_loading"):
            df = load_data()
            if df is None:
                return
            
            epic_data = process_epic_data(df)
        
        # Epic Progress Overview
        st.subheader("Epic Progress")
        fig_progress = px.bar(
            epic_data,
            x="Epic",
            y=["Completed", "In Progress", "To Do"],
            title="Epic Progress Overview",
            barmode="stack"
        )
        st.plotly_chart(fig_progress, use_container_width=True)
        
        # Epic Details
        st.subheader("Epic Details")
        selected_epic = st.selectbox(
            "Select Epic",
            options=epic_data["Epic"].unique()
        )
        
        epic_details = epic_data[epic_data["Epic"] == selected_epic]
        st.metric(
            "Completion Rate",
            f"{epic_details['Completion Rate'].iloc[0]:.1%}"
        )
        
    except Exception as e:
        logger.error("Error in epic tracking: %s", str(e))
        st.error("An error occurred while rendering epic tracking.")

if __name__ == "__main__":
    render_epic_tracking() 