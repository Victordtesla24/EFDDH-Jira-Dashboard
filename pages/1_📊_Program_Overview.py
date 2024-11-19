"""Program Overview page."""

import streamlit as st
import plotly.express as px
from src.utils.data_processor import process_sprint_data
from src.utils.logger import logger
from src.visualizations.metrics_calculator import MetricsCalculator

def main():
    st.title("Program Overview")
    
    try:
        # Get the data and calculate metrics
        data = st.session_state.data
        metrics_calculator = MetricsCalculator(data)
        
        # Display data quality indicators
        st.sidebar.subheader("Data Quality Metrics")
        quality_metrics = metrics_calculator.accuracy_metrics
        
        # Completeness
        st.sidebar.markdown("**Data Completeness**")
        for metric, value in quality_metrics['completeness'].items():
            st.sidebar.progress(value, text=f"{metric}: {value:.1%}")
            
        # Consistency
        st.sidebar.markdown("**Data Consistency**")
        for metric, value in quality_metrics['consistency'].items():
            st.sidebar.progress(value, text=f"{metric}: {value:.1%}")
            
        # Data freshness
        if 'freshness' in quality_metrics:
            st.sidebar.metric("Data Freshness", f"{quality_metrics['freshness']} days old")
            
        # Process metrics
        metrics = process_sprint_data(data)
        
        if not metrics['velocity'] or not metrics['completion_rate']:
            st.warning("No sprint data available for visualization")
            return
            
        # Display metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sprint Velocity")
            sprints = list(metrics['velocity'].keys())
            velocity_values = list(metrics['velocity'].values())
            
            fig_velocity = px.line(
                x=sprints,
                y=velocity_values,
                labels={'x': 'Sprint', 'y': 'Story Points'},
                title="Sprint Velocity Trend"
            )
            fig_velocity.update_layout(
                height=400,
                margin=dict(t=50, l=25, r=25, b=25)
            )
            st.plotly_chart(fig_velocity, use_container_width=True)
            
        with col2:
            st.subheader("Completion Rate")
            completion_values = [v * 100 for v in metrics['completion_rate'].values()]
            
            fig_completion = px.bar(
                x=sprints,
                y=completion_values,
                labels={'x': 'Sprint', 'y': 'Completion Rate (%)'},
                title="Sprint Completion Rates"
            )
            fig_completion.update_layout(
                height=400,
                margin=dict(t=50, l=25, r=25, b=25),
                yaxis_range=[0, 100]
            )
            st.plotly_chart(fig_completion, use_container_width=True)
            
    except Exception as e:
        logger.error(f"Error in program overview: {str(e)}")
        st.error("Error processing data. Please check the data format.")

if __name__ == "__main__":
    main() 