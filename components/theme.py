import streamlit as st


APP_TITLE = "AI Model Performance Simulator"
PRIMARY = "#5ee7ff"
SECONDARY = "#8b5cf6"
ACCENT = "#22c55e"
WARNING = "#f59e0b"
DANGER = "#fb7185"
THEME_MODES = [
    "Neon dark",
    "Clean dark",
    "Midnight",
    "Slate dark",
    "High contrast dark",
    "Light",
    "Soft gray",
    "Warm light",
    "High contrast light",
    "Presentation",
]


def get_theme_mode() -> str:
    mode = st.session_state.get("ui_theme_mode", "Neon dark")
    return mode if mode in THEME_MODES else "Neon dark"


def is_light_theme() -> bool:
    return get_theme_mode() in {"Light", "Soft gray", "Warm light", "High contrast light", "Presentation"}


def _theme_tokens() -> dict[str, str]:
    mode = get_theme_mode()
    if mode == "Warm light":
        return {
            "app_bg": "linear-gradient(135deg, #fffaf2 0%, #f7efe4 48%, #f4f8fb 100%)",
            "sidebar_bg": "linear-gradient(180deg, rgba(255,251,244,0.98), rgba(247,239,228,0.96))",
            "panel": "rgba(255, 252, 247, 0.86)",
            "panel_strong": "rgba(255, 252, 247, 0.96)",
            "metric_bg": "linear-gradient(145deg, rgba(255,252,247,0.96), rgba(247,239,228,0.88)), radial-gradient(circle at top right, rgba(14,165,233,0.10), transparent 30%)",
            "hero_bg": "linear-gradient(135deg, rgba(255,252,247,0.95), rgba(247,239,228,0.88)), linear-gradient(90deg, rgba(14,165,233,0.10), rgba(245,158,11,0.10))",
            "quick_action_bg": "linear-gradient(145deg, rgba(255,252,247,.94), rgba(247,239,228,.86))",
            "tab_bg": "rgba(255,252,247,.82)",
            "border": "rgba(82, 63, 43, 0.16)",
            "text": "#1f2933",
            "muted": "#667085",
            "hero_title": "#111827",
            "hero_copy": "#4b5563",
            "metric_value": "#111827",
            "metric_delta": "#047857",
            "section_title": "#111827",
            "sidebar_text": "#1f2933",
            "sidebar_muted": "#667085",
            "shadow": "0 18px 52px rgba(82, 63, 43, 0.12)",
            "scan": "linear-gradient(115deg, transparent 0%, rgba(245,158,11,0.08) 42%, transparent 62%), repeating-linear-gradient(90deg, rgba(82,63,43,0.045) 0 1px, transparent 1px 80px)",
        }
    if mode == "Soft gray":
        return {
            "app_bg": "linear-gradient(135deg, #f8fafc 0%, #eef2f7 52%, #f5f7fb 100%)",
            "sidebar_bg": "linear-gradient(180deg, rgba(248,250,252,0.98), rgba(235,241,248,0.96))",
            "panel": "rgba(255, 255, 255, 0.84)",
            "panel_strong": "rgba(255, 255, 255, 0.96)",
            "metric_bg": "linear-gradient(145deg, rgba(255,255,255,0.96), rgba(238,242,247,0.88)), radial-gradient(circle at top right, rgba(34,197,94,0.10), transparent 30%)",
            "hero_bg": "linear-gradient(135deg, rgba(255,255,255,0.94), rgba(238,242,247,0.88)), linear-gradient(90deg, rgba(14,165,233,0.08), rgba(34,197,94,0.08))",
            "quick_action_bg": "linear-gradient(145deg, rgba(255,255,255,.92), rgba(238,242,247,.86))",
            "tab_bg": "rgba(255,255,255,.78)",
            "border": "rgba(51, 65, 85, 0.14)",
            "text": "#172033",
            "muted": "#5f6b7a",
            "hero_title": "#111827",
            "hero_copy": "#475569",
            "metric_value": "#111827",
            "metric_delta": "#047857",
            "section_title": "#111827",
            "sidebar_text": "#172033",
            "sidebar_muted": "#64748b",
            "shadow": "0 18px 48px rgba(15, 23, 42, 0.10)",
            "scan": "linear-gradient(115deg, transparent 0%, rgba(34,197,94,0.08) 42%, transparent 62%), repeating-linear-gradient(90deg, rgba(15,23,42,0.035) 0 1px, transparent 1px 80px)",
        }
    if mode == "High contrast light":
        return {
            "app_bg": "linear-gradient(135deg, #ffffff 0%, #f3f6fb 100%)",
            "sidebar_bg": "linear-gradient(180deg, #ffffff, #edf2f7)",
            "panel": "rgba(255, 255, 255, 0.96)",
            "panel_strong": "#ffffff",
            "metric_bg": "linear-gradient(145deg, #ffffff, #f3f6fb)",
            "hero_bg": "linear-gradient(135deg, #ffffff, #f3f6fb)",
            "quick_action_bg": "linear-gradient(145deg, #ffffff, #f3f6fb)",
            "tab_bg": "#ffffff",
            "border": "rgba(15, 23, 42, 0.28)",
            "text": "#05070d",
            "muted": "#334155",
            "hero_title": "#05070d",
            "hero_copy": "#1e293b",
            "metric_value": "#05070d",
            "metric_delta": "#065f46",
            "section_title": "#05070d",
            "sidebar_text": "#05070d",
            "sidebar_muted": "#334155",
            "shadow": "0 14px 36px rgba(15, 23, 42, 0.14)",
            "scan": "repeating-linear-gradient(90deg, rgba(15,23,42,0.05) 0 1px, transparent 1px 80px)",
        }
    if mode == "Light":
        return {
            "app_bg": "radial-gradient(circle at 18% 8%, rgba(14, 165, 233, 0.12), transparent 28%), radial-gradient(circle at 88% 10%, rgba(139, 92, 246, 0.10), transparent 32%), linear-gradient(135deg, #f8fbff 0%, #eef6ff 48%, #f9fafb 100%)",
            "sidebar_bg": "linear-gradient(180deg, rgba(255,255,255,0.98), rgba(240,247,255,0.96))",
            "panel": "rgba(255, 255, 255, 0.82)",
            "panel_strong": "rgba(255, 255, 255, 0.94)",
            "metric_bg": "linear-gradient(145deg, rgba(255,255,255,0.95), rgba(240,247,255,0.86)), radial-gradient(circle at top right, rgba(14,165,233,0.13), transparent 30%)",
            "hero_bg": "linear-gradient(135deg, rgba(255,255,255,0.92), rgba(232,244,255,0.86)), linear-gradient(90deg, rgba(14,165,233,0.12), rgba(124,58,237,0.10))",
            "quick_action_bg": "linear-gradient(145deg, rgba(255,255,255,.90), rgba(240,247,255,.82))",
            "tab_bg": "rgba(255,255,255,.74)",
            "border": "rgba(51, 65, 85, 0.16)",
            "text": "#102033",
            "muted": "#53657d",
            "hero_title": "#0f172a",
            "hero_copy": "#475569",
            "metric_value": "#0f172a",
            "metric_delta": "#047857",
            "section_title": "#0f172a",
            "sidebar_text": "#102033",
            "sidebar_muted": "#53657d",
            "shadow": "0 18px 52px rgba(15, 23, 42, 0.12)",
            "scan": "linear-gradient(115deg, transparent 0%, rgba(14,165,233,0.10) 42%, transparent 62%), repeating-linear-gradient(90deg, rgba(15,23,42,0.045) 0 1px, transparent 1px 80px)",
        }
    if mode == "Presentation":
        return {
            "app_bg": "linear-gradient(135deg, #ffffff 0%, #f6f8fb 54%, #eef5ff 100%)",
            "sidebar_bg": "linear-gradient(180deg, rgba(248,250,252,0.98), rgba(226,232,240,0.94))",
            "panel": "rgba(255, 255, 255, 0.88)",
            "panel_strong": "rgba(255, 255, 255, 0.96)",
            "metric_bg": "linear-gradient(145deg, rgba(255,255,255,0.98), rgba(244,248,252,0.90)), radial-gradient(circle at top right, rgba(94,231,255,0.16), transparent 30%)",
            "hero_bg": "linear-gradient(135deg, rgba(255,255,255,0.96), rgba(239,246,255,0.90)), linear-gradient(90deg, rgba(94,231,255,0.10), rgba(139,92,246,0.10))",
            "quick_action_bg": "linear-gradient(145deg, rgba(255,255,255,.94), rgba(244,248,252,.88))",
            "tab_bg": "rgba(255,255,255,.82)",
            "border": "rgba(30, 41, 59, 0.14)",
            "text": "#111827",
            "muted": "#5b6472",
            "hero_title": "#0b1220",
            "hero_copy": "#475569",
            "metric_value": "#111827",
            "metric_delta": "#047857",
            "section_title": "#111827",
            "sidebar_text": "#111827",
            "sidebar_muted": "#64748b",
            "shadow": "0 18px 50px rgba(15, 23, 42, 0.10)",
            "scan": "linear-gradient(115deg, transparent 0%, rgba(94,231,255,0.09) 42%, transparent 62%), repeating-linear-gradient(90deg, rgba(15,23,42,0.035) 0 1px, transparent 1px 80px)",
        }
    if mode == "Midnight":
        return {
            "app_bg": "radial-gradient(circle at 22% 0%, rgba(14,165,233,0.16), transparent 30%), linear-gradient(135deg, #020617 0%, #081120 50%, #020617 100%)",
            "sidebar_bg": "linear-gradient(180deg, rgba(2,6,23,0.98), rgba(8,17,32,0.96))",
            "panel": "rgba(8, 17, 32, 0.78)",
            "panel_strong": "rgba(15, 23, 42, 0.94)",
            "metric_bg": "linear-gradient(145deg, rgba(15,23,42,0.92), rgba(2,6,23,0.86)), radial-gradient(circle at top right, rgba(14,165,233,0.14), transparent 30%)",
            "hero_bg": "linear-gradient(135deg, rgba(15,23,42,0.92), rgba(2,6,23,0.86)), linear-gradient(90deg, rgba(14,165,233,0.12), rgba(34,197,94,0.08))",
            "quick_action_bg": "linear-gradient(145deg, rgba(15,23,42,.88), rgba(2,6,23,.82))",
            "tab_bg": "rgba(15,23,42,.72)",
            "border": "rgba(125, 211, 252, 0.18)",
            "text": "#f8fafc",
            "muted": "#9fb1c7",
            "hero_title": "#ffffff",
            "hero_copy": "#cbd5e1",
            "metric_value": "#ffffff",
            "metric_delta": "#9eeec0",
            "section_title": "#f8fafc",
            "sidebar_text": "#e5edf7",
            "sidebar_muted": "#9fb1c7",
            "shadow": "0 18px 58px rgba(0,0,0,.28)",
            "scan": "linear-gradient(115deg, transparent 0%, rgba(14,165,233,0.10) 42%, transparent 62%), repeating-linear-gradient(90deg, rgba(255,255,255,0.026) 0 1px, transparent 1px 80px)",
        }
    if mode == "Slate dark":
        return {
            "app_bg": "linear-gradient(135deg, #111827 0%, #1f2937 52%, #0f172a 100%)",
            "sidebar_bg": "linear-gradient(180deg, rgba(15,23,42,0.98), rgba(31,41,55,0.96))",
            "panel": "rgba(31, 41, 55, 0.76)",
            "panel_strong": "rgba(31, 41, 55, 0.94)",
            "metric_bg": "linear-gradient(145deg, rgba(31,41,55,0.92), rgba(15,23,42,0.84)), radial-gradient(circle at top right, rgba(34,197,94,0.10), transparent 30%)",
            "hero_bg": "linear-gradient(135deg, rgba(31,41,55,0.90), rgba(15,23,42,0.84)), linear-gradient(90deg, rgba(14,165,233,0.08), rgba(34,197,94,0.08))",
            "quick_action_bg": "linear-gradient(145deg, rgba(31,41,55,.86), rgba(15,23,42,.80))",
            "tab_bg": "rgba(31,41,55,.74)",
            "border": "rgba(203, 213, 225, 0.16)",
            "text": "#f8fafc",
            "muted": "#a9b5c6",
            "hero_title": "#ffffff",
            "hero_copy": "#d4dae3",
            "metric_value": "#ffffff",
            "metric_delta": "#9eeec0",
            "section_title": "#f8fafc",
            "sidebar_text": "#e5edf7",
            "sidebar_muted": "#a9b5c6",
            "shadow": "0 18px 54px rgba(0,0,0,.22)",
            "scan": "linear-gradient(115deg, transparent 0%, rgba(203,213,225,0.07) 42%, transparent 62%), repeating-linear-gradient(90deg, rgba(255,255,255,0.025) 0 1px, transparent 1px 80px)",
        }
    if mode == "High contrast dark":
        return {
            "app_bg": "linear-gradient(135deg, #000000 0%, #090c12 100%)",
            "sidebar_bg": "linear-gradient(180deg, #000000, #090c12)",
            "panel": "rgba(5, 7, 13, 0.90)",
            "panel_strong": "#090c12",
            "metric_bg": "linear-gradient(145deg, #090c12, #000000)",
            "hero_bg": "linear-gradient(135deg, #090c12, #000000)",
            "quick_action_bg": "linear-gradient(145deg, #090c12, #000000)",
            "tab_bg": "#090c12",
            "border": "rgba(248, 250, 252, 0.30)",
            "text": "#ffffff",
            "muted": "#d7dde7",
            "hero_title": "#ffffff",
            "hero_copy": "#e5e7eb",
            "metric_value": "#ffffff",
            "metric_delta": "#bbf7d0",
            "section_title": "#ffffff",
            "sidebar_text": "#ffffff",
            "sidebar_muted": "#d7dde7",
            "shadow": "0 18px 50px rgba(0,0,0,.34)",
            "scan": "repeating-linear-gradient(90deg, rgba(255,255,255,0.04) 0 1px, transparent 1px 80px)",
        }
    if mode == "Clean dark":
        return {
            "app_bg": "linear-gradient(135deg, #0b1020 0%, #111827 54%, #0b1220 100%)",
            "sidebar_bg": "linear-gradient(180deg, rgba(12,18,32,0.97), rgba(15,23,42,0.95))",
            "panel": "rgba(17, 24, 39, 0.78)",
            "panel_strong": "rgba(20, 29, 45, 0.92)",
            "metric_bg": "linear-gradient(145deg, rgba(20,29,45,0.92), rgba(12,18,32,0.84)), radial-gradient(circle at top right, rgba(94,231,255,0.10), transparent 30%)",
            "hero_bg": "linear-gradient(135deg, rgba(20,29,45,0.90), rgba(12,18,32,0.84)), linear-gradient(90deg, rgba(94,231,255,0.08), rgba(139,92,246,0.08))",
            "quick_action_bg": "linear-gradient(145deg, rgba(20,29,45,.86), rgba(12,18,32,.80))",
            "tab_bg": "rgba(17,24,39,.72)",
            "border": "rgba(148, 163, 184, 0.18)",
            "text": "#f8fafc",
            "muted": "#9aa7bd",
            "hero_title": "#ffffff",
            "hero_copy": "#cbd5e1",
            "metric_value": "#ffffff",
            "metric_delta": "#9eeec0",
            "section_title": "#f8fafc",
            "sidebar_text": "#e5edf7",
            "sidebar_muted": "#9aa7bd",
            "shadow": "0 18px 55px rgba(0,0,0,.22)",
            "scan": "linear-gradient(115deg, transparent 0%, rgba(94,231,255,0.08) 42%, transparent 62%), repeating-linear-gradient(90deg, rgba(255,255,255,0.025) 0 1px, transparent 1px 80px)",
        }
    return {
        "app_bg": "radial-gradient(circle at 18% 8%, rgba(94, 231, 255, 0.14), transparent 28%), radial-gradient(circle at 88% 10%, rgba(139, 92, 246, 0.18), transparent 32%), linear-gradient(135deg, #060914 0%, #09111f 48%, #070816 100%)",
        "sidebar_bg": "linear-gradient(180deg, rgba(5, 8, 20, 0.96), rgba(11, 18, 35, 0.94))",
        "panel": "rgba(14, 19, 36, 0.78)",
        "panel_strong": "rgba(17, 24, 45, 0.92)",
        "metric_bg": "linear-gradient(145deg, rgba(17, 24, 45, 0.90), rgba(9, 14, 28, 0.82)), radial-gradient(circle at top right, rgba(94, 231, 255, 0.16), transparent 30%)",
        "hero_bg": "linear-gradient(135deg, rgba(20, 30, 58, 0.88), rgba(11, 17, 32, 0.82)), linear-gradient(90deg, rgba(94, 231, 255, 0.12), rgba(139, 92, 246, 0.12))",
        "quick_action_bg": "linear-gradient(145deg, rgba(17, 24, 45, .84), rgba(10, 16, 31, .78))",
        "tab_bg": "rgba(14, 19, 36, .68)",
        "border": "rgba(148, 163, 184, 0.18)",
        "text": "#f8fafc",
        "muted": "#9aa7bd",
        "hero_title": "#ffffff",
        "hero_copy": "#cbd5e1",
        "metric_value": "#ffffff",
        "metric_delta": "#9eeec0",
        "section_title": "#f8fafc",
        "sidebar_text": "#e5edf7",
        "sidebar_muted": "#8fb2c7",
        "shadow": "0 18px 55px rgba(0,0,0,.22)",
        "scan": "linear-gradient(115deg, transparent 0%, rgba(94, 231, 255, 0.11) 42%, transparent 62%), repeating-linear-gradient(90deg, rgba(255,255,255,0.035) 0 1px, transparent 1px 80px)",
    }


def configure_page(page_title: str = APP_TITLE) -> None:
    st.set_page_config(
        page_title=page_title,
        page_icon="AI",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def apply_theme() -> None:
    tokens = _theme_tokens()
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {{
            --app-bg: {tokens["app_bg"]};
            --sidebar-bg: {tokens["sidebar_bg"]};
            --panel: {tokens["panel"]};
            --panel-strong: {tokens["panel_strong"]};
            --metric-bg: {tokens["metric_bg"]};
            --hero-bg: {tokens["hero_bg"]};
            --quick-action-bg: {tokens["quick_action_bg"]};
            --tab-bg: {tokens["tab_bg"]};
            --scan-overlay: {tokens["scan"]};
            --border: {tokens["border"]};
            --text: {tokens["text"]};
            --muted: {tokens["muted"]};
            --hero-title: {tokens["hero_title"]};
            --hero-copy: {tokens["hero_copy"]};
            --metric-value: {tokens["metric_value"]};
            --metric-delta: {tokens["metric_delta"]};
            --section-title: {tokens["section_title"]};
            --sidebar-text: {tokens["sidebar_text"]};
            --sidebar-muted: {tokens["sidebar_muted"]};
            --card-shadow: {tokens["shadow"]};
            --cyan: #5ee7ff;
            --violet: #8b5cf6;
            --green: #22c55e;
            --pink: #fb7185;
            --amber: #f59e0b;
        }}

        html, body, [class*="css"] {{
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        body {{
            background: var(--app-bg);
        }}

        header[data-testid="stHeader"] {{
            background: transparent;
        }}

        .stApp {{
            color: var(--text);
            background: var(--app-bg);
        }}

        .stApp,
        [data-testid="stMarkdownContainer"],
        [data-testid="stWidgetLabel"],
        [data-testid="stMetric"],
        [data-testid="stCaptionContainer"],
        .stRadio,
        .stSelectbox,
        .stMultiSelect,
        .stSlider,
        .stFileUploader {{
            color: var(--text);
        }}

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stWidgetLabel"] label,
        [data-testid="stCaptionContainer"] p {{
            color: var(--text);
        }}

        [data-testid="stSidebar"] {{
            background: var(--sidebar-bg);
            border-right: 1px solid var(--border);
        }}

        [data-testid="stSidebar"] * {{
            color: var(--sidebar-text);
        }}

        [data-testid="stSidebar"] .sidebar-muted {{
            color: var(--sidebar-muted);
        }}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1500px;
        }}

        h1, h2, h3 {{
            letter-spacing: 0;
        }}

        .hero-panel {{
            position: relative;
            overflow: hidden;
            border: 1px solid var(--border);
            border-radius: 22px;
            padding: 36px 38px;
            background: var(--hero-bg);
            box-shadow: var(--card-shadow);
            backdrop-filter: blur(18px);
        }}

        .hero-panel:before {{
            content: "";
            position: absolute;
            inset: 0;
            background: var(--scan-overlay);
            animation: scan 8s linear infinite;
            pointer-events: none;
        }}

        @keyframes scan {{
            from {{ transform: translateX(-20%); opacity: 0.8; }}
            to {{ transform: translateX(20%); opacity: 1; }}
        }}

        .hero-kicker {{
            position: relative;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            color: var(--cyan);
            font-size: 0.82rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: .14em;
        }}

        .hero-title {{
            position: relative;
            max-width: 900px;
            margin: 10px 0 10px;
            font-size: clamp(2.1rem, 5vw, 4.4rem);
            line-height: 1.02;
            font-weight: 800;
            color: var(--hero-title);
        }}

        .hero-copy {{
            position: relative;
            max-width: 860px;
            color: var(--hero-copy);
            font-size: 1.05rem;
            line-height: 1.65;
        }}

        .glass-card {{
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 22px;
            background: var(--panel);
            box-shadow: var(--card-shadow);
            backdrop-filter: blur(16px);
            transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease;
        }}

        .glass-card:hover {{
            transform: translateY(-2px);
            border-color: rgba(94, 231, 255, 0.42);
            box-shadow: 0 20px 70px rgba(94, 231, 255, .10);
        }}

        .glass-card h3,
        .sidebar-title {{
            color: var(--text);
        }}

        .card-body,
        .sidebar-subtitle {{
            color: var(--muted);
        }}

        .card-footer {{
            margin-top: 14px;
            color: var(--cyan);
            font-weight: 700;
        }}

        .metric-card {{
            min-height: 132px;
            border-radius: 18px;
            padding: 20px;
            border: 1px solid var(--border);
            background: var(--metric-bg);
            box-shadow: inset 0 1px 0 rgba(255,255,255,.08), var(--card-shadow);
        }}

        .metric-label {{
            color: var(--muted);
            font-size: .78rem;
            font-weight: 700;
            letter-spacing: .08em;
            text-transform: uppercase;
        }}

        .metric-value {{
            margin-top: 8px;
            color: var(--metric-value);
            font-size: 2rem;
            line-height: 1.1;
            font-weight: 800;
        }}

        .metric-delta {{
            margin-top: 8px;
            color: var(--metric-delta);
            font-size: .86rem;
            font-weight: 600;
        }}

        .section-title {{
            margin: 22px 0 10px;
            color: var(--section-title);
            font-size: 1.45rem;
            font-weight: 800;
        }}

        .subtle {{
            color: var(--muted);
        }}

        .status-pill {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(34, 197, 94, .12);
            color: #86efac;
            border: 1px solid rgba(34, 197, 94, .24);
            font-size: .82rem;
            font-weight: 700;
        }}

        .quick-action {{
            display: block;
            padding: 18px 18px;
            border-radius: 16px;
            border: 1px solid var(--border);
            background: var(--quick-action-bg);
            color: var(--text);
            text-decoration: none;
        }}

        div[data-testid="stMetric"] {{
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 16px;
            background: var(--panel);
        }}

        div[data-testid="stDataFrame"],
        div[data-testid="stTable"] {{
            border-radius: 14px;
            overflow: hidden;
        }}

        .stButton > button,
        .stDownloadButton > button {{
            border: 1px solid rgba(94, 231, 255, .35);
            border-radius: 12px;
            color: #f8fafc;
            background: linear-gradient(135deg, rgba(14, 165, 233, .92), rgba(124, 58, 237, .92));
            box-shadow: 0 12px 32px rgba(14, 165, 233, .18);
            transition: transform .18s ease, box-shadow .18s ease;
        }}

        .stButton > button:hover,
        .stDownloadButton > button:hover {{
            transform: translateY(-1px);
            border-color: rgba(94, 231, 255, .7);
            box-shadow: 0 16px 42px rgba(124, 58, 237, .25);
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}

        .stTabs [data-baseweb="tab"] {{
            border-radius: 999px;
            padding: 10px 16px;
            background: var(--tab-bg);
            border: 1px solid var(--border);
        }}

        input, textarea, [data-baseweb="select"] > div {{
            color: var(--text);
            background-color: var(--panel-strong);
        }}

        @media (max-width: 760px) {{
            .hero-panel {{ padding: 26px 22px; border-radius: 18px; }}
            .metric-value {{ font-size: 1.55rem; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(kicker: str, title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="hero-panel">
            <div class="hero-kicker">{kicker}</div>
            <div class="hero-title">{title}</div>
            <div class="hero-copy">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
