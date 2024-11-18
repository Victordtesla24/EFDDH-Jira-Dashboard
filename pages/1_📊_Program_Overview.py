import streamlit as st
from src.utils.logger import logger
from src.utils.error_handler import ErrorHandler
from src.utils.data_processor import load_data
from src.services.jira import JiraService
from src.visualizations import create_program_overview
from src.utils.logger import logger
from src.visualizations import create_program_charts
from typing import Optional, Dict, List

def render_program_overview() -> None:
    """Render the program overview dashboard with metrics and charts."""
    try:
        st.title("Program Overview 📊")
        
        with ErrorHandler().handle_operation("data_loading"):
            df = load_data()
            
        if df is not None:
            # Program metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Epics", len(df['Epic'].unique()))
            with col2:
                st.metric("Active Sprints", len(df['Sprint'].unique()))
            with col3:
                st.metric("Total Story Points", df['Story Points'].sum())
                
            # Program charts
            create_program_charts(df)
        else:
            st.error("Unable to load dashboard data. Please check the data file and try again.")
            
    except Exception as e:
        logger.error(f"Program Overview error: {str(e)}")
        st.error("An unexpected error occurred. Please check the logs for details.")

if __name__ == "__main__":
    render_program_overview() 