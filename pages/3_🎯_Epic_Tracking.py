import streamlit as st
import plotly.express as px
import pandas as pd
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
                st.warning("Please upload data first")
                return
            
            epic_data = process_epic_data(df)
            if epic_data.empty:
                st.warning("No epic data available")
                return

        # Create progress data
        progress_data = []
        for _, row in epic_data.iterrows():
            status_counts = row['Status']
            progress_data.append({
                'Epic': row['Epic'],
                'To Do': status_counts.get('To Do', 0),
                'In Progress': status_counts.get('In Progress', 0),
                'Done': status_counts.get('Done', 0)
            })
            
        progress_df = pd.DataFrame(progress_data)
        
        # Epic Progress Overview
        st.subheader("Epic Progress")
        
        if not progress_df.empty:
            fig = px.bar(
                progress_df,
                x='Epic',
                y=['To Do', 'In Progress', 'Done'],
                title="Epic Progress Overview",
                barmode="stack",
                color_discrete_map={
                    'To Do': '#95a5a6',
                    'In Progress': '#3498db',
                    'Done': '#2ecc71'
                }
            )
            
            fig.update_layout(
                xaxis_title="Epic",
                yaxis_title="Number of Issues",
                legend_title="Status",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Epic Details
            st.subheader("Epic Details")
            selected_epic = st.selectbox(
                "Select Epic",
                options=epic_data['Epic'].unique()
            )
            
            epic_details = epic_data[epic_data['Epic'] == selected_epic].iloc[0]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Completion Rate", 
                         f"{epic_details['Completion Rate']:.1%}")
            with col2:
                st.metric("Total Issues", 
                         int(epic_details['Total Issues']))
            with col3:
                st.metric("Done Issues", 
                         int(epic_details['Done Issues']))
                
    except Exception as e:
        logger.error(f"Error in epic tracking: {str(e)}")
        st.error("An error occurred while rendering epic tracking.")

if __name__ == "__main__":
    render_epic_tracking() 