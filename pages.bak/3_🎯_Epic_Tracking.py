"""Epic tracking page."""

import streamlit as st

st.set_page_config(page_title="Epic Tracking", page_icon="🎯", layout="wide")


def main():
    """Display epic tracking metrics."""
    st.title("Epic Tracking")

    if "data" not in st.session_state:
        st.error("Please load data from the Home page first")
        return

    # Get epic metrics
    metrics = st.session_state.calculator.get_epic_metrics()

    # Display epic KPIs
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Epics", metrics["total_epics"])
    with col2:
        st.metric("Average Completion", f"{metrics['avg_completion']:.1%}")

    # Display epic charts
    st.plotly_chart(
        st.session_state.visualizer.create_epic_progress(), use_container_width=True
    )
    st.plotly_chart(
        st.session_state.visualizer.create_epic_status(), use_container_width=True
    )


if __name__ == "__main__":
    main()
