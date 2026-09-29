import streamlit as st

import store
from theme import inject_css, esc, note, label, SEV_COLOR

inject_css()

inc_id = st.session_state.get("selected_incident_id")
incidents = store.load_incidents()
inc = next((i for i in incidents if i["id"] == inc_id), None)

if st.button("← Back to Incidents"):
    st.switch_page("pages_/incidents.py")

if not inc:
    st.warning("No incident selected. Go back to Incidents and pick one.")
    st.stop()

color = SEV_COLOR.get(inc["severity"], "#6b7280")

st.markdown(
    f"""<div class="card">
    <span class="badge" style="background:{color}">{esc(inc['severity'])}</span>
    <span class="badge" style="background:#334155">{esc(inc['id'])}</span>
    <span class="badge" style="background:#22c55e">Fixed</span>
    <div class="card-title">{esc(inc['service'])}</div>
    <div class="card-sub">{esc(inc['symptom'])}</div>
    <div style="color:#8b93a7; font-size:.82rem; margin-top:.4rem;">
      {esc(inc['category'])} · {esc(inc['date'])} · {inc['mttr_minutes']} min to resolve
    </div></div>""",
    unsafe_allow_html=True,
)

tab_summary, tab_timeline, tab_lessons = st.tabs(["Summary", "Timeline", "Lessons Learned"])

with tab_summary:
    left, right = st.columns(2)
    with left:
        label("Problem")
        note(inc["symptom"], "info")
        label("Root cause")
        note(inc["root_cause"], "info")
    with right:
        label("What we tried (failed)")
        if inc["failed_attempts"]:
            for a in inc["failed_attempts"]:
                note(a, "bad")
        else:
            note("No failed attempts recorded.", "muted")
        label("What worked")
        note(inc["fix"], "good")

with tab_timeline:
    st.markdown(
        f"""
        <div style="border-left:2px solid rgba(255,255,255,.15); padding-left:1rem; margin-left:.4rem;">
          <div style="margin-bottom:1.2rem;">
            <div style="font-weight:600;">Incident detected</div>
            <div style="color:#8b93a7; font-size:.85rem;">{esc(inc['date'])}</div>
            <div class="card-sub" style="margin-top:.2rem;">{esc(inc['symptom'])}</div>
          </div>
          {''.join(f'''<div style="margin-bottom:1.2rem;">
            <div style="font-weight:600; color:#f87171;">Attempted fix failed</div>
            <div class="card-sub" style="margin-top:.2rem;">{esc(a)}</div>
          </div>''' for a in inc["failed_attempts"])}
          <div style="margin-bottom:1.2rem;">
            <div style="font-weight:600; color:#4ade80;">Resolved</div>
            <div style="color:#8b93a7; font-size:.85rem;">{inc['mttr_minutes']} minutes after detection</div>
            <div class="card-sub" style="margin-top:.2rem;">{esc(inc['fix'])}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_lessons:
    label("Key lesson")
    if inc["failed_attempts"]:
        st.markdown(
            f"""<div class="note info">
            {esc(inc['failed_attempts'][0])} did not solve this incident.
            {esc(inc['fix'])} successfully resolved the problem.
            </div>""",
            unsafe_allow_html=True,
        )
    else:
        note(f"{inc['fix']} resolved the problem on the first attempt.", "info")

    label("Related incidents")
    peers = [i for i in incidents if i["category"] == inc["category"] and i["id"] != inc["id"]]
    if peers:
        for p in peers[:3]:
            st.markdown(
                f'<div class="note muted"><b>{esc(p["service"])}</b> ({esc(p["id"])}): {esc(p["fix"])}</div>',
                unsafe_allow_html=True,
            )
    else:
        note("No other incidents in this category yet.", "muted")

# ---------------------------------------------------------------- feedback
st.write("")
label("Was this incident's fix helpful?")

feedback_log = store.load_feedback()
already_done = any(f["incident_id"] == inc["id"] for f in feedback_log)

if already_done:
    st.caption("Thanks — feedback for this incident has already been recorded.")
else:
    f1, f2, _ = st.columns([1, 1, 3])
    with f1:
        if st.button("Fix worked", icon=":material/thumb_up:", key=f"fb_up_{inc['id']}"):
            try:
                store.add_feedback(inc, inc["symptom"], True)
                st.success("Thanks! Saved to memory.")
                st.rerun()
            except Exception as e:
                st.error(f"Could not save feedback: {e}")
    with f2:
        if st.button("Didn't help", icon=":material/thumb_down:", key=f"fb_down_{inc['id']}"):
            try:
                store.add_feedback(inc, inc["symptom"], False)
                st.success("Thanks! Saved to memory.")
                st.rerun()
            except Exception as e:
                st.error(f"Could not save feedback: {e}")