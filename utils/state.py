from __future__ import annotations

import json
from pathlib import Path

import streamlit as st


PREFERENCES_PATH = Path(".streamlit/user_preferences.json")

DEFAULTS = {
    "sim_done": False,
    "rel_df": None,
    "all_results": None,
    "distortion_levels": None,
    "selected_models_snap": None,
    "ds_name_snap": None,
    "max_level_snap": None,
    "best_baseline": 0.75,
    "suggested_threshold": 0.75,
    "fig_main": None,
    "fig_analysis": None,
    "analysis_df": None,
    "analysis_results": None,
    "settings": None,
    "distortions_used": None,
    "rf_res": None,
    "lr_res": None,
    "svm_res": None,
    "run_saved": False,
    "last_run_id": None,
    "last_run_dir": None,
    "trained_models": None,
    "X_test_clean": None,
    "X_test_max_dist": None,
    "y_test": None,
    "y_test_max_dist": None,
    "fig_confusion": None,
    "fig_degradation": None,
    "summary_df": None,
    "fig_recommendation": None,
    "rec_df": None,
    "fig_reliability": None,
    "horizons_df": None,
    "reliability_threshold": None,
    "reliability_metric": None,
    "uploaded_dataset_profile": None,
    "ui_theme_mode": "Neon dark",
    "notify_success": True,
}


def load_user_preferences() -> dict:
    try:
        if PREFERENCES_PATH.exists():
            return json.loads(PREFERENCES_PATH.read_text())
    except Exception:
        return {}
    return {}


def save_user_preferences(**updates) -> None:
    preferences = load_user_preferences()
    preferences.update({key: value for key, value in updates.items() if value is not None})
    PREFERENCES_PATH.parent.mkdir(parents=True, exist_ok=True)
    PREFERENCES_PATH.write_text(json.dumps(preferences, indent=2))


def init_state() -> None:
    preferences = load_user_preferences()
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = preferences.get(key, value)


def has_active_simulation() -> bool:
    return bool(st.session_state.get("sim_done") and st.session_state.get("rel_df") is not None)
