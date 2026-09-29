from datetime import date

import streamlit as st

import store
from theme import inject_css, hero_banner, label, note

inject_css()

hero_banner("Report a New Incident",
            "Add details about the incident so our AI can analyze it and learn from the experience.")

with st.form("report_form", clear_on_submit=False):
    c1, c2 = st.columns(2)
    with c1:
        service = st.text_input("Service", placeholder="e.g. Payment API")
    with c2:
        severity = st.selectbox("Severity", ["SEV-1 - Critical", "SEV-2 - Major", "SEV-3 - Minor"])

    title = st.text_input("Title", placeholder="e.g. Payment API returning 500 errors")
    description = st.text_area(
        "Description",
        placeholder="What happened? Include error messages, logs, and context...",
        height=140,
    )

    category = st.selectbox("Category", store.CATEGORIES)
    mttr = st.number_input("Minutes to resolve", min_value=1, value=30)
    root = st.text_area("Root cause (if known)")
    failed = st.text_area("What was tried and failed (one per line)")
    fix = st.text_area("What fixed it (leave blank if still investigating)")

    submitted = st.form_submit_button("Analyze & Get Recommendations", type="primary",
                                       icon=":material/psychology:")

if submitted:
    if not (service.strip() and title.strip() and description.strip()):
        note("Service, title, and description are required.", "bad")
    else:
        sev_code = severity.split(" - ")[0]
        new_inc = {
            "id": store.next_id(),
            "service": service.strip(),
            "severity": sev_code,
            "category": category,
            "date": date.today().isoformat(),
            "mttr_minutes": int(mttr),
            "symptom": f"{title.strip()}. {description.strip()}",
            "root_cause": root.strip() or "Not yet determined",
            "failed_attempts": [x.strip() for x in failed.splitlines() if x.strip()],
            "fix": fix.strip() or "Still investigating",
            "keywords": store.auto_keywords(service.strip(), description, root),
        }
        try:
            store.add_incident(new_inc)
            st.success(f"Saved {new_inc['id']} to memory. It can take a minute or two before it shows up in search.")
            label("What to check next")
            note("Check recent deployments and configuration changes around this time.", "info")
            note("Search Memory for similar past incidents once this one settles into the index.", "info")
            if st.button("Go to Memory search"):
                st.switch_page("pages_/memory_search.py")
        except Exception as e:
            note(f"Could not save to memory: {e}", "bad")