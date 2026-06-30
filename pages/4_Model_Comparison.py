import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from backend.core.degradation_analysis import compute_degradation
from components.cards import ranking_cards, section_title
from components.charts import metric_bar, radar_from_recommendation
from components.navbar import profile_panel, render_sidebar
from components.theme import apply_theme, configure_page, page_header
from utils.data import active_or_latest_rel_df
from utils.state import init_state


configure_page("Model Comparison | AI Model Performance Simulator")
init_state()
apply_theme()
render_sidebar()
profile_panel()

page_header(
    "Model Comparison",
    "Rank candidates by performance and resilience.",
    "Compare multiple AI models across accuracy, precision, recall, F1-score, ROC-AUC, confidence, stability, and degradation.",
)

rel_df = active_or_latest_rel_df()
if rel_df is None or rel_df.empty:
    st.info("Run a simulation first to compare models.")
    st.stop()

summary = compute_degradation(rel_df, metric="accuracy")
section_title("Leaderboard")
ranking_cards(summary.to_dict("records"), "Model", "Robustness Score")
st.plotly_chart(metric_bar(summary), use_container_width=True)

section_title("Metric Comparison Table")
comparison = (
    rel_df.groupby("model_name")
    .agg(
        accuracy=("accuracy", "mean"),
        precision=("precision", "mean"),
        recall=("recall", "mean"),
        f1=("f1", "mean"),
        roc_auc=("roc_auc", "mean"),
        confidence=("confidence", "mean"),
    )
    .reset_index()
    .rename(columns={"model_name": "Model"})
)
comparison["Speed Proxy"] = 1 / (comparison.index + 1)
st.dataframe(comparison.style.format({col: "{:.3f}" for col in comparison.columns if col != "Model"}), use_container_width=True)

section_title("Composite Radar")
if st.session_state.get("rec_df") is not None:
    st.plotly_chart(radar_from_recommendation(st.session_state.rec_df), use_container_width=True)
else:
    st.info("Radar scores are available after an active simulator run.")
