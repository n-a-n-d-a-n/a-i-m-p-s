from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import BinaryIO

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

from backend.core.confusion_matrix_analysis import compute_confusion_matrices, plot_confusion_matrices
from backend.core.degradation_analysis import compute_degradation, plot_degradation
from backend.core.distortion_analysis import DISTORTION_NAMES, run_per_distortion_analysis
from backend.core.distortions import apply_distortion
from backend.core.evaluation import evaluate
from backend.core.model import ALL_MODELS, MODEL_COLORS, MODEL_MARKERS, load_dataset, train_models
from backend.core.recommendation_engine import build_recommendation
from backend.core.reliability_analysis import compute_reliability_horizons, plot_reliability_windows
from backend.core.run_logger import save_run


METRICS = ["accuracy", "precision", "recall", "f1", "roc_auc", "confidence"]
EMPTY_RESULT = {metric: 0 for metric in METRICS}


@dataclass
class DatasetBundle:
    X: np.ndarray
    y: np.ndarray
    name: str
    preview: pd.DataFrame | None = None
    profile: dict | None = None


def is_regression_target(values, threshold: float = 0.05) -> bool:
    vals = pd.Series(pd.to_numeric(pd.Series(values), errors="coerce"))
    if vals.isnull().all() or len(vals.dropna()) == 0:
        return False
    unique_ratio = len(vals.dropna().unique()) / len(vals.dropna())
    return unique_ratio > threshold and len(vals.dropna().unique()) > 20


@st.cache_data(show_spinner=False)
def load_builtin_bundle(dataset_name: str) -> DatasetBundle:
    X, y, ds_name = load_dataset(name=dataset_name)
    return DatasetBundle(
        X=X,
        y=y,
        name=ds_name,
        preview=pd.DataFrame(X).head(12),
        profile={"samples": len(y), "features": X.shape[1], "classes": len(np.unique(y))},
    )


def prepare_uploaded_csv(uploaded_file: BinaryIO, target_col: str | None = None) -> DatasetBundle:
    df = pd.read_csv(uploaded_file)
    df.dropna(axis=1, how="all", inplace=True)
    df.dropna(axis=0, how="all", inplace=True)

    if df.empty:
        raise ValueError("Uploaded CSV is empty after cleaning.")
    if len(df) < 20:
        raise ValueError(f"Dataset has only {len(df)} rows. Need at least 20 samples.")
    if len(df.columns) < 2:
        raise ValueError("Dataset needs at least 2 columns: one feature and one target.")

    target_col = target_col or df.columns[-1]
    if is_regression_target(df[target_col].values):
        raise ValueError(f"Column '{target_col}' looks continuous. Choose a categorical classification target.")

    feature_cols = [col for col in df.columns if col != target_col]
    feature_df = df[feature_cols].copy()
    non_numeric_cols = feature_df.select_dtypes(exclude=[np.number]).columns.tolist()
    numeric_cols = feature_df.select_dtypes(include=[np.number]).columns.tolist()
    id_like_cols = [col for col in numeric_cols if feature_df[col].nunique() == len(feature_df)]
    numeric_cols = [col for col in numeric_cols if col not in id_like_cols]

    encoded_cols = []
    for col in non_numeric_cols:
        if feature_df[col].dropna().nunique() <= 20:
            encoder = LabelEncoder()
            feature_df[col] = encoder.fit_transform(feature_df[col].astype(str))
            encoded_cols.append(col)

    all_feature_cols = numeric_cols + encoded_cols
    if not all_feature_cols:
        raise ValueError("No usable feature columns found after preprocessing.")

    feature_df = feature_df[all_feature_cols].copy()
    feature_df = feature_df.drop_duplicates().dropna()
    if len(feature_df) < 20:
        raise ValueError(f"Only {len(feature_df)} usable rows remain. Need at least 20.")

    X = feature_df.values.astype(float)
    y_raw = df.loc[feature_df.index, target_col].values
    mask = pd.isnull(y_raw)
    if mask.any():
        X = X[~mask]
        y_raw = y_raw[~mask]

    encoder = LabelEncoder()
    y = encoder.fit_transform(y_raw.astype(str))
    n_classes = len(np.unique(y))
    if n_classes < 2:
        raise ValueError("Target column has only one class. Need at least two.")
    if n_classes > 50:
        raise ValueError(f"Target column has {n_classes} classes and looks like an ID/regression target.")

    class_counts = Counter(y)
    profile = {
        "samples": len(y),
        "features": X.shape[1],
        "classes": n_classes,
        "target": target_col,
        "encoded_columns": encoded_cols,
        "dropped_id_columns": id_like_cols,
        "class_labels": list(encoder.classes_),
        "imbalance_ratio": max(class_counts.values()) / min(class_counts.values()),
    }
    return DatasetBundle(X=X, y=y, name=getattr(uploaded_file, "name", "uploaded.csv"), preview=df.head(20), profile=profile)


def run_simulation(
    dataset: DatasetBundle,
    selected_models: list[str],
    max_level: float,
    num_levels: int,
    test_size: float,
    scale_data: bool,
    random_seed: int,
    distortions_used: dict[str, bool],
) -> dict:
    if not selected_models:
        raise ValueError("Select at least one model.")

    distortion_levels = list(np.linspace(0, max_level, num_levels))
    X_scaled = dataset.X.copy()
    if scale_data:
        X_scaled = StandardScaler().fit_transform(X_scaled)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        dataset.y,
        test_size=test_size,
        random_state=int(random_seed),
        stratify=dataset.y,
    )
    trained_models = train_models(X_train, y_train, selected_models)

    all_results = {name: [] for name in selected_models}
    progress = st.progress(0)
    status = st.empty()

    for index, level in enumerate(distortion_levels):
        status.caption(f"Evaluating distortion level {level:.3f}")
        X_dist, y_dist = apply_distortion(
            X_test.copy(),
            y_test.copy(),
            noise_level=level if distortions_used.get("gaussian_noise") else 0.0,
            drift_level=level if distortions_used.get("covariate_drift") else 0.0,
            dist_shift_level=level if distortions_used.get("distribution_shift") else 0.0,
            imbalance_level=level if distortions_used.get("class_imbalance") else 0.0,
            missing_level=level if distortions_used.get("missing_values") else 0.0,
            label_noise_level=level if distortions_used.get("label_noise") else 0.0,
            outlier_level=level if distortions_used.get("outlier_injection") else 0.0,
            corruption_level=level if distortions_used.get("feature_corruption") else 0.0,
        )

        if len(X_dist) == 0 or len(np.unique(y_dist)) < 2:
            for name in selected_models:
                all_results[name].append(EMPTY_RESULT.copy())
        else:
            for name, model in trained_models.items():
                all_results[name].append(evaluate(model, X_dist, y_dist))
        progress.progress((index + 1) / len(distortion_levels))

    status.caption("Simulation complete")
    X_test_max_dist, y_test_max_dist = apply_distortion(
        X_test.copy(),
        y_test.copy(),
        noise_level=max_level if distortions_used.get("gaussian_noise") else 0.0,
        drift_level=max_level if distortions_used.get("covariate_drift") else 0.0,
        dist_shift_level=max_level if distortions_used.get("distribution_shift") else 0.0,
        imbalance_level=max_level if distortions_used.get("class_imbalance") else 0.0,
        missing_level=max_level if distortions_used.get("missing_values") else 0.0,
        label_noise_level=max_level if distortions_used.get("label_noise") else 0.0,
        outlier_level=max_level if distortions_used.get("outlier_injection") else 0.0,
        corruption_level=max_level if distortions_used.get("feature_corruption") else 0.0,
    )

    fig_main = build_matplotlib_performance_grid(dataset.name, selected_models, distortion_levels, all_results)
    analysis_results = run_per_distortion_analysis(trained_models, X_test, y_test, level=max_level)
    analysis_df = build_analysis_df(selected_models, analysis_results)
    rel_df = build_rel_df(selected_models, distortion_levels, all_results)
    best_baseline = max([all_results[name][0]["accuracy"] for name in selected_models] or [0.75])
    suggested = round(round(max(0.40, min(best_baseline * 0.80, 0.95)) / 0.05) * 0.05, 2)
    summary_df = compute_degradation(rel_df, metric="accuracy")
    horizons_df = compute_reliability_horizons(rel_df, metric="accuracy", threshold=suggested)
    fig_reliability = plot_reliability_windows(rel_df, horizons_df, MODEL_COLORS, metric="accuracy", threshold=suggested)
    cm_results = compute_confusion_matrices(
        trained_models=trained_models,
        X_train=None,
        y_train=None,
        X_test_clean=X_test,
        y_test=y_test,
        X_test_distorted=X_test_max_dist,
        y_test_distorted=y_test_max_dist,
    )
    fig_confusion = plot_confusion_matrices(cm_results, MODEL_COLORS)
    fig_degradation = plot_degradation(rel_df, summary_df, MODEL_COLORS, metric="accuracy")
    fig_recommendation, rec_df = build_recommendation(rel_df, MODEL_COLORS)

    result = {
        "rel_df": rel_df,
        "all_results": all_results,
        "distortion_levels": distortion_levels,
        "selected_models": selected_models,
        "dataset_name": dataset.name,
        "max_level": max_level,
        "best_baseline": best_baseline,
        "suggested_threshold": suggested,
        "fig_main": fig_main,
        "analysis_df": analysis_df,
        "analysis_results": analysis_results,
        "trained_models": trained_models,
        "X_test_clean": X_test,
        "X_test_max_dist": X_test_max_dist,
        "y_test": y_test,
        "y_test_max_dist": y_test_max_dist,
        "summary_df": summary_df,
        "horizons_df": horizons_df,
        "fig_reliability": fig_reliability,
        "fig_confusion": fig_confusion,
        "fig_degradation": fig_degradation,
        "fig_recommendation": fig_recommendation,
        "rec_df": rec_df,
        "settings": {
            "max_distortion_level": max_level,
            "num_levels": num_levels,
            "test_size": test_size,
            "scale_data": scale_data,
            "random_seed": int(random_seed),
            "selected_models": selected_models,
        },
        "distortions_used": distortions_used,
    }
    persist_result(result)
    return result


def persist_result(result: dict) -> None:
    st.session_state.sim_done = True
    st.session_state.rel_df = result["rel_df"]
    st.session_state.all_results = result["all_results"]
    st.session_state.distortion_levels = result["distortion_levels"]
    st.session_state.selected_models_snap = result["selected_models"]
    st.session_state.ds_name_snap = result["dataset_name"]
    st.session_state.max_level_snap = result["max_level"]
    st.session_state.best_baseline = result["best_baseline"]
    st.session_state.suggested_threshold = result["suggested_threshold"]
    st.session_state.fig_main = result["fig_main"]
    st.session_state.analysis_df = result["analysis_df"]
    st.session_state.analysis_results = result["analysis_results"]
    st.session_state.trained_models = result["trained_models"]
    st.session_state.X_test_clean = result["X_test_clean"]
    st.session_state.X_test_max_dist = result["X_test_max_dist"]
    st.session_state.y_test = result["y_test"]
    st.session_state.y_test_max_dist = result["y_test_max_dist"]
    st.session_state.summary_df = result["summary_df"]
    st.session_state.horizons_df = result["horizons_df"]
    st.session_state.fig_reliability = result["fig_reliability"]
    st.session_state.fig_confusion = result["fig_confusion"]
    st.session_state.fig_degradation = result["fig_degradation"]
    st.session_state.fig_recommendation = result["fig_recommendation"]
    st.session_state.rec_df = result["rec_df"]
    st.session_state.settings = result["settings"]
    st.session_state.distortions_used = result["distortions_used"]
    st.session_state.reliability_threshold = result["suggested_threshold"]
    st.session_state.reliability_metric = "accuracy"
    st.session_state.rf_res = result["all_results"].get("Random Forest", [EMPTY_RESULT] * len(result["distortion_levels"]))
    st.session_state.lr_res = result["all_results"].get("Logistic Regression", [EMPTY_RESULT] * len(result["distortion_levels"]))
    st.session_state.svm_res = result["all_results"].get("SVM", [EMPTY_RESULT] * len(result["distortion_levels"]))
    st.session_state.run_saved = False


def build_matplotlib_performance_grid(dataset_name, selected_models, distortion_levels, all_results):
    titles = ["Accuracy", "Precision (macro)", "Recall (macro)", "F1 Score (macro)", "ROC-AUC Score", "Model Confidence"]
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    fig.suptitle(f"Model Performance Under Increasing Distortion\nDataset: {dataset_name}", fontsize=13, fontweight="bold")
    for ax, metric, title in zip(axes.flat, METRICS, titles):
        for name in selected_models:
            ax.plot(
                distortion_levels,
                [r[metric] for r in all_results[name]],
                marker=MODEL_MARKERS.get(name, "o"),
                label=name,
                color=MODEL_COLORS.get(name, "gray"),
            )
        ax.set_title(title)
        ax.set_xlabel("Distortion Level")
        ax.set_ylabel(metric.replace("_", " ").capitalize())
        ax.set_ylim(0, 1.05)
        ax.legend(fontsize=7)
        ax.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    return fig


def build_analysis_df(selected_models, analysis_results) -> pd.DataFrame:
    rows = []
    for d_name in DISTORTION_NAMES:
        row = {"Distortion": d_name}
        for name in selected_models:
            short = "".join(word[0] for word in name.split())
            row[f"{short} Acc"] = round(analysis_results[d_name][name].get("accuracy", 0), 3)
            row[f"{short} F1"] = round(analysis_results[d_name][name].get("f1", 0), 3)
            row[f"{short} AUC"] = round(analysis_results[d_name][name].get("roc_auc", 0), 3)
        rows.append(row)
    return pd.DataFrame(rows)


def build_rel_df(selected_models, distortion_levels, all_results) -> pd.DataFrame:
    rows = []
    for name in selected_models:
        for index, level in enumerate(distortion_levels):
            rows.append({"model_name": name, "distortion_level": level, **all_results[name][index]})
    return pd.DataFrame(rows)


def compact_results_table() -> pd.DataFrame:
    if st.session_state.get("all_results") is None:
        return pd.DataFrame()
    rows = []
    selected_models = st.session_state.selected_models_snap or []
    for index, level in enumerate(st.session_state.distortion_levels or []):
        row = {"Level": round(level, 3)}
        for name in selected_models:
            short = "".join(word[0] for word in name.split())
            result = st.session_state.all_results[name][index]
            row[f"{short} Acc"] = round(result["accuracy"], 3)
            row[f"{short} F1"] = round(result["f1"], 3)
            row[f"{short} AUC"] = round(result["roc_auc"], 3)
            row[f"{short} Conf"] = round(result["confidence"], 3)
        rows.append(row)
    return pd.DataFrame(rows)


def save_active_run() -> tuple[int, str] | None:
    if not st.session_state.get("sim_done"):
        return None
    if st.session_state.get("run_saved") and st.session_state.get("last_run_id"):
        return st.session_state.last_run_id, st.session_state.last_run_dir

    run_id, run_dir = save_run(
        st.session_state.ds_name_snap,
        st.session_state.settings,
        st.session_state.distortions_used,
        st.session_state.distortion_levels,
        st.session_state.rf_res,
        st.session_state.lr_res,
        st.session_state.svm_res,
        st.session_state.fig_main,
        fig_analysis=st.session_state.fig_analysis,
        analysis_df=st.session_state.analysis_df,
        fig_reliability=st.session_state.fig_reliability,
        horizons_df=st.session_state.horizons_df,
        reliability_threshold=st.session_state.reliability_threshold,
        reliability_metric=st.session_state.reliability_metric,
        fig_confusion=st.session_state.fig_confusion,
        fig_degradation=st.session_state.fig_degradation,
        summary_df=st.session_state.summary_df,
        fig_recommendation=st.session_state.fig_recommendation,
        rec_df=st.session_state.rec_df,
        model_results=st.session_state.all_results,
    )
    st.session_state.run_saved = True
    st.session_state.last_run_id = run_id
    st.session_state.last_run_dir = str(run_dir)
    try:
        from utils.data import cached_runs

        cached_runs.clear()
    except Exception:
        pass
    return run_id, str(run_dir)
