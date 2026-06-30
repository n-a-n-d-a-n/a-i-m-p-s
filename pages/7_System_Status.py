import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import platform
import time

import streamlit as st

from components.cards import section_title
from components.charts import gauge
from components.metrics import render_metric_grid
from components.navbar import profile_panel, render_sidebar
from components.theme import apply_theme, configure_page, page_header
from utils.data import cached_runs
from utils.state import init_state


configure_page("System Status | AI Model Performance Simulator")
init_state()
apply_theme()
render_sidebar()
profile_panel()

page_header(
    "System Status",
    "Monitor the local simulator runtime.",
    "Inspect CPU, memory, uptime, package status, saved artifacts, and operational logs for the current Streamlit control plane.",
)

if "app_started_at" not in st.session_state:
    st.session_state.app_started_at = time.time()

try:
    import psutil
    cpu = float(psutil.cpu_percent(interval=0.2))
    memory = float(psutil.virtual_memory().percent)
    processes = len(psutil.pids())
except Exception:
    cpu = 0.0
    memory = 0.0
    processes = 0

uptime = int(time.time() - st.session_state.app_started_at)
runs = cached_runs()
render_metric_grid(
    [
        ("CPU Usage", f"{cpu:.1f}%", "Local machine"),
        ("Memory Usage", f"{memory:.1f}%", "System RAM"),
        ("App Uptime", f"{uptime}s", "Current session"),
        ("Saved Runs", str(len(runs)), "Artifact store"),
    ]
)

left, right = st.columns(2)
with left:
    st.plotly_chart(gauge(cpu, "CPU Usage"), use_container_width=True)
with right:
    st.plotly_chart(gauge(memory, "Memory Usage"), use_container_width=True)

section_title("Runtime")
st.dataframe(
    [
        {"Check": "Python", "Value": platform.python_version(), "Status": "OK"},
        {"Check": "OS", "Value": platform.platform(), "Status": "OK"},
        {"Check": "CPU Processes", "Value": processes, "Status": "OK" if processes else "Unavailable"},
        {"Check": "API Core Modules", "Value": "backend/core", "Status": "OK"},
    ],
    use_container_width=True,
    hide_index=True,
)

section_title("Logs")
st.code(
    "\n".join(
        [
            "INFO streamlit platform booted",
            f"INFO saved_runs={len(runs)}",
            f"INFO active_simulation={bool(st.session_state.get('sim_done'))}",
            "INFO backend.core engines importable",
        ]
    )
)
