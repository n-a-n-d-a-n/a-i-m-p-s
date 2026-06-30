import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import streamlit as st

from backend.core.model import ALL_MODELS
from components.cards import section_title
from components.charts import class_distribution, performance_line
from components.metrics import render_metric_grid
from components.navbar import profile_panel, render_sidebar
from components.theme import apply_theme, configure_page, page_header
from utils.simulator import compact_results_table, load_builtin_bundle, prepare_uploaded_csv, run_simulation, save_active_run
from utils.state import init_state


configure_page("Model Simulator | AI Model Performance Simulator")
init_state()
apply_theme()
render_sidebar()
profile_panel()

page_header(
    "Simulation Studio",
    "Build a distortion experiment in minutes.",
    "Select data, choose candidate models, apply real-world degradation patterns, and generate downloadable reliability artifacts.",
)

section_title("Dataset Input", "Use a built-in sklearn benchmark or upload a classification CSV.")
source_col, profile_col = st.columns([1, 1])
with source_col:
    dataset_source = st.radio("Dataset source", ["Built-in Dataset", "Upload CSV"], horizontal=True)
    dataset_bundle = None
    if dataset_source == "Built-in Dataset":
        dataset_name = st.selectbox("Dataset", ["iris", "wine", "breast_cancer"], index=1)
        dataset_bundle = load_builtin_bundle(dataset_name)
    else:
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"], help="Target defaults to the last column.")
        if uploaded_file is not None:
            preview_df = None
            try:
                import pandas as pd
                uploaded_file.seek(0)
                preview_df = pd.read_csv(uploaded_file, nrows=5)
                uploaded_file.seek(0)
                target_col = st.selectbox("Target column", preview_df.columns.tolist(), index=len(preview_df.columns) - 1)
                dataset_bundle = prepare_uploaded_csv(uploaded_file, target_col=target_col)
                st.session_state.uploaded_dataset_profile = dataset_bundle.profile
            except Exception as exc:
                st.error(str(exc))
        else:
            st.info("Upload a CSV to activate custom-data simulation.")

with profile_col:
    if dataset_bundle is not None:
        render_metric_grid(
            [
                ("Samples", f"{len(dataset_bundle.y):,}", "Rows ready"),
                ("Features", str(dataset_bundle.X.shape[1]), "Model inputs"),
                ("Classes", str(len(np.unique(dataset_bundle.y))), "Target labels"),
            ]
        )
        st.plotly_chart(class_distribution(dataset_bundle.y), use_container_width=True)

section_title("Experiment Configuration")
config_a, config_b, config_c = st.columns([1.1, 1, 1])
with config_a:
    selected_models = st.multiselect(
        "Models",
        list(ALL_MODELS.keys()),
        default=["Random Forest", "Logistic Regression", "SVM"],
    )
with config_b:
    max_level = st.slider("Max distortion level", 0.1, 1.0, 0.4, step=0.1)
    num_levels = st.slider("Number of levels", 3, 10, 5)
with config_c:
    test_size = st.slider("Test set size", 0.1, 0.4, 0.2, step=0.05)
    random_seed = st.number_input("Random seed", min_value=0, max_value=9999, value=42, step=1)
    scale_data = st.toggle("Scale features", value=True)

section_title("Distortion Stack")
dcols = st.columns(4)
distortions_used = {
    "gaussian_noise": dcols[0].checkbox("Gaussian Noise", value=True),
    "covariate_drift": dcols[1].checkbox("Covariate Drift", value=True),
    "distribution_shift": dcols[2].checkbox("Distribution Shift", value=True),
    "class_imbalance": dcols[3].checkbox("Class Imbalance", value=True),
    "missing_values": dcols[0].checkbox("Missing Values", value=False),
    "label_noise": dcols[1].checkbox("Label Noise", value=False),
    "outlier_injection": dcols[2].checkbox("Outlier Injection", value=False),
    "feature_corruption": dcols[3].checkbox("Feature Corruption", value=False),
}

run_col, save_col = st.columns([1, 1])
with run_col:
    run_clicked = st.button("Run Simulation", type="primary", use_container_width=True, disabled=dataset_bundle is None)
with save_col:
    save_clicked = st.button("Save Active Run", use_container_width=True, disabled=not st.session_state.get("sim_done"))

if run_clicked and dataset_bundle is not None:
    try:
        with st.spinner("Training models and evaluating distortion levels..."):
            run_simulation(
                dataset=dataset_bundle,
                selected_models=selected_models,
                max_level=max_level,
                num_levels=num_levels,
                test_size=test_size,
                scale_data=scale_data,
                random_seed=int(random_seed),
                distortions_used=distortions_used,
            )
            saved = save_active_run()
        if saved:
            st.success(f"Simulation complete and saved as run #{saved[0]:03d}. Analytics, comparison, and report artifacts are ready.")
        else:
            st.success("Simulation complete. Analytics, comparison, and report artifacts are ready.")
    except Exception as exc:
        st.error(f"Simulation failed: {exc}")

if save_clicked:
    saved = save_active_run()
    if saved:
        st.success(f"Saved run #{saved[0]:03d} to {saved[1]}")

if st.session_state.get("sim_done"):
    section_title("Simulation Results")
    st.plotly_chart(performance_line(st.session_state.rel_df, "accuracy"), use_container_width=True)
    st.dataframe(compact_results_table(), use_container_width=True, hide_index=True)
    csv = compact_results_table().to_csv(index=False).encode("utf-8")
    st.download_button("Download Results CSV", csv, file_name="simulation_results.csv", mime="text/csv")
