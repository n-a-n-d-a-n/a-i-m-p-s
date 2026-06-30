import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from components.cards import glass_card, section_title
from components.navbar import profile_panel, render_sidebar
from components.theme import apply_theme, configure_page, is_light_theme, page_header
from utils.state import init_state


configure_page("About Project | AI Model Performance Simulator")
init_state()
apply_theme()
render_sidebar()
profile_panel()

page_header(
    "About The Platform",
    "A model reliability lab for deployment-minded ML teams.",
    "The project simulates how classical AI models degrade under realistic data distortions, then packages the outcome as dashboards, rankings, and reliability reports.",
)

section_title("Objectives")
cols = st.columns(3)
with cols[0]:
    glass_card("Stress Test", "Quantify how models respond to Gaussian noise, drift, imbalance, missing values, label noise, outliers, and feature corruption.")
with cols[1]:
    glass_card("Explain Reliability", "Convert metric curves into reliability horizons, degradation rates, and robust deployment recommendations.")
with cols[2]:
    glass_card("Compare Decisions", "Rank model candidates using accuracy, F1, stability, confidence, and composite robustness scoring.")

section_title("Architecture")
graph_fill = "#ffffff" if is_light_theme() else "#111827"
graph_font = "#111827" if is_light_theme() else "#f8fafc"
graph_edge = "#2563eb" if is_light_theme() else "#8b5cf6"
st.graphviz_chart(
    f"""
digraph {{
    graph [bgcolor="transparent", rankdir=LR]
    node [shape=box, style="rounded,filled", fillcolor="{graph_fill}", fontcolor="{graph_font}", color="#5ee7ff"]
    edge [color="{graph_edge}", fontcolor="{graph_font}"]
    UI [label="Streamlit Multipage UI"]
    Components [label="Reusable Components"]
    Service [label="Simulator Service"]
    Core [label="backend/core ML Engines"]
    Distortions [label="Distortions"]
    Metrics [label="Evaluation Metrics"]
    Reliability [label="Reliability + Recommendation"]
    Artifacts [label="Saved Run Artifacts"]
    UI -> Components -> Service -> Core
    Core -> Distortions
    Core -> Metrics
    Core -> Reliability -> Artifacts
}}
"""
)

section_title("Technologies Used")
st.write("Streamlit, Plotly, Matplotlib, Pandas, NumPy, scikit-learn, XGBoost, FastAPI backend modules, reusable Python components, and local run artifact logging.")

section_title("Future Scope")
st.write("Authentication, team workspaces, richer PDF reports, model registry integrations, real-time API monitors, experiment diffing, and cloud deployment pipelines.")

section_title("Team & Contact")
st.info("Built as an AI Model Performance Simulator project. Add team member names, emails, and deployment links here when ready.")
