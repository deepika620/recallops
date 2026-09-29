import html
import streamlit as st

PRIMARY = "#6366f1"
SEV_COLOR = {"SEV-1": "#ef4444", "SEV-2": "#f59e0b", "SEV-3": "#3b82f6"}


def esc(x):
    return html.escape(str(x))


def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        .stApp, .stApp button, .stApp textarea, .stApp input {font-family:'Inter',system-ui,sans-serif;}
        .stApp {
          background:
            radial-gradient(900px 540px at 14% -6%, rgba(37,99,235,.38), transparent 60%),
            radial-gradient(760px 520px at 96% 38%, rgba(14,165,233,.17), transparent 60%),
            linear-gradient(rgba(96,165,250,.05) 1px, transparent 1px) 0 0 / 48px 48px,
            linear-gradient(90deg, rgba(96,165,250,.05) 1px, transparent 1px) 0 0 / 48px 48px,
            #040816 !important;
        }
        #MainMenu, footer {visibility:hidden;}
        header[data-testid="stHeader"] {background:transparent;}
        .block-container {padding-top:1.4rem; max-width:1180px;}

        [data-testid="stSidebar"] {background:#0f1629; border-right:1px solid rgba(255,255,255,.06);}
        [data-testid="stSidebarNav"] a[href$="/incident-detail"] {display:none !important;}

        .brand {display:flex; align-items:center; gap:10px; padding:.6rem .2rem 1rem;}
        .brand-icon {width:38px; height:38px; border-radius:11px;
                     background:linear-gradient(135deg,#6366f1,#8b5cf6);
                     display:flex; align-items:center; justify-content:center; font-size:19px;}
        .brand-name {color:#fff; font-weight:700; font-size:1.05rem;}
        .brand-sub {color:#8b93a7; font-size:.72rem;}

        .hero {display:flex; align-items:center; justify-content:space-between; gap:1rem;
               padding:1.4rem 1.8rem; border-radius:18px; margin-bottom:1.2rem;
               background:linear-gradient(135deg, rgba(99,102,241,.38), rgba(139,92,246,.16));
               border:1px solid rgba(255,255,255,.10);}
        .hero-title {font-size:1.7rem; font-weight:700; color:#fff; letter-spacing:-.02em;
                     display:flex; align-items:center; gap:.6rem;}
        .hero-emoji {font-size:2.6rem; line-height:1;}
        .hero-sub {margin-top:.25rem; color:#c7d2fe; font-size:.95rem;}
        .pill {padding:4px 12px; border-radius:999px; font-size:.75rem; font-weight:600;
               background:rgba(255,255,255,.10); color:#e0e7ff; border:1px solid rgba(255,255,255,.14);
               white-space:nowrap;}

        .stButton button, .stDownloadButton button, [data-testid="stFormSubmitButton"] button {
          border-radius:10px; border:1px solid rgba(255,255,255,.14);
          background:rgba(255,255,255,.04); color:#e5e7eb; font-weight:500;
          padding:.45rem 1rem; transition:all .18s ease;}
        .stButton button:hover, .stDownloadButton button:hover,
        [data-testid="stFormSubmitButton"] button:hover {
          border-color:#818cf8; background:rgba(99,102,241,.16); color:#fff;
          transform:translateY(-1px); box-shadow:0 6px 18px rgba(99,102,241,.25);}
        button[kind="primary"], button[data-testid="stBaseButton-primary"],
        button[data-testid="stBaseButton-primaryFormSubmit"] {
          background:linear-gradient(135deg,#6366f1,#8b5cf6) !important;
          border:none !important; color:#fff !important; font-weight:600;}

        [data-testid="stMetric"] {background:rgba(255,255,255,.035); border:1px solid rgba(255,255,255,.08);
                                   padding:.8rem 1rem; border-radius:14px;}
        [data-testid="stMetricValue"] {font-size:1.5rem; font-weight:700;}
        [data-baseweb="textarea"], [data-baseweb="input"], [data-baseweb="select"] > div {border-radius:10px !important;}

        .card {padding:1.2rem 1.4rem; border-radius:16px; margin:.4rem 0 1rem;
               background:linear-gradient(180deg, rgba(255,255,255,.05), rgba(255,255,255,.02));
               border:1px solid rgba(255,255,255,.10);}
        .card-title {font-size:1.35rem; font-weight:700; margin:.6rem 0 .2rem; color:#f8fafc;}
        .card-sub {color:#9ca3af;}
        .badge {display:inline-block; padding:2px 10px; border-radius:999px; font-size:.75rem;
                font-weight:600; color:#fff; margin-right:6px;}
        .label {font-size:.72rem; font-weight:600; letter-spacing:.08em; text-transform:uppercase;
                color:#94a3b8; margin:1rem 0 .4rem;}
        .note {padding:.7rem .9rem; border-radius:10px; margin-bottom:.45rem; font-size:.95rem;
               line-height:1.45; border:1px solid transparent;}
        .note.info {background:rgba(99,102,241,.10); border-color:rgba(99,102,241,.30);}
        .note.good {background:rgba(34,197,94,.10); border-color:rgba(34,197,94,.30); color:#bbf7d0;}
        .note.bad {background:rgba(239,68,68,.08); border-color:rgba(239,68,68,.28); color:#fecaca;}
        .note.muted {background:rgba(255,255,255,.03); border-color:rgba(255,255,255,.08); color:#94a3b8;}
        .empty {text-align:center; color:#94a3b8; padding:2.2rem 1rem; margin-top:1rem;
                border:1px dashed rgba(255,255,255,.14); border-radius:16px;}

        .kpi {padding:1rem 1.2rem; border-radius:14px; background:rgba(255,255,255,.035);
              border:1px solid rgba(255,255,255,.08);}
        .kpi-top {display:flex; align-items:center; gap:8px; color:#94a3b8; font-size:.82rem;}
        .kpi-val {font-size:1.6rem; font-weight:700; color:#f8fafc; margin-top:.3rem;}
        .kpi-delta {font-size:.78rem; margin-top:.2rem;}
        .kpi-delta.up {color:#4ade80;}
        .kpi-delta.down {color:#f87171;}

        .status-dot {width:8px; height:8px; border-radius:50%; display:inline-block; margin-right:6px;}
        .status-dot.on {background:#4ade80;}
        .status-dot.off {background:#6b7280;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def brand_header():
    st.markdown(
        """<div class="brand">
        <div class="brand-icon">🧠</div>
        <div><div class="brand-name">RecallOps</div>
        <div class="brand-sub">Past incidents. Smarter fixes. Faster.</div></div>
        </div>""",
        unsafe_allow_html=True,
    )


def hero_banner(title, subtitle, pill_text="Powered by Hindsight memory", icon="🧠"):
    icon_html = f'<span class="hero-emoji">{esc(icon)}</span>' if icon else ""
    st.markdown(
        f"""<div class="hero">
          <div>
            <div class="hero-title">{icon_html}{esc(title)}</div>
            <div class="hero-sub">{esc(subtitle)}</div>
          </div>
          <div class="pill">{esc(pill_text)}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def label(text):
    st.markdown(f'<div class="label">{esc(text)}</div>', unsafe_allow_html=True)


def note(text, kind="info"):
    st.markdown(f'<div class="note {kind}">{esc(text)}</div>', unsafe_allow_html=True)


def kpi_card(top, value, delta=None, delta_up=True):
    delta_html = ""
    if delta:
        cls = "up" if delta_up else "down"
        arrow = "▲" if delta_up else "▼"
        delta_html = f'<div class="kpi-delta {cls}">{arrow} {esc(delta)}</div>'
    st.markdown(
        f"""<div class="kpi"><div class="kpi-top">{esc(top)}</div>
        <div class="kpi-val">{esc(value)}</div>{delta_html}</div>""",
        unsafe_allow_html=True,
    )