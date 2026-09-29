import streamlit as st

import store
from handle_alert import search_alert
from theme import inject_css, hero_banner, esc, note, label, SEV_COLOR

inject_css()

hero_banner("Search Your Memory", "Ask a question and find relevant past incidents, fixes, and lessons.")

SUGGESTED = [
    "Payment service errors",
    "Database connection issues",
    "Redis memory leaks",
    "Deployment rollbacks",
    "Authentication timeouts",
]

incidents = store.load_incidents()


@st.cache_data(ttl=600, show_spinner=False)
def cached_search(q):
    return search_alert(q, top_n=6)


st.session_state.setdefault("mem_search_query", "")

query = st.text_input(
    "Search", value=st.session_state.mem_search_query,
    placeholder="e.g. Payment API issues, database connection problems...",
    label_visibility="collapsed",
)

label("Suggested searches")
cols = st.columns(len(SUGGESTED))
for i, s in enumerate(SUGGESTED):
    if cols[i].button(s, key=f"memsugg_{i}"):
        st.session_state.mem_search_query = s
        st.rerun()

st.write("")

if query.strip():
    with st.spinner("Searching memory..."):
        try:
            results = cached_search(query.strip())
        except Exception as e:
            results = []
            st.error(f"Search failed: {e}")

    if not results:
        st.markdown('<div class="empty">No matching memories found.</div>', unsafe_allow_html=True)
    else:
        matched_inc = store.match_incident(results[:4], incidents)
        overlap = store.relevance(query, matched_inc) if matched_inc else 0

        if matched_inc and overlap > 0:
            color = SEV_COLOR.get(matched_inc["severity"], "#6b7280")
            with st.container(border=True):
                st.markdown(
                    f"""<span class="badge" style="background:{color}">{esc(matched_inc['severity'])}</span>
                    <span class="badge" style="background:#334155">{esc(matched_inc['id'])}</span>
                    <div class="card-title" style="font-size:1.1rem; margin-top:.4rem;">{esc(matched_inc['service'])}</div>
                    <div class="card-sub">{esc(matched_inc['symptom'])}</div>""",
                    unsafe_allow_html=True,
                )
                b1, b2 = st.columns([5, 1])
                with b2:
                    if st.button("View details", key="memview", icon=":material/arrow_forward:"):
                        st.session_state.selected_incident_id = matched_inc["id"]
                        st.switch_page("pages_/incident_detail.py")
        else:
            note("No confident single-incident match. See raw memories below.", "muted")

        label("Raw memories from Hindsight")
        for i, text in enumerate(results, start=1):
            st.markdown(f'<div class="note muted">{esc(text)}</div>', unsafe_allow_html=True)
else:
    st.markdown(
        '<div class="empty">Type a question above, or pick a suggested search.</div>',
        unsafe_allow_html=True,
    )
