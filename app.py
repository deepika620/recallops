import html
import json
from datetime import date

import streamlit as st

import charts
import store
from handle_alert import search_alert
from memory import reflect

st.set_page_config(page_title="RecallOps", page_icon="🧠", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
.stApp, .stApp button, .stApp textarea, .stApp input {font-family: 'Inter', system-ui, sans-serif;}
.stApp {background: radial-gradient(1100px 520px at 8% -8%, rgba(99,102,241,.20), transparent 60%), #0b1020;}
#MainMenu, footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}
.block-container {padding-top: 1.6rem; max-width: 1180px;}
[data-testid="stSidebar"] {background: #0f1629; border-right: 1px solid rgba(255,255,255,.06);}

.hero {display: flex; align-items: center; justify-content: space-between; gap: 1rem;
       padding: 1.4rem 1.8rem; border-radius: 18px; margin-bottom: 1.2rem;
       background: linear-gradient(135deg, rgba(99,102,241,.38), rgba(139,92,246,.16));
       border: 1px solid rgba(255,255,255,.10);}
.hero-title {font-size: 1.7rem; font-weight: 700; color: #fff; letter-spacing: -.02em;}
.hero-sub {margin-top: .25rem; color: #c7d2fe; font-size: .95rem;}
.pill {padding: 4px 12px; border-radius: 999px; font-size: .75rem; font-weight: 600;
       background: rgba(255,255,255,.10); color: #e0e7ff; border: 1px solid rgba(255,255,255,.14);
       white-space: nowrap;}

.stTabs [data-baseweb="tab-list"] {gap: 6px; border-bottom: 1px solid rgba(255,255,255,.08);}
.stTabs [data-baseweb="tab"] {padding: .6rem 1rem; font-weight: 600;}

.stButton button, .stDownloadButton button, [data-testid="stFormSubmitButton"] button {
  border-radius: 10px; border: 1px solid rgba(255,255,255,.14);
  background: rgba(255,255,255,.04); color: #e5e7eb; font-weight: 500;
  padding: .45rem 1rem; transition: all .18s ease;}
.stButton button:hover, .stDownloadButton button:hover,
[data-testid="stFormSubmitButton"] button:hover {
  border-color: #818cf8; background: rgba(99,102,241,.16); color: #fff;
  transform: translateY(-1px); box-shadow: 0 6px 18px rgba(99,102,241,.25);}
.stButton button:active {transform: translateY(0);}
button[kind="primary"], button[data-testid="stBaseButton-primary"],
button[data-testid="stBaseButton-primaryFormSubmit"] {
  background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
  border: none !important; color: #fff !important; font-weight: 600;}
.st-key-chips .stButton button {
  border-radius: 999px; font-size: .85rem; padding: .3rem .9rem; width: 100%;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;}

[data-testid="stMetric"] {background: rgba(255,255,255,.035); border: 1px solid rgba(255,255,255,.08);
                          padding: .8rem 1rem; border-radius: 14px;}
[data-testid="stMetricValue"] {font-size: 1.5rem; font-weight: 700;}
[data-baseweb="textarea"], [data-baseweb="input"], [data-baseweb="select"] > div {border-radius: 10px !important;}
[data-testid="stChatMessage"] {background: rgba(255,255,255,.03); border: 1px solid rgba(255,255,255,.07);
                               border-radius: 14px; padding: .8rem 1rem;}

.card {padding: 1.2rem 1.4rem; border-radius: 16px; margin: .4rem 0 1rem;
       background: linear-gradient(180deg, rgba(255,255,255,.05), rgba(255,255,255,.02));
       border: 1px solid rgba(255,255,255,.10);}
.card-title {font-size: 1.35rem; font-weight: 700; margin: .6rem 0 .2rem; color: #f8fafc;}
.card-sub {color: #9ca3af;}
.badge {display: inline-block; padding: 2px 10px; border-radius: 999px; font-size: .75rem;
        font-weight: 600; color: #fff; margin-right: 6px;}
.label {font-size: .72rem; font-weight: 600; letter-spacing: .08em; text-transform: uppercase;
        color: #94a3b8; margin: 1rem 0 .4rem;}
.note {padding: .7rem .9rem; border-radius: 10px; margin-bottom: .45rem; font-size: .95rem;
       line-height: 1.45; border: 1px solid transparent;}
.note.info {background: rgba(99,102,241,.10); border-color: rgba(99,102,241,.30);}
.note.good {background: rgba(34,197,94,.10); border-color: rgba(34,197,94,.30); color: #bbf7d0;}
.note.bad {background: rgba(239,68,68,.08); border-color: rgba(239,68,68,.28); color: #fecaca;}
.note.muted {background: rgba(255,255,255,.03); border-color: rgba(255,255,255,.08); color: #94a3b8;}
.empty {text-align: center; color: #94a3b8; padding: 2.2rem 1rem; margin-top: 1rem;
        border: 1px dashed rgba(255,255,255,.14); border-radius: 16px;}
</style>

<div class="hero">
  <div>
    <div class="hero-title">RecallOps</div>
    <div class="hero-sub">Incident memory for on-call engineers: what broke before, what failed, and what fixed it.</div>
  </div>
  <div class="pill">Powered by Hindsight memory</div>
</div>
""",
    unsafe_allow_html=True,
)

SEV_COLOR = {"SEV-1": "#ef4444", "SEV-2": "#f59e0b", "SEV-3": "#3b82f6"}
EXAMPLES = [
    "500 errors after deploy",
    "Pods running out of memory",
    "Auth errors after config",
    "Database replica lagging",
]
ASK_EXAMPLES = [
    "Which incidents were caused by a config change?",
    "What failed before we fixed the memory problem?",
    "What should I check first when a deploy causes 500 errors?",
]


# ------------------------------------------------------------------- helpers
def esc(x):
    return html.escape(str(x))


def label(text):
    st.markdown(f'<div class="label">{esc(text)}</div>', unsafe_allow_html=True)


def note(text, kind="info"):
    st.markdown(f'<div class="note {kind}">{esc(text)}</div>', unsafe_allow_html=True)


def plot(fig):
    st.plotly_chart(fig, theme=None, config={"displayModeBar": False})


# ------------------------------------------------------------ cached functions
@st.cache_data(ttl=600, show_spinner=False)
def cached_search(alert):
    return search_alert(alert)


@st.cache_data(ttl=1800, show_spinner=False)
def cached_plan(alert, inc_id):
    query = (
        f'An alert just fired: "{alert}". Based on past incidents, give a short '
        "step-by-step response plan for the on-call engineer: what to check first, "
        "the most likely fix, and which approaches to avoid because they failed before."
    )
    return reflect(query).text


@st.cache_data(ttl=1800, show_spinner=False)
def cached_ask(question):
    prompt = (
        "You are RecallOps, an assistant for on-call engineers. Answer using only "
        "what is in memory about past incidents, and name the service or incident "
        "you are drawing on. If memory has nothing relevant, say so plainly instead "
        f"of guessing.\n\nQuestion: {question}"
    )
    return reflect(prompt).text


@st.cache_data(show_spinner=False)
def dashboard_figs(incidents_json):
    df = charts.to_df(json.loads(incidents_json))
    return {
        "category": charts.category_chart(df),
        "mttr": charts.mttr_chart(df),
        "severity": charts.severity_chart(df),
        "attempts": charts.attempts_chart(df),
        "timeline": charts.timeline_chart(df),
    }


@st.cache_data(show_spinner=False)
def compare_fig(incidents_json, inc_id):
    incs = json.loads(incidents_json)
    inc = next(i for i in incs if i["id"] == inc_id)
    return charts.compare_chart(charts.to_df(incs), inc)


# ------------------------------------------------------------------- data
incidents = store.load_incidents()
incidents_json = json.dumps(incidents, sort_keys=True)
df = charts.to_df(incidents)
feedback = store.load_feedback()

with st.sidebar:
    st.markdown("### About")
    st.write("Search runs on **Hindsight** agent memory (bank: `recallops`).")
    st.metric("Incidents in memory", len(incidents))
    st.metric("Feedback entries", len(feedback))
    st.caption(
        "Severity, category, date and time-to-resolve come from a structured "
        "sample dataset used for the dashboard."
    )

tab_find, tab_dash, tab_log, tab_ask = st.tabs([
    ":material/search: Investigate",
    ":material/monitoring: Dashboard",
    ":material/add_circle: Log incident",
    ":material/forum: Ask memory",
])


# ---------------------------------------------------------------- Investigate
def set_example(text):
    st.session_state.alert_text = text


def save_feedback(inc, alert, worked, key):
    try:
        store.add_feedback(inc, alert, worked)
    except Exception as e:
        st.error(f"Could not save feedback: {e}")
        return
    cached_search.clear()
    cached_ask.clear()
    st.session_state.setdefault("fb_done", set()).add(key)
    st.rerun()


@st.fragment
def match_view(inc, overlap, alert):
    color = SEV_COLOR.get(inc["severity"], "#6b7280")
    st.markdown(
        f"""<div class="card">
        <span class="badge" style="background:{color}">{esc(inc['severity'])}</span>
        <span class="badge" style="background:#334155">{esc(inc['category'])}</span>
        <span class="badge" style="background:#334155">{esc(inc['id'])}</span>
        <div class="card-title">{esc(inc['service'])}</div>
        <div class="card-sub">{esc(inc['symptom'])}</div></div>""",
        unsafe_allow_html=True,
    )

    avg = df["mttr_minutes"].mean()
    level = "High" if overlap >= 3 else "Medium" if overlap == 2 else "Low"
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Time to resolve", f"{inc['mttr_minutes']} min",
              delta=f"{inc['mttr_minutes'] - avg:+.0f} min vs avg", delta_color="inverse")
    m2.metric("Failed attempts", len(inc["failed_attempts"]))
    m3.metric("Date", inc["date"])
    m4.metric("Relevance", level)

    left, right = st.columns(2)
    with left:
        label("Root cause")
        note(inc["root_cause"], "info")
        label("What did not work")
        if inc["failed_attempts"]:
            for a in inc["failed_attempts"]:
                note(a, "bad")
        else:
            note("No failed attempts recorded.", "muted")
    with right:
        label("What worked")
        note(inc["fix"], "good")
        peers = [i for i in incidents
                 if i["category"] == inc["category"] and i["id"] != inc["id"]]
        if peers:
            label(f"Other {inc['category']} incidents")
            for p in peers:
                st.markdown(
                    f'<div class="note muted"><b>{esc(p["service"])}</b>: {esc(p["fix"])}</div>',
                    unsafe_allow_html=True,
                )

    label("Actions")
    plan_key = (alert, inc["id"])
    c1, c2, _ = st.columns([1.3, 1.3, 2.4])
    if c1.button("Generate response plan", icon=":material/auto_awesome:",
                 key=f"plan_{inc['id']}"):
        with st.spinner("Asking Hindsight to reflect on past incidents..."):
            try:
                st.session_state.plan = {
                    "key": plan_key, "text": cached_plan(alert, inc["id"]),
                }
            except Exception as e:
                st.error(f"Could not generate a plan: {e}")
    c2.download_button(
        "Download postmortem", store.postmortem_md(inc),
        file_name=f"{inc['id']}_postmortem.md", mime="text/markdown",
        icon=":material/download:", key=f"pm_{inc['id']}", on_click="ignore",
    )

    plan = st.session_state.get("plan")
    if plan and plan["key"] == plan_key:
        label("Response plan (Hindsight reflect)")
        with st.container(border=True):
            st.markdown(plan["text"])

    label("Was this helpful?")
    done = st.session_state.setdefault("fb_done", set())
    if plan_key in done:
        st.caption("Thanks, your feedback was saved to memory.")
    else:
        f1, f2, _ = st.columns([1, 1, 3])
        if f1.button("Fix worked", icon=":material/thumb_up:", key=f"up_{inc['id']}"):
            save_feedback(inc, alert, True, plan_key)
        if f2.button("Didn't help", icon=":material/thumb_down:", key=f"down_{inc['id']}"):
            save_feedback(inc, alert, False, plan_key)

    plot(compare_fig(incidents_json, inc["id"]))


with tab_find:
    st.caption("Try an example or paste your own alert.")
    with st.container(key="chips"):
        cols = st.columns(len(EXAMPLES))
        for i, ex in enumerate(EXAMPLES):
            cols[i].button(ex, key=f"ex{i}", on_click=set_example, args=(ex,))

    alert = st.text_area(
        "Alert", key="alert_text", height=90,
        placeholder="e.g. Pods keep restarting and running out of memory",
    )

    if st.button("Investigate", type="primary", icon=":material/search:") and alert.strip():
        with st.spinner("Searching incident memory..."):
            try:
                st.session_state.result = {
                    "alert": alert.strip(), "related": cached_search(alert.strip()),
                }
            except Exception as e:
                st.session_state.result = None
                st.error(f"Memory search failed: {e}")

    res = st.session_state.get("result")
    if not res:
        st.markdown(
            '<div class="empty">Paste an alert above to find the closest past incident.</div>',
            unsafe_allow_html=True,
        )
    else:
        inc = store.match_incident(res["related"][:4], incidents)
        overlap = store.relevance(res["alert"], inc) if inc else 0

        if inc and overlap > 0:
            match_view(inc, overlap, res["alert"])
        else:
            st.warning(
                "No confident match. Nothing in memory looks closely related to this "
                "alert. Check the raw memories below, and consider logging this "
                "incident once it is resolved."
            )

        with st.expander("Raw memories recalled from Hindsight"):
            for i, text in enumerate(res["related"], start=1):
                st.markdown(f"**{i}.** {text}")


# ------------------------------------------------------------------ Dashboard
with tab_dash:
    figs = dashboard_figs(incidents_json)
    helpful = sum(1 for f in feedback if f["worked"])
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total incidents", len(df))
    k2.metric("Avg. time to resolve", f"{df['mttr_minutes'].mean():.0f} min")
    k3.metric("Top category", df["category"].mode().iloc[0])
    k4.metric("Fixed first try", f"{df['first_try'].mean() * 100:.0f}%")
    k5.metric("Fix feedback",
              f"{helpful}/{len(feedback)} helpful" if feedback else "None yet")

    c1, c2 = st.columns(2)
    with c1:
        plot(figs["category"])
    with c2:
        plot(figs["mttr"])

    c3, c4 = st.columns(2)
    with c3:
        plot(figs["severity"])
    with c4:
        plot(figs["attempts"])

    plot(figs["timeline"])

    label("All incidents")
    table = charts.table_df(incidents)
    st.dataframe(table)
    st.download_button("Download as CSV", table.to_csv(index=False),
                       file_name="recallops_incidents.csv", mime="text/csv",
                       icon=":material/download:", on_click="ignore")


# ---------------------------------------------------------------- Log incident
with tab_log:
    st.caption("Save a resolved incident so the next on-call engineer can find it.")
    with st.form("log_form", clear_on_submit=True):
        a, b, c = st.columns(3)
        service = a.text_input("Service", placeholder="e.g. billing-service")
        severity = b.selectbox("Severity", ["SEV-1", "SEV-2", "SEV-3"])
        category = c.selectbox("Category", store.CATEGORIES)
        mttr = st.number_input("Minutes to resolve", min_value=1, value=30)
        symptom = st.text_area("What did users or alerts show?")
        root = st.text_area("Root cause")
        failed = st.text_area("What was tried and failed (one per line)")
        fix = st.text_area("What fixed it")
        submitted = st.form_submit_button("Save to memory", type="primary")

    if submitted:
        if not (service.strip() and symptom.strip() and root.strip() and fix.strip()):
            st.error("Service, symptom, root cause and fix are required.")
        else:
            new_inc = {
                "id": store.next_id(),
                "service": service.strip(),
                "severity": severity,
                "category": category,
                "date": date.today().isoformat(),
                "mttr_minutes": int(mttr),
                "symptom": symptom.strip(),
                "root_cause": root.strip(),
                "failed_attempts": [x.strip() for x in failed.splitlines() if x.strip()],
                "fix": fix.strip(),
                "keywords": store.auto_keywords(service.strip(), symptom, root),
            }
            try:
                store.add_incident(new_inc)
                cached_search.clear()
                cached_ask.clear()
                st.success(
                    f"Saved {new_inc['id']}. It can take a minute or two before "
                    "it shows up in search results."
                )
            except Exception as e:
                st.error(f"Could not save to memory: {e}")


# --------------------------------------------------------------- Ask memory
def ask_memory(question):
    question = question.strip()
    if not question:
        return
    st.session_state.chat.append({"role": "user", "text": question})
    try:
        answer = cached_ask(question)
    except Exception as e:
        answer = f"Sorry, I couldn't reach memory right now: {e}"
    st.session_state.chat.append({"role": "assistant", "text": answer})


with tab_ask:
    st.caption("Ask a question across all past incidents. Answers come from Hindsight memory.")
    st.session_state.setdefault("chat", [])

    with st.container(key="ask_chips"):
        for i, q in enumerate(ASK_EXAMPLES):
            if st.button(q, key=f"askex{i}"):
                with st.spinner("Searching memory..."):
                    ask_memory(q)

    question = st.chat_input("Ask about past incidents...", key="ask_input")
    if question:
        with st.spinner("Searching memory..."):
            ask_memory(question)

    if not st.session_state.chat:
        st.markdown(
            '<div class="empty">Pick a suggested question or type your own.</div>',
            unsafe_allow_html=True,
        )
    else:
        for m in st.session_state.chat:
            with st.chat_message(m["role"]):
                st.markdown(m["text"])
        if st.button("Clear conversation", icon=":material/delete:", key="clear_chat"):
            st.session_state.chat = []
            st.rerun()
import streamlit.components.v1 as components

def render_project_assistant():
    st.divider()
    components.html(
        """
<div style="font-family:'Inter',sans-serif; max-width:640px; border-radius:16px;
     overflow:hidden; box-shadow:0 8px 28px rgba(0,0,0,.35);
     border:1px solid rgba(255,255,255,.10);">

  <div style="display:flex; align-items:center; gap:10px; padding:12px 16px;
       background:linear-gradient(135deg,#6366f1,#8b5cf6);">
    <div style="width:36px; height:36px; border-radius:50%; background:rgba(255,255,255,.2);
         display:flex; align-items:center; justify-content:center; font-size:18px;">🧠</div>
    <div>
      <div style="color:#fff; font-weight:700; font-size:14.5px;">RecallOps Assistant</div>
      <div style="color:#e0e7ff; font-size:11.5px; display:flex; align-items:center; gap:5px;">
        <span style="width:7px; height:7px; border-radius:50%; background:#4ade80; display:inline-block;"></span>
        Online · answers from project FAQ
      </div>
    </div>
  </div>

  <div id="ro-log" style="height:230px; overflow-y:auto; padding:14px; background:#0d1326;"></div>

  <div style="display:flex; gap:8px; padding:10px; background:#0f1629;
       border-top:1px solid rgba(255,255,255,.08);">
    <input id="ro-input" placeholder="Ask about RecallOps..." style="flex:1;
      padding:10px 12px; border-radius:20px; border:1px solid rgba(255,255,255,.16);
      background:#1a2036; color:#fff; font-size:13px; outline:none;">
    <button id="ro-mic" title="Speak" style="border:none; border-radius:50%; width:38px; height:38px;
      background:#1a2036; color:#fff; cursor:pointer; font-size:16px;">🎤</button>
    <button id="ro-send" style="border:none; border-radius:50%; width:38px; height:38px;
      background:linear-gradient(135deg,#6366f1,#8b5cf6); color:#fff; cursor:pointer; font-size:15px;">➤</button>
  </div>
</div>

<script>
const FAQ = [
  {k:["what is recallops","what does this do","about"],
   a:"RecallOps is incident memory for on-call engineers. It recalls similar past incidents, what fixed them, and what didn't, using Hindsight agent memory."},
  {k:["hindsight","memory work","how does it work"],
   a:"RecallOps uses Hindsight's retain to store each incident and feedback, recall to find the closest past incident by meaning, and reflect to synthesize a response plan or answer questions across incidents."},
  {k:["tab","investigate","dashboard","log incident","ask memory"],
   a:"There are four tabs: Investigate (paste an alert, get the closest fix), Dashboard (charts and KPIs), Log incident (save a new resolved incident), and Ask memory (chat across all incidents)."},
  {k:["tech stack","built with","technology"],
   a:"It's built with Python, Streamlit for the UI, Plotly for charts, pandas, and Hindsight for agent memory."},
  {k:["response plan"],
   a:"The response plan button asks Hindsight to reflect across past incidents and produce a step-by-step plan, including approaches that failed before."},
  {k:["feedback"],
   a:"After viewing a fix, you can mark it as helpful or not. That outcome is stored back into memory, so the system learns over time."},
  {k:["postmortem"],
   a:"You can download a ready-to-edit Markdown postmortem for any matched incident, with root cause, what failed, the fix, and follow-up actions."},
  {k:["limitation","accurate","confident"],
   a:"Recall always returns the nearest memories, so a keyword-overlap check flags low-relevance matches as 'no confident match' instead of showing a misleading fix."},
];

function findAnswer(q) {
  q = q.toLowerCase();
  for (const item of FAQ) {
    if (item.k.some(kw => q.includes(kw))) return item.a;
  }
  return "I can answer questions about what RecallOps is, how Hindsight memory is used, the four tabs, the tech stack, and its limitations. Try asking about one of those.";
}

const log = document.getElementById("ro-log");
const input = document.getElementById("ro-input");
const sendBtn = document.getElementById("ro-send");
const micBtn = document.getElementById("ro-mic");

function addMsg(text, who) {
  const row = document.createElement("div");
  row.style.display = "flex";
  row.style.gap = "8px";
  row.style.margin = "10px 0";
  row.style.flexDirection = who === "user" ? "row-reverse" : "row";

  const avatar = document.createElement("div");
  avatar.style.cssText = "width:26px;height:26px;border-radius:50%;flex-shrink:0;" +
    "display:flex;align-items:center;justify-content:center;font-size:13px;" +
    (who === "user" ? "background:#334155;" : "background:linear-gradient(135deg,#6366f1,#8b5cf6);");
  avatar.textContent = who === "user" ? "🧑" : "🧠";

  const bubble = document.createElement("div");
  bubble.style.cssText = "max-width:78%; padding:8px 12px; border-radius:14px; font-size:13px; " +
    "line-height:1.4; color:#fff;" +
    (who === "user"
      ? "background:#6366f1; border-bottom-right-radius:4px;"
      : "background:rgba(255,255,255,.07); border-bottom-left-radius:4px;");
  bubble.textContent = text;

  row.appendChild(avatar);
  row.appendChild(bubble);
  log.appendChild(row);
  log.scrollTop = log.scrollHeight;
}

function speak(text) {
  if (!window.speechSynthesis) return;
  window.speechSynthesis.speak(new SpeechSynthesisUtterance(text));
}

function handleSend() {
  const q = input.value.trim();
  if (!q) return;
  addMsg(q, "user");
  input.value = "";
  setTimeout(() => { const a = findAnswer(q); addMsg(a, "bot"); speak(a); }, 200);
}

sendBtn.onclick = handleSend;
input.addEventListener("keydown", e => { if (e.key === "Enter") handleSend(); });

const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
if (SR) {
  const rec = new SR();
  rec.lang = "en-US";
  rec.onresult = e => { input.value = e.results[0][0].transcript; handleSend(); };
  micBtn.onclick = () => rec.start();
} else {
  micBtn.onclick = () => addMsg("Voice input isn't supported in this browser. Try Chrome or Edge.", "bot");
}

addMsg("Hi! Ask me anything about RecallOps, or tap the mic to speak.", "bot");
</script>
        """,
        height=430,
    )


render_project_assistant()