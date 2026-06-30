from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from components.charts import metric_bar, performance_line, radar_from_recommendation
from components.metrics import render_metric_grid


RESULTS_DIR = Path("results")
METRIC_OPTIONS = ["accuracy", "f1", "precision", "recall", "roc_auc", "confidence"]

MODEL_RESULT_KEYS = {
    "Random Forest": "random_forest",
    "Logistic Regression": "logistic_regression",
    "SVM": "svm",
    "Decision Tree": "decision_tree",
    "KNN": "knn",
    "Gradient Boosting": "gradient_boosting",
    "XGBoost": "xgboost",
}

ARTIFACTS = [
    ("Performance Grid", "_png_path", "results.png"),
    ("Per-Distortion Analysis", "_analysis_png_path", "per_distortion.png"),
    ("Reliability Horizon", "_reliability_png_path", "reliability.png"),
    ("Degradation Analysis", "_degradation_png_path", "degradation_analysis.png"),
    ("Confusion Matrices", "_confusion_png_path", "confusion_matrices.png"),
    ("Recommendation Dashboard", "_recommendation_png_path", "recommendation_dashboard.png"),
]


def run_name(run: dict) -> str:
    return f"run_{int(run.get('run_id', 0)):03d}"


def run_label(run: dict) -> str:
    dataset = run.get("dataset", "Unknown dataset")
    timestamp = run.get("timestamp", "No timestamp")
    return f"{run_name(run)} - {dataset} - {timestamp}"


def _normalise_key(value: str) -> str:
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")


def _compact_text(value: object, max_chars: int = 28) -> str:
    text = str(value)
    return text if len(text) <= max_chars else f"{text[: max_chars - 3]}..."


def _artifact_path(run: dict, json_key: str, fallback_name: str | None = None) -> str | None:
    path_value = run.get(json_key)
    candidates = []
    if path_value:
        candidates.append(Path(str(path_value).replace("\\", "/")))
    if fallback_name:
        candidates.append(run_dir(run) / fallback_name)

    for path in candidates:
        if path.exists():
            return str(path)
    return None


def run_dir(run: dict) -> Path:
    for _, key, _ in ARTIFACTS:
        path_value = run.get(key)
        if path_value:
            path = Path(str(path_value).replace("\\", "/"))
            if path.parent.exists():
                return path.parent
    return RESULTS_DIR / run_name(run)


def _csv_table(run: dict, filename: str) -> pd.DataFrame:
    path = run_dir(run) / filename
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def recommendation_df(run: dict) -> pd.DataFrame:
    df = _csv_table(run, "model_recommendation.csv")
    if not df.empty:
        return df
    data = run.get("recommendation", [])
    return pd.DataFrame(data if isinstance(data, list) else [])


def degradation_df(run: dict) -> pd.DataFrame:
    df = _csv_table(run, "degradation_summary.csv")
    if not df.empty:
        return df
    data = run.get("degradation", [])
    return pd.DataFrame(data if isinstance(data, list) else [])


def reliability_df(run: dict) -> pd.DataFrame:
    df = _csv_table(run, "reliability_horizons.csv")
    if not df.empty:
        return df
    data = run.get("reliability", {}).get("horizons", [])
    return pd.DataFrame(data if isinstance(data, list) else [])


def per_distortion_df(run: dict) -> pd.DataFrame:
    return _csv_table(run, "per_distortion_analysis.csv")


def run_rel_df(run: dict) -> pd.DataFrame:
    levels = run.get("levels", [])
    results = run.get("results", {})
    selected_models = run.get("settings", {}).get("selected_models", [])

    if not selected_models:
        selected_models = [
            model_name
            for model_name, key in MODEL_RESULT_KEYS.items()
            if key in results and results.get(key)
        ]

    rows = []
    for model_name in selected_models:
        result_key = MODEL_RESULT_KEYS.get(model_name, _normalise_key(model_name))
        model_results = results.get(result_key) or results.get(model_name) or results.get(_normalise_key(model_name))
        if not model_results:
            continue
        for level, metrics in zip(levels, model_results):
            rows.append({"model_name": model_name, "distortion_level": level, **metrics})
    return pd.DataFrame(rows)


def run_catalog_from_runs(runs: list[dict]) -> pd.DataFrame:
    rows = []
    for run in runs:
        settings = run.get("settings", {})
        distortions = [name.replace("_", " ").title() for name, enabled in run.get("distortions_used", {}).items() if enabled]
        rows.append(
            {
                "Run": run_name(run),
                "Timestamp": run.get("timestamp", ""),
                "Dataset": run.get("dataset", ""),
                "Models": ", ".join(settings.get("selected_models", [])),
                "Distortions": ", ".join(distortions) if distortions else "None",
                "Max Distortion": settings.get("max_distortion_level", None),
                "Levels": len(run.get("levels", [])),
            }
        )
    return pd.DataFrame(rows)


def render_run_detail(run: dict, key_prefix: str, compact: bool = False) -> None:
    settings = run.get("settings", {})
    selected_models = settings.get("selected_models", [])
    distortions = [name.replace("_", " ").title() for name, enabled in run.get("distortions_used", {}).items() if enabled]
    rec_df = recommendation_df(run)
    deg_df = degradation_df(run)
    rel_horizon_df = reliability_df(run)
    distortion_df = per_distortion_df(run)
    rel_df = run_rel_df(run)

    top_model = "n/a"
    top_score = "n/a"
    if not rec_df.empty and {"Model", "Composite Score"}.issubset(rec_df.columns):
        top_model = str(rec_df.iloc[0]["Model"])
        try:
            top_score = f"{float(rec_df.iloc[0]['Composite Score']) * 100:.1f}%"
        except Exception:
            top_score = str(rec_df.iloc[0]["Composite Score"])

    render_metric_grid(
        [
            ("Dataset", _compact_text(run.get("dataset", "n/a")), "Workload"),
            ("Models", str(len(selected_models)), _compact_text(", ".join(selected_models[:3]) + ("..." if len(selected_models) > 3 else ""), 34)),
            ("Top Model", top_model, f"Composite {top_score}"),
            ("Distortions", str(len(distortions)), f"Max level {settings.get('max_distortion_level', 'n/a')}"),
        ]
    )

    meta_left, meta_right = st.columns([1.1, 1])
    with meta_left:
        st.caption("Simulation settings")
        settings_rows = [
            {"Setting": "Timestamp", "Value": run.get("timestamp", "n/a")},
            {"Setting": "Levels", "Value": len(run.get("levels", []))},
            {"Setting": "Test size", "Value": settings.get("test_size", "n/a")},
            {"Setting": "Scaled features", "Value": settings.get("scale_data", "n/a")},
            {"Setting": "Random seed", "Value": settings.get("random_seed", "n/a")},
        ]
        st.dataframe(pd.DataFrame(settings_rows), use_container_width=True, hide_index=True)
    with meta_right:
        st.caption("Enabled distortions")
        st.write(", ".join(distortions) if distortions else "No distortions recorded.")

    tabs = st.tabs(["Interactive Charts", "Result Tables", "Saved Visualizations", "Raw Catalog"])
    with tabs[0]:
        if rel_df.empty:
            st.info("Interactive metric curves are limited for older runs that only saved image artifacts.")
        else:
            metric = st.selectbox("Metric", METRIC_OPTIONS, key=f"{key_prefix}_metric")
            st.plotly_chart(
                performance_line(rel_df, metric),
                use_container_width=True,
                key=f"{key_prefix}_performance_{metric}",
            )

        chart_left, chart_right = st.columns([1, 1])
        with chart_left:
            if not deg_df.empty and {"Model", "Robustness Score"}.issubset(deg_df.columns):
                st.plotly_chart(
                    metric_bar(deg_df),
                    use_container_width=True,
                    key=f"{key_prefix}_degradation_bar",
                )
        with chart_right:
            if not rec_df.empty:
                st.plotly_chart(
                    radar_from_recommendation(rec_df),
                    use_container_width=True,
                    key=f"{key_prefix}_recommendation_radar",
                )

    with tabs[1]:
        table_tabs = st.tabs(["Recommendation", "Degradation", "Reliability", "Per-Distortion"])
        with table_tabs[0]:
            st.dataframe(rec_df, use_container_width=True, hide_index=True) if not rec_df.empty else st.info("No recommendation table found.")
        with table_tabs[1]:
            st.dataframe(deg_df, use_container_width=True, hide_index=True) if not deg_df.empty else st.info("No degradation table found.")
        with table_tabs[2]:
            st.dataframe(rel_horizon_df, use_container_width=True, hide_index=True) if not rel_horizon_df.empty else st.info("No reliability table found.")
        with table_tabs[3]:
            st.dataframe(distortion_df, use_container_width=True, hide_index=True) if not distortion_df.empty else st.info("No per-distortion table found.")

    with tabs[2]:
        image_paths = [(label, _artifact_path(run, key, fallback)) for label, key, fallback in ARTIFACTS]
        image_paths = [(label, path) for label, path in image_paths if path]
        if not image_paths:
            st.info("No saved image artifacts found for this run.")
        elif compact:
            preview_cols = st.columns(2)
            for index, (label, path) in enumerate(image_paths):
                with preview_cols[index % 2]:
                    st.markdown(f"**{label}**")
                    st.image(path, use_container_width=True)
        else:
            image_tabs = st.tabs([label for label, _ in image_paths])
            for tab, (label, path) in zip(image_tabs, image_paths):
                with tab:
                    st.markdown(f"**{label}**")
                    st.image(path, use_container_width=True)

    with tabs[3]:
        catalog_df = run_catalog_from_runs([run])
        st.dataframe(catalog_df, use_container_width=True, hide_index=True)
        if not rel_df.empty:
            st.dataframe(rel_df, use_container_width=True, hide_index=True)


def render_recent_run_expanders(runs: list[dict], limit: int = 5, key_prefix: str = "recent") -> None:
    if not runs:
        st.info("Run history is empty.")
        return

    recent_runs = list(reversed(runs[-limit:]))
    st.dataframe(run_catalog_from_runs(recent_runs), use_container_width=True, hide_index=True)
    for index, run in enumerate(recent_runs):
        with st.expander(run_label(run), expanded=index == 0):
            render_run_detail(run, key_prefix=f"{key_prefix}_{run_name(run)}", compact=True)
