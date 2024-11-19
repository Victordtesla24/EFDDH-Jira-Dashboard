"""Main Streamlit application."""
import streamlit as st
from src.utils.logger import logger
from src.utils.data_processor import DataProcessor
from src.visualizations.program_charts import Visualizer

def main() -> None:
    """Main application entry point."""
    try:
        st.set_page_config(
            page_title="Jira Dashboard",
            page_icon="📊",
            layout="wide"
        )
        
        logger.info("Starting Jira Dashboard application")
        
        # Rest of your Streamlit app code...
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        st.error("An error occurred. Please check the logs for details.")

if __name__ == "__main__":
    main() 