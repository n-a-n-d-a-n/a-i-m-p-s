import streamlit as st


def render_sidebar() -> None:
    st.sidebar.markdown(
        """
        <div style="padding:14px 4px 22px;">
            <div class="sidebar-title" style="font-size:1.05rem;font-weight:800;">AI Model Performance</div>
            <div class="sidebar-subtitle" style="font-size:.82rem;margin-top:4px;">Simulator Control Plane</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown('<span class="status-pill">Platform online</span>', unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.caption("Use the page list above to move between the dashboard, simulator, analytics, comparison, dataset, status, settings, and history workspaces.")


def profile_panel() -> None:
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div class="glass-card" style="padding:16px;border-radius:16px;">
            <div class="sidebar-title" style="font-weight:800;">Analyst Workspace</div>
            <div class="sidebar-subtitle" style="font-size:.82rem;margin-top:4px;">Local Streamlit session</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
