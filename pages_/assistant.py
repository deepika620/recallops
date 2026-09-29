import streamlit as st

from theme import inject_css, hero_banner, label
from memory import reflect

inject_css()

hero_banner("AI Incident Assistant",
            "Get intelligent recommendations based on your team's past incidents and what actually worked.")

SUGGESTED = [
    "What should I do for a payment API 500 error? It started right after a deployment.",
    "Which incidents were caused by a configuration change?",
    "What approaches have failed before for memory or OOM issues?",
    "How do I fix a database replication lag issue?",
]


@st.cache_data(ttl=1800, show_spinner=False)
def cached_ask(question):
    prompt = (
        "You are RecallOps AI, an assistant for on-call engineers. Answer using "
        "only what is in memory about past incidents. Structure your answer as: "
        "a one-line diagnosis of what this looks similar to, then 'From past "
        "experience:' with bullet points, marking failed approaches with an X "
        "and the working fix with a check mark. If memory has nothing relevant, "
        f"say so plainly instead of guessing.\n\nQuestion: {question}"
    )
    return reflect(prompt).text


st.session_state.setdefault("assistant_chat", [])

label("Suggested questions")
cols = st.columns(2)
for i, q in enumerate(SUGGESTED):
    if cols[i % 2].button(q, key=f"sugg_{i}"):
        st.session_state.assistant_chat.append({"role": "user", "text": q})
        with st.spinner("Analyzing past incidents..."):
            try:
                answer = cached_ask(q)
            except Exception as e:
                answer = f"Sorry, I couldn't reach memory right now: {e}"
        st.session_state.assistant_chat.append({"role": "assistant", "text": answer})
        st.rerun()

st.write("")

for m in st.session_state.assistant_chat:
    with st.chat_message(m["role"], avatar="🧠" if m["role"] == "assistant" else None):
        st.markdown(m["text"])

question = st.chat_input("Ask a follow-up question...")
if question:
    st.session_state.assistant_chat.append({"role": "user", "text": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant", avatar="🧠"):
        with st.spinner("Analyzing past incidents..."):
            try:
                answer = cached_ask(question.strip())
            except Exception as e:
                answer = f"Sorry, I couldn't reach memory right now: {e}"
        st.markdown(answer)
    st.session_state.assistant_chat.append({"role": "assistant", "text": answer})

if st.session_state.assistant_chat:
    if st.button("Clear conversation", icon=":material/delete:"):
        st.session_state.assistant_chat = []
        st.rerun()