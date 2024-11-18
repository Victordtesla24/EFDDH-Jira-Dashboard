import streamlit as st
from src.utils.data_processor import DataProcessor
from src.utils.error_handler import ErrorHandler
from src.utils.logger import setup_logger

def main():
    st.set_page_config(
        page_title="EFDDH Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    logger = setup_logger()
    
    try:
        # Load and process data
        data_processor = DataProcessor()
        df = data_processor.load_data()
        
        # Display main dashboard
        st.title("EFDDH Agile Coaching Metrics Dashboard")
        
        return df
        
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        st.error("Unable to load dashboard data. Please check the data file and try again.")
        return None

if __name__ == "__main__":
    main() 