import streamlit as st

import store
import charts
from theme import inject_css, esc, hero_banner, label, SEV_COLOR

inject_css()

hero_banner("Past Incidents & Learned Lessons", "Browse your incident history and see what the AI remembers.")

incidents = store.load_incidents()
df = charts.to_df(incidents)

# ---------------------------------------------------------------- filters
f1, f2, f3 = st.columns([2, 1, 1])
with f1:
    query = st.text_input("Search", placeholder="Search incidents, services, or keywords...",
                          label_visibility="collapsed")
with f2:
    services = ["All services"] + sorted(df["service"].unique().tolist())
    service_filter = st.selectbox("Service", services, label_visibility="collapsed")
with f3:
    severities = ["All severities"] + sorted(df["severity"].unique().tolist())
    severity_filter = st.selectbox("Severity", severities, label_visibility="collapsed")

# ---------------------------------------------------------------- apply filters
filtered = df.copy()
if query.strip():
    q = query.strip().lower()
    mask = (
        filtered["service"].str.lower().str.contains(q)
        | filtered["symptom"].str.lower().str.contains(q)
        | filtered["root_cause"].str.lower().str.contains(q)
        | filtered["fix"].str.lower().str.contains(q)
    )
    filtered = filtered[mask]
if service_filter != "All services":
    filtered = filtered[filtered["service"] == service_filter]
if severity_filter != "All severities":
    filtered = filtered[filtered["severity"] == severity_filter]

filtered = filtered.sort_values("date", ascending=False)

st.write("")
st.caption(f"{len(filtered)} of {len(df)} incidents")

# ---------------------------------------------------------------- incident cards
if filtered.empty:
    st.markdown('<div class="empty">No incidents match your filters.</div>', unsafe_allow_html=True)
else:
    for _, row in filtered.iterrows():
        color = SEV_COLOR.get(row["severity"], "#6b7280")
        with st.container(border=True):
            top1, top2 = st.columns([5, 1])
            with top1:
                st.markdown(
                    f"""<span class="badge" style="background:{color}">{esc(row['severity'])}</span>
                    <span class="badge" style="background:#334155">{esc(row['id'])}</span>
                    <div class="card-title" style="font-size:1.05rem; margin-top:.4rem;">{esc(row['symptom'])}</div>
                    <div class="card-sub">{esc(row['service'])} · {esc(row['category'])} · {row['date'].strftime('%b %d, %Y')}</div>""",
                    unsafe_allow_html=True,
                )
            with top2:
                st.markdown(
                    '<div style="text-align:right; margin-top:.5rem;">'
                    '<span class="badge" style="background:#22c55e;">Fixed</span></div>',
                    unsafe_allow_html=True,
                )

            b1, b2 = st.columns([5, 1])
            with b2:
                if st.button("View details", key=f"view_{row['id']}", icon=":material/arrow_forward:"):
                    st.session_state.selected_incident_id = row["id"]
                    st.switch_page("pages_/incident_detail.py")
