import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from components.cards import section_title
from components.history import render_run_detail, run_catalog_from_runs, run_label, run_name
from components.metrics import render_metric_grid
from components.navbar import profile_panel, render_sidebar
from components.theme import apply_theme, configure_page, page_header
from utils.data import cached_runs
from utils.state import init_state


configure_page("Simulation History | AI Model Performance Simulator")
init_state()
apply_theme()
render_sidebar()
profile_panel()

page_header(
    "Simulation History",
    "Browse every saved robustness experiment.",
    "Open any historical run to revisit its metric curves, saved graph artifacts, reliability tables, degradation summaries, confusion matrices, and recommendation outputs.",
)

runs = cached_runs()
if not runs:
    st.info("No saved simulations yet. Run and save an experiment from the Model Simulator page.")
    st.stop()

datasets = sorted({run.get("dataset", "Unknown") for run in runs})
model_names = sorted(
    {
        model
        for run in runs
        for model in run.get("settings", {}).get("selected_models", [])
    }
)

render_metric_grid(
    [
        ("Saved Runs", str(len(runs)), "Historical experiments"),
        ("Datasets", str(len(datasets)), "Unique workloads"),
        ("Models Seen", str(len(model_names)), "Across all runs"),
        ("Latest Run", run_name(runs[-1]), runs[-1].get("timestamp", "")),
    ]
)

section_title("Filters")
filter_cols = st.columns([1, 1, 1, 1])
with filter_cols[0]:
    dataset_filter = st.selectbox("Dataset", ["All"] + datasets)
with filter_cols[1]:
    model_filter = st.selectbox("Model", ["All"] + model_names)
with filter_cols[2]:
    sort_order = st.selectbox("Sort", ["Newest first", "Oldest first"])
with filter_cols[3]:
    max_runs = st.number_input("Runs to show", min_value=1, max_value=len(runs), value=len(runs), step=1)

filtered_runs = runs
if dataset_filter != "All":
    filtered_runs = [run for run in filtered_runs if run.get("dataset") == dataset_filter]
if model_filter != "All":
    filtered_runs = [run for run in filtered_runs if model_filter in run.get("settings", {}).get("selected_models", [])]

filtered_runs = sorted(filtered_runs, key=lambda run: int(run.get("run_id", 0)), reverse=sort_order == "Newest first")
filtered_runs = filtered_runs[: int(max_runs)]

section_title("Run Catalog", "Use the expanders below to inspect the full saved result set for each run.")
if not filtered_runs:
    st.info("No runs match the current filters.")
    st.stop()

st.dataframe(run_catalog_from_runs(filtered_runs), use_container_width=True, hide_index=True)
open_all = st.toggle("Open all run details", value=False)

for index, run in enumerate(filtered_runs):
    with st.expander(run_label(run), expanded=open_all or index == 0):
        render_run_detail(run, key_prefix=f"history_{run_name(run)}", compact=False)
