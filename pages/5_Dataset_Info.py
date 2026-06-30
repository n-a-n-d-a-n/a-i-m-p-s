import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
import streamlit as st

from components.cards import section_title
from components.charts import class_distribution
from components.metrics import render_metric_grid
from components.navbar import profile_panel, render_sidebar
from components.theme import apply_theme, configure_page, page_header
from utils.data import dataset_profile
from utils.simulator import prepare_uploaded_csv
from utils.state import init_state


configure_page("Dataset Info | AI Model Performance Simulator")
init_state()
apply_theme()
render_sidebar()
profile_panel()

page_header(
    "Dataset Intelligence",
    "Profile data before stress testing models.",
    "Review sample previews, feature counts, class distribution, preprocessing behavior, and upload diagnostics.",
)

tab_builtin, tab_upload = st.tabs(["Built-in Datasets", "CSV Upload Inspector"])
with tab_builtin:
    dataset_name = st.selectbox("Dataset", ["iris", "wine", "breast_cancer"], index=0)
    profile = dataset_profile(dataset_name)
    render_metric_grid(
        [
            ("Samples", f"{profile['samples']:,}", "Benchmark rows"),
            ("Features", str(profile["features"]), "Numeric inputs"),
            ("Classes", str(profile["classes"]), "Classification labels"),
        ]
    )
    st.plotly_chart(class_distribution(profile["y"]), use_container_width=True)
    st.dataframe(pd.DataFrame(profile["X"]).head(20), use_container_width=True)

with tab_upload:
    upload = st.file_uploader("Upload a CSV for inspection", type=["csv"], key="dataset_info_upload")
    if upload is None:
        st.info("Upload a CSV to inspect preprocessing behavior.")
    else:
        preview = pd.read_csv(upload, nrows=8)
        upload.seek(0)
        target = st.selectbox("Target column", preview.columns.tolist(), index=len(preview.columns) - 1)
        try:
            bundle = prepare_uploaded_csv(upload, target)
            render_metric_grid(
                [
                    ("Usable Samples", f"{len(bundle.y):,}", "After cleaning"),
                    ("Features Used", str(bundle.X.shape[1]), "Numeric or encoded"),
                    ("Classes", str(bundle.profile['classes']), "Encoded target"),
                ]
            )
            st.plotly_chart(class_distribution(bundle.y), use_container_width=True)
            section_title("Preview")
            st.dataframe(bundle.preview, use_container_width=True)
            section_title("Preprocessing Info")
            st.json(bundle.profile)
        except Exception as exc:
            st.error(str(exc))
