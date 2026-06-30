from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

from backend.core.model import load_dataset
from backend.core.run_logger import load_all_runs


RESULTS_DIR = Path("results")


@st.cache_data(show_spinner=False)
def cached_builtin_dataset(name: str):
    X, y, ds_name = load_dataset(name=name)
    return X, y, ds_name


@st.cache_data(show_spinner=False, ttl=5)
def cached_runs() -> list[dict]:
    return load_all_runs()


def latest_run() -> dict | None:
    runs = cached_runs()
    return runs[-1] if runs else None


def run_catalog_df() -> pd.DataFrame:
    rows = []
    for run in cached_runs():
        settings = run.get("settings", {})
        rows.append(
            {
                "Run": f"run_{int(run.get('run_id', 0)):03d}",
                "Timestamp": run.get("timestamp", ""),
                "Dataset": run.get("dataset", ""),
                "Models": ", ".join(settings.get("selected_models", [])),
                "Max Distortion": settings.get("max_distortion_level", None),
                "Levels": len(run.get("levels", [])),
            }
        )
    return pd.DataFrame(rows)


def active_or_latest_rel_df() -> pd.DataFrame | None:
    if st.session_state.get("rel_df") is not None:
        return st.session_state.rel_df

    run = latest_run()
    if not run:
        return None

    levels = run.get("levels", [])
    model_map = {
        "random_forest": "Random Forest",
        "logistic_regression": "Logistic Regression",
        "svm": "SVM",
    }
    rows = []
    for key, model_name in model_map.items():
        for level, metrics in zip(levels, run.get("results", {}).get(key, [])):
            row = {"model_name": model_name, "distortion_level": level}
            row.update(metrics)
            rows.append(row)
    return pd.DataFrame(rows) if rows else None


def read_run_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def dataset_profile(name: str) -> dict:
    X, y, ds_name = cached_builtin_dataset(name)
    return {
        "name": ds_name,
        "samples": len(y),
        "features": X.shape[1],
        "classes": len(np.unique(y)),
        "X": X,
        "y": y,
    }
