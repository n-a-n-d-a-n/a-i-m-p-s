import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from backend.core.degradation_analysis import compute_degradation, get_robustness_tier
from backend.core.reliability_analysis import compute_reliability_horizons, get_reliability_verdict
from components.cards import section_title
from components.charts import metric_bar, performance_line
from components.navbar import profile_panel, render_sidebar
from components.theme import apply_theme, configure_page, page_header
from utils.data import active_or_latest_rel_df, latest_run
from utils.state import init_state


def existing_artifact(path_value):
    if not path_value:
        return None
    path = Path(str(path_value).replace("\\", "/"))
    return str(path) if path.exists() else None


configure_page("Results Analytics | AI Model Performance Simulator")
init_state()
apply_theme()
render_sidebar()
profile_panel()

page_header(
    "Results & Analytics",
    "Turn raw simulations into reliability decisions.",
    "Explore accuracy curves, degradation speed, reliability thresholds, confusion matrices, per-distortion weaknesses, and exportable reports.",
)

rel_df = active_or_latest_rel_df()
if rel_df is None or rel_df.empty:
    st.info("Run a simulation first to populate analytics.")
    st.stop()

metric = st.selectbox("Metric", ["accuracy", "f1", "precision", "recall", "roc_auc", "confidence"], index=0)
section_title("Metric Curves")
st.plotly_chart(performance_line(rel_df, metric), use_container_width=True)

section_title("Degradation Analysis")
summary_df = compute_degradation(rel_df, metric=metric if metric in ["accuracy", "f1", "precision", "recall"] else "accuracy")
st.plotly_chart(metric_bar(summary_df), use_container_width=True)
st.dataframe(summary_df, use_container_width=True, hide_index=True)
cols = st.columns(min(len(summary_df), 4))
for col, (_, row) in zip(cols, summary_df.iterrows()):
    col.metric(row["Model"], get_robustness_tier(row["Robustness Score"]), f"-{row['% Drop']:.1f}% drop", delta_color="inverse")

section_title("Reliability Horizon")
threshold = st.slider("Reliability threshold", 0.05, 0.99, float(st.session_state.get("suggested_threshold", 0.75)), step=0.05)
horizons_df = compute_reliability_horizons(rel_df, metric="accuracy", threshold=threshold)
st.dataframe(horizons_df, use_container_width=True, hide_index=True)
st.markdown(get_reliability_verdict(horizons_df, float(rel_df["distortion_level"].max())))
st.download_button("Download Reliability CSV", horizons_df.to_csv(index=False), "reliability_horizons.csv", "text/csv")

section_title("Advanced Artifacts")
tab1, tab2, tab3, tab4 = st.tabs(["Per-Distortion", "Confusion Matrix", "Recommendation", "Saved Run Images"])
with tab1:
    if st.session_state.get("analysis_df") is not None:
        st.dataframe(st.session_state.analysis_df, use_container_width=True, hide_index=True)
        st.download_button("Download Per-Distortion CSV", st.session_state.analysis_df.to_csv(index=False), "per_distortion_analysis.csv", "text/csv")
    else:
        st.info("Per-distortion table is available for the active session after running the simulator.")
with tab2:
    if st.session_state.get("fig_confusion") is not None:
        st.pyplot(st.session_state.fig_confusion, use_container_width=True)
    else:
        run = latest_run()
        path = existing_artifact(run.get("_confusion_png_path")) if run else None
        st.image(path, use_container_width=True) if path else st.info("No confusion matrix artifact found.")
with tab3:
    if st.session_state.get("rec_df") is not None:
        st.dataframe(st.session_state.rec_df, use_container_width=True, hide_index=True)
    else:
        st.info("Recommendation scores are available after a new active simulation.")
with tab4:
    run = latest_run()
    if not run:
        st.info("No saved images yet.")
    else:
        for label, key in [
            ("Main Simulation", "_png_path"),
            ("Degradation", "_degradation_png_path"),
            ("Reliability", "_reliability_png_path"),
            ("Recommendation", "_recommendation_png_path"),
        ]:
            path = existing_artifact(run.get(key))
            if path:
                st.markdown(f"**{label}**")
                st.image(path, use_container_width=True)
