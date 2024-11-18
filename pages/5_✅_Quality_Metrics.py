import streamlit as st
import plotly.express as px
from src.utils.logger import logger
from src.utils.error_handler import ErrorHandler
from src.utils.data_processor import process_quality_data
from Home import load_data

def render_quality_metrics():
    try:
        st.title("Quality Metrics ✅")
        
        # Load and process data
        with ErrorHandler().handle_operation("data_loading"):
            df = load_data()
            if df is None:
                return
            
            quality_data = process_quality_data(df)
        
        # Bug Trends
        st.subheader("Bug Trends")
        fig_bugs = px.line(
            quality_data,
            x="Sprint",
            y=["New Bugs", "Resolved Bugs"],
            title="Bug Trend Analysis"
        )
        st.plotly_chart(fig_bugs, use_container_width=True)
        
        # Quality Metrics Dashboard
        st.subheader("Quality Overview")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Bug Resolution Rate",
                f"{quality_data['Resolution Rate'].mean():.1%}"
            )
        
        with col2:
            st.metric(
                "Average Resolution Time",
                f"{quality_data['Resolution Time'].mean():.1f} days"
            )
            
        with col3:
            st.metric(
                "First-Time-Right Rate",
                f"{quality_data['FTR Rate'].mean():.1%}"
            )
            
    except Exception as e:
        logger.error(f"Error in quality metrics: {str(e)}")
        st.error("An error occurred while rendering quality metrics.")

if __name__ == "__main__":
    render_quality_metrics() 