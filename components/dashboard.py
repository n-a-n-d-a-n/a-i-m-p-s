from __future__ import annotations

import streamlit as st

from components.cards import glass_card, section_title
from components.charts import gauge, metric_bar, performance_line
from components.history import render_recent_run_expanders
from components.metrics import render_metric_grid
from components.navbar import profile_panel, render_sidebar
from components.theme import apply_theme, configure_page, page_header
from utils.data import active_or_latest_rel_df, cached_runs, run_catalog_df
from utils.state import init_state


def render_dashboard(
    page_title: str | None = None,
    description: str = "A modern dashboard for simulating noise, drift, imbalance, missing values, label noise, outliers, and feature corruption across classical ML models.",
    key_prefix: str = "dashboard",
) -> None:
    configure_page(page_title)
    init_state()
    apply_theme()
    render_sidebar()
    profile_panel()

    page_header(
        "AI Reliability Command Center",
        "Stress-test model performance before production does.",
        description,
    )

    runs = cached_runs()
    rel_df = active_or_latest_rel_df()
    latest = runs[-1] if runs else None

    active_model_names = st.session_state.get("selected_models_snap")
    if not active_model_names and latest:
        active_model_names = latest.get("settings", {}).get("selected_models", [])

    best_score = 0
    if st.session_state.get("rec_df") is not None and not st.session_state.rec_df.empty:
        best_score = float(st.session_state.rec_df.iloc[0]["Composite Score"]) * 100
    elif latest and latest.get("recommendation"):
        try:
            best_score = float(latest["recommendation"][0]["Composite Score"]) * 100
        except Exception:
            best_score = 0

    render_metric_grid(
        [
            ("Saved Runs", str(len(runs)), "Historical simulations indexed"),
            ("Datasets Tested", str(len({run.get("dataset") for run in runs}) if runs else 0), "Built-in and CSV workloads"),
            ("Active Models", str(len(active_model_names or [])), "Ready for comparison"),
            ("Top Composite", f"{best_score:.1f}%", "Recommendation score"),
        ]
    )

    section_title("Performance Overview", "Live charts use the current session first, then fall back to the most recent saved run.")
    left, right = st.columns([1.55, 1])
    with left:
        st.plotly_chart(performance_line(rel_df, "accuracy"), use_container_width=True, key=f"{key_prefix}_overview_accuracy")
    with right:
        st.plotly_chart(gauge(best_score, "Recommended Model Confidence"), use_container_width=True, key=f"{key_prefix}_confidence_gauge")

    section_title("Quick Actions")
    cols = st.columns(4)
    for col, (title, body) in zip(
        cols,
        [
            ("Run Simulator", "Launch a new robustness test from the Model Simulator page."),
            ("Open Analytics", "Inspect degradation, reliability, and confusion matrices."),
            ("Compare Models", "Rank algorithms by accuracy, speed proxy, F1, and stability."),
            ("System Status", "Check runtime, package, memory, and platform health."),
        ],
    ):
        with col:
            glass_card(title, body, "Use sidebar navigation")

    section_title("Model Ranking")
    if st.session_state.get("summary_df") is not None:
        st.plotly_chart(metric_bar(st.session_state.summary_df), use_container_width=True, key=f"{key_prefix}_model_ranking")
    else:
        catalog = run_catalog_df()
        if catalog.empty:
            st.info("No saved simulations yet. Start with the Model Simulator page.")
        else:
            st.dataframe(catalog.tail(8), use_container_width=True, hide_index=True)

    section_title(
        "Recent Simulations",
        "Expanded run cards include the original saved visualizations, CSV-backed detail tables, and regenerated interactive charts where the JSON data is available.",
    )
    render_recent_run_expanders(runs, limit=len(runs), key_prefix=f"{key_prefix}_recent")
