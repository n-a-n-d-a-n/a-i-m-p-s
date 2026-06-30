import streamlit as st

from components.cards import metric_card


def render_metric_grid(metrics: list[tuple[str, str, str]], accents: list[str] | None = None) -> None:
    accents = accents or ["#5ee7ff", "#8b5cf6", "#22c55e", "#f59e0b"]
    cols = st.columns(len(metrics))
    for idx, (label, value, delta) in enumerate(metrics):
        with cols[idx]:
            metric_card(label, value, delta, accents[idx % len(accents)])

