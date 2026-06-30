from __future__ import annotations

import html
from typing import Iterable

import streamlit as st


def metric_card(label: str, value: str, delta: str = "", accent: str = "#5ee7ff") -> None:
    st.markdown(
        f"""
        <div class="metric-card" style="box-shadow: inset 0 1px 0 rgba(255,255,255,.08), var(--card-shadow), 0 0 34px {accent}1f;">
            <div class="metric-label">{html.escape(label)}</div>
            <div class="metric-value">{html.escape(str(value))}</div>
            <div class="metric-delta">{html.escape(str(delta))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def glass_card(title: str, body: str, footer: str = "") -> None:
    st.markdown(
        f"""
        <div class="glass-card">
            <h3 style="margin:0 0 8px;font-size:1.05rem;">{html.escape(title)}</h3>
            <p class="card-body" style="margin:0;line-height:1.55;">{body}</p>
            {f'<div class="card-footer">{html.escape(footer)}</div>' if footer else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title: str, caption: str | None = None) -> None:
    st.markdown(f'<div class="section-title">{html.escape(title)}</div>', unsafe_allow_html=True)
    if caption:
        st.markdown(f'<div class="subtle">{caption}</div>', unsafe_allow_html=True)


def ranking_cards(rows: Iterable[dict], label_key: str, score_key: str) -> None:
    rows = list(rows)
    if not rows:
        st.info("No ranking data available yet.")
        return

    cols = st.columns(min(len(rows), 4))
    for idx, row in enumerate(rows[:4]):
        with cols[idx % len(cols)]:
            metric_card(
                f"Rank {idx + 1}",
                str(row.get(label_key, "Model")),
                f"{score_key}: {row.get(score_key, 'n/a')}",
                accent=["#5ee7ff", "#8b5cf6", "#22c55e", "#f59e0b"][idx % 4],
            )
