"""Team analysis page."""

import streamlit as st

st.set_page_config(page_title="Team Analysis", page_icon="👥", layout="wide")


def main():
    """Display team analysis metrics."""
    st.title("Team Analysis")

    if "data" not in st.session_state:
        st.error("Please load data from the Home page first")
        return

    # Get team metrics
    metrics = st.session_state.calculator.get_team_metrics()

    # Display team KPIs
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Active Team Members", metrics["active_members"])
    with col2:
        st.metric("Average Points per Member", f"{metrics['avg_points']:.1f}")

    # Display team charts
    st.plotly_chart(
        st.session_state.visualizer.create_team_workload(), use_container_width=True
    )
    st.plotly_chart(
        st.session_state.visualizer.create_team_velocity(), use_container_width=True
    )


if __name__ == "__main__":
    main()
