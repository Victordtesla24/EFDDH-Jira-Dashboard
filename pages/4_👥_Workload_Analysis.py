import streamlit as st
import plotly.express as px
from src.utils.logger import logger
from src.utils.data_processor import process_workload_data
from Home import load_data

def render_workload_analysis():
    try:
        st.title("Workload Analysis 👥")
        
        # Load and process data
        with ErrorHandler().handle_operation("data_loading"):
            df = load_data()
            if df is None:
                return
            
            workload_data = process_workload_data(df)
        
        # Team Capacity Overview
        st.subheader("Team Capacity")
        fig_capacity = px.bar(
            workload_data,
            x="Team Member",
            y="Story Points",
            color="Status",
            title="Team Workload Distribution"
        )
        st.plotly_chart(fig_capacity, use_container_width=True)
        
        # Individual Analysis
        st.subheader("Individual Workload")
        col1, col2 = st.columns(2)
        
        with col1:
            team_member = st.selectbox(
                "Select Team Member",
                options=workload_data["Team Member"].unique()
            )
            
        member_data = workload_data[workload_data["Team Member"] == team_member]
        fig_member = px.pie(
            member_data,
            values="Story Points",
            names="Type",
            title=f"Work Distribution - {team_member}"
        )
        st.plotly_chart(fig_member, use_container_width=True)
        
    except Exception as e:
        logger.error(f"Error in workload analysis: {str(e)}")
        st.error("An error occurred while rendering workload analysis.")

if __name__ == "__main__":
    render_workload_analysis() 