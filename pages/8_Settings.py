import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json

import streamlit as st

from components.cards import section_title
from components.navbar import profile_panel, render_sidebar
from components.theme import THEME_MODES, apply_theme, configure_page, page_header
from utils.state import init_state, save_user_preferences


def persist_interface_preferences() -> None:
    save_user_preferences(
        ui_theme_mode=st.session_state.ui_theme_mode,
        notify_success=st.session_state.notify_success,
    )


configure_page("Settings | AI Model Performance Simulator")
init_state()
apply_theme()
render_sidebar()
profile_panel()

page_header(
    "Settings",
    "Tune the simulator workspace.",
    "Manage UI preferences, default model behavior, notification preferences, and export/import local configuration.",
)

section_title("Interface")
current_theme = st.session_state.ui_theme_mode if st.session_state.ui_theme_mode in THEME_MODES else "Neon dark"
st.selectbox(
    "Theme mode",
    THEME_MODES,
    index=THEME_MODES.index(current_theme),
    key="ui_theme_mode",
    on_change=persist_interface_preferences,
)
st.toggle("Show success notifications", key="notify_success", on_change=persist_interface_preferences)

section_title("Model Preferences")
default_models = st.multiselect(
    "Preferred default models",
    ["Random Forest", "Logistic Regression", "SVM", "Decision Tree", "KNN", "Gradient Boosting", "XGBoost"],
    default=(st.session_state.get("settings") or {}).get("selected_models", ["Random Forest", "Logistic Regression", "SVM"]),
)
threshold = st.slider("Default reliability threshold", 0.05, 0.99, float(st.session_state.get("suggested_threshold", 0.75)), step=0.05)

settings_payload = {
    "ui_theme_mode": st.session_state.ui_theme_mode,
    "notify_success": st.session_state.notify_success,
    "default_models": default_models,
    "default_reliability_threshold": threshold,
}

section_title("Export / Import")
st.download_button(
    "Export Settings JSON",
    json.dumps(settings_payload, indent=2),
    "ai_simulator_settings.json",
    "application/json",
)
uploaded = st.file_uploader("Import settings JSON", type=["json"])
if uploaded is not None:
    try:
        imported = json.load(uploaded)
        st.json(imported)
        st.success("Settings file parsed. Apply these values manually in this local session as needed.")
    except Exception as exc:
        st.error(f"Invalid settings JSON: {exc}")
