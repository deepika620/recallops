import json
from datetime import datetime

import streamlit as st

import store
import charts
from theme import inject_css, label, kpi_card, hero_banner

inject_css()

incidents = store.load_incidents()
df = charts.to_df(incidents)
feedback = store.load_feedback()

# ---------------------------------------------------------------- hero banner
hour = datetime.now().hour
greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
hero_banner("RecallOps", f"{greeting} — here's what's happening with your incident memory.")

# ---------------------------------------------------------------- KPI row
total = len(df)
resolved = int(df["mttr_minutes"].notna().sum())
helpful = sum(1 for f in feedback if f["worked"])

k1, k2, k3 = st.columns(3)
with k1:
    kpi_card("Total incidents", total)
with k2:
    kpi_card("Successful resolutions", resolved)
with k3:
    kpi_card("Feedback recorded", len(feedback),
             delta=f"{helpful} confirmed helpful" if feedback else None, delta_up=True)

st.write("")

# ---------------------------------------------------------------- growth chart + recent list
left, right = st.columns([1.6, 1])

with left:
    label("Memory growth")
    growth = df.sort_values("date").copy()
    growth["incidents_so_far"] = range(1, len(growth) + 1)
    growth["failed_so_far"] = growth["n_failed"].cumsum()
    fig = charts.px.line(
        growth, x="date", y=["incidents_so_far", "failed_so_far"],
        labels={"value": "count", "date": "", "variable": ""},
    )
    fig.data[0].name = "Incidents in memory"
    fig.data[1].name = "Failed attempts logged"
    fig = charts._style(fig)
    st.plotly_chart(fig, theme=None, config={"displayModeBar": False})

with right:
    label("Recent incidents")
    recent = df.sort_values("date", ascending=False).head(5)
    for _, row in recent.iterrows():
        color = {"SEV-1": "#ef4444", "SEV-2": "#f59e0b", "SEV-3": "#3b82f6"}.get(row["severity"], "#6b7280")
        st.markdown(
            f"""<div style="display:flex; justify-content:space-between; align-items:center;
                 padding:.5rem 0; border-bottom:1px solid rgba(255,255,255,.06);">
                 <div><div style="font-weight:600; font-size:.9rem;">{row['symptom'][:42]}</div>
                 <div style="font-size:.75rem; color:#8b93a7;">{row['service']} · {row['date'].strftime('%b %d')}</div></div>
                 <span class="badge" style="background:{color}">{row['severity']}</span>
                 </div>""",
            unsafe_allow_html=True,
        )

st.write("")
st.info("Use the sidebar to investigate an alert, browse memory, or log a new incident.")
