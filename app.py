import streamlit as st
from theme import inject_css, brand_header

st.set_page_config(page_title="RecallOps", page_icon="🧠", layout="wide")
inject_css()

with st.sidebar:
    brand_header()

welcome = st.Page("pages_/welcome.py", title="Welcome", icon=":material/rocket_launch:", default=True)
home = st.Page("pages_/home.py", title="Home", icon=":material/home:")
dashboard = st.Page("pages_/dashboard.py", title="Dashboard", icon=":material/monitoring:")
incidents = st.Page("pages_/incidents.py", title="Incidents", icon=":material/list_alt:")
memory_page = st.Page("pages_/memory_search.py", title="Memory", icon=":material/psychology:")
assistant = st.Page("pages_/assistant.py", title="AI Assistant", icon=":material/forum:")
report = st.Page("pages_/report_incident.py", title="Report Incident", icon=":material/add_circle:")
settings = st.Page("pages_/settings.py", title="Settings", icon=":material/settings:")
incident_detail = st.Page("pages_/incident_detail.py", title="Incident Detail",
                          icon=":material/description:", url_path="incident-detail")

nav = st.navigation([welcome, home, dashboard, incidents, memory_page, assistant, report, settings, incident_detail])
nav.run()