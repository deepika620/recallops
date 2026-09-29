import streamlit as st

import store
from theme import inject_css, hero_banner, label

inject_css()

hero_banner("Settings", "Connections, memory bank, and organization details.")

tab_connections, tab_bank, tab_org = st.tabs(["Connections", "Memory Bank", "Organization"])

with tab_connections:
    label("Integrations")
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("**🧠 Hindsight**")
            st.markdown(
                '<span class="status-dot on"></span> Connected',
                unsafe_allow_html=True,
            )
            st.caption("Memory & recall")
    with c2:
        with st.container(border=True):
            st.markdown("**🖥️ Streamlit**")
            st.markdown(
                '<span class="status-dot on"></span> Connected',
                unsafe_allow_html=True,
            )
            st.caption("Frontend UI")

with tab_bank:
    incidents = store.load_incidents()
    feedback = store.load_feedback()
    label("Memory bank")
    c1, c2, c3 = st.columns(3)
    c1.metric("Bank ID", "recallops")
    c2.metric("Incidents stored", len(incidents))
    c3.metric("Feedback entries", len(feedback))
    st.caption(
        "Every incident (symptom, root cause, failed attempts, fix) and every "
        "feedback click is retained in Hindsight. Recall and reflect draw on all of it."
    )

with tab_org:
    label("Organization")
    with st.container(border=True):
        st.markdown("**RecallOps**")
        st.caption("Free plan · Hackathon build")