from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from components.theme import is_light_theme

PALETTE = ["#5ee7ff", "#8b5cf6", "#22c55e", "#f59e0b", "#fb7185", "#38bdf8", "#a78bfa"]


def _plotly_template() -> str:
    return "plotly_white" if is_light_theme() else "plotly_dark"


def _chart_text_color() -> str:
    return "#475569" if is_light_theme() else "#9aa7bd"


def _chart_grid_color() -> str:
    return "rgba(51,65,85,.14)" if is_light_theme() else "rgba(148,163,184,.16)"


def _transparent_layout() -> dict:
    return {
        "template": _plotly_template(),
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "#102033" if is_light_theme() else "#f8fafc"},
        "xaxis": {"gridcolor": _chart_grid_color(), "zerolinecolor": _chart_grid_color()},
        "yaxis": {"gridcolor": _chart_grid_color(), "zerolinecolor": _chart_grid_color()},
    }


def empty_chart(message: str = "Run a simulation to populate this chart.") -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=message, x=0.5, y=0.5, showarrow=False, font=dict(size=16, color=_chart_text_color()))
    fig.update_layout(**_transparent_layout(), height=360)
    return fig


def performance_line(rel_df: pd.DataFrame, metric: str = "accuracy") -> go.Figure:
    if rel_df is None or rel_df.empty or metric not in rel_df.columns:
        return empty_chart()
    fig = px.line(
        rel_df,
        x="distortion_level",
        y=metric,
        color="model_name",
        markers=True,
        template=_plotly_template(),
        color_discrete_sequence=PALETTE,
    )
    fig.update_layout(
        **_transparent_layout(),
        height=420,
        margin=dict(l=18, r=18, t=42, b=18),
        title=f"{metric.replace('_', ' ').title()} Under Distortion",
        legend_title_text="Model",
        yaxis_range=[0, 1.05],
    )
    return fig


def metric_bar(summary_df: pd.DataFrame, x: str = "Model", y: str = "Robustness Score") -> go.Figure:
    if summary_df is None or summary_df.empty or x not in summary_df.columns or y not in summary_df.columns:
        return empty_chart()
    fig = px.bar(
        summary_df,
        x=x,
        y=y,
        color=x,
        template=_plotly_template(),
        color_discrete_sequence=PALETTE,
    )
    fig.update_layout(
        **_transparent_layout(),
        height=380,
        margin=dict(l=18, r=18, t=42, b=18),
        title=f"{y} Ranking",
        showlegend=False,
    )
    return fig


def radar_from_recommendation(rec_df: pd.DataFrame) -> go.Figure:
    if rec_df is None or rec_df.empty:
        return empty_chart("Recommendation scores will appear after a simulation.")

    fields = ["Robustness Score", "Peak Accuracy", "Stability Score", "Composite Score"]
    fig = go.Figure()
    for idx, row in rec_df.iterrows():
        values = []
        for field in fields:
            value = float(row[field])
            values.append(value / 100 if field == "Robustness Score" else value)
        fig.add_trace(
            go.Scatterpolar(
                r=values + values[:1],
                theta=fields + fields[:1],
                fill="toself",
                name=row["Model"],
                line=dict(color=PALETTE[idx % len(PALETTE)]),
            )
        )
    fig.update_layout(
        **_transparent_layout(),
        height=430,
        margin=dict(l=18, r=18, t=42, b=18),
        title="Model Scoring Radar",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 1], gridcolor=_chart_grid_color()),
            angularaxis=dict(gridcolor=_chart_grid_color()),
        ),
    )
    return fig


def class_distribution(labels: np.ndarray | list) -> go.Figure:
    series = pd.Series(labels).value_counts().sort_index()
    fig = px.pie(
        values=series.values,
        names=[f"Class {idx}" for idx in series.index],
        hole=0.58,
        template=_plotly_template(),
        color_discrete_sequence=PALETTE,
    )
    fig.update_layout(
        **_transparent_layout(),
        height=350,
        margin=dict(l=18, r=18, t=42, b=18),
        title="Class Distribution",
    )
    return fig


def gauge(value: float, title: str, suffix: str = "%") -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": suffix, "font": {"size": 34}},
            title={"text": title},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#5ee7ff"},
                "bgcolor": "rgba(15,23,42,0.04)" if is_light_theme() else "rgba(255,255,255,0.04)",
                "borderwidth": 1,
                "bordercolor": "rgba(51,65,85,.18)" if is_light_theme() else "rgba(148,163,184,.24)",
                "steps": [
                    {"range": [0, 55], "color": "rgba(251,113,133,.22)"},
                    {"range": [55, 80], "color": "rgba(245,158,11,.22)"},
                    {"range": [80, 100], "color": "rgba(34,197,94,.22)"},
                ],
            },
        )
    )
    fig.update_layout(
        **_transparent_layout(),
        height=300,
        margin=dict(l=18, r=18, t=42, b=18),
    )
    return fig
