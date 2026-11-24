"""NovaDesk FAQ Chatbot - Streamlit entry point."""
import os
import time
from pathlib import Path
import pandas as pd
import streamlit as st

from modules import ui
from modules.data_manager import FAQStore
from modules.nlp import FAQEngine

BASE = Path(__file__).parent
WELCOME = {"role": "bot", "text": "Hi, I'm Nova! 👋 Ask me anything about NovaDesk: accounts, pricing, features, "
                                  "troubleshooting or privacy. Pick a suggestion below or type your own question."}

st.set_page_config(page_title="NovaDesk FAQ Chatbot", page_icon="💬", layout="wide")
ui.load_css(BASE / "assets" / "style.css")
S = st.session_state


def init():
    if "store" in S:
        return
    S.store = FAQStore(BASE / "data" / "faqs.csv")
    S.warnings = S.store.load()
    S.engine = FAQEngine(S.store.df)
    S.messages = [dict(WELCOME)]
    S.asked, S.matched, S.unanswered, S.scores = 0, 0, [], []
    S.pending, S.admin_ok = None, False


def rebuild_engine():
    S.engine = FAQEngine(S.store.df)


def ask_this(question):
    S.pending = question


def clear_chat():
    S.messages = [dict(WELCOME)]
    S.asked, S.matched, S.unanswered, S.scores = 0, 0, [], []


init()

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown('<div class="brand">💬 NovaDesk AI</div><div class="brand-sub">Smart FAQ Assistant</div>',
                unsafe_allow_html=True)
    page = st.radio("Navigation", ["💬 Chat", "📊 Dashboard", "🛠️ Admin", "ℹ️ About"], label_visibility="collapsed")
    st.divider()
    S.threshold = st.slider("Similarity threshold", 0.05, 0.9, 0.25, 0.05,
                            help="Higher = stricter matching. Below this score the bot shows a fallback message.")
    st.button("🗑️ Clear chat", on_click=clear_chat)
    st.caption(f"{len(S.store.df)} FAQs loaded · {S.asked} questions asked")


# ---------------- Pages ----------------
def chat_page():
    ui.hero("Ask Nova", "Instant answers from the NovaDesk knowledge base, powered by TF-IDF and cosine similarity.")
    for w in S.warnings:
        st.warning(w)
    question = st.chat_input("Ask a question about NovaDesk...")
    if S.pending:
        question, S.pending = S.pending, None

    for msg in S.messages:
        ui.bubble(msg)

    if question is not None:
        if not question.strip():
            st.warning("Please type a question first.")
            return
        ui.bubble({"role": "user", "text": question})
        slot = st.empty()
        slot.markdown(ui.TYPING, unsafe_allow_html=True)
        time.sleep(0.6)
        try:
            res = S.engine.ask(question, S.threshold)
        except Exception as exc:  # keep the app alive whatever happens
            slot.empty()
            st.error(f"Something went wrong while searching: {exc}")
            return
        S.asked += 1
        S.scores.append(res.score)
        if res.matched:
            S.matched += 1
        else:
            S.unanswered.append(question)
        S.messages.append({"role": "user", "text": question})
        S.messages.append({"role": "bot", "text": res.answer, "category": res.category if res.matched else "",
                           "score": res.score, "miss": not res.matched, "related": res.related})
        st.rerun()

    last = S.messages[-1]
    if len(S.messages) == 1 and len(S.store.df):
        st.markdown('<div class="section-title">✨ Suggested questions</div>', unsafe_allow_html=True)
        picks = S.store.df.groupby("category", sort=False).head(1)["question"].tolist()[:6]
        cols = st.columns(2)
        for i, q in enumerate(picks):
            cols[i % 2].button(q, key=f"sg{i}", on_click=ask_this, args=(q,))
    elif last["role"] == "bot" and last.get("related"):
        st.markdown('<div class="section-title">🔗 Related questions</div>', unsafe_allow_html=True)
        for i, q in enumerate(last["related"]):
            st.button(q, key=f"rl{len(S.messages)}_{i}", on_click=ask_this, args=(q,))


def dashboard_page():
    ui.hero("Dashboard", "Live performance of the chatbot in this session.")
    unanswered = S.asked - S.matched
    rate = (S.matched / S.asked) if S.asked else 0.0
    cols = st.columns(4)
    with cols[0]:
        ui.metric("Total FAQs", len(S.store.df), "📚", f"{len(S.store.categories())} categories")
    with cols[1]:
        ui.metric("Questions asked", S.asked, "💬", "this session")
    with cols[2]:
        ui.metric("Matched", S.matched, "✅", "answered successfully")
    with cols[3]:
        ui.metric("Unanswered", unanswered, "❓", "below threshold")
    st.markdown('<div class="section-title">Performance summary</div>', unsafe_allow_html=True)
    st.progress(rate, text=f"Success rate: {rate * 100:.0f}%")
    avg = sum(S.scores) / len(S.scores) if S.scores else 0
    st.write(f"Average match score: **{avg * 100:.0f}%** · Current threshold: **{S.threshold:.2f}**")
    left, right = st.columns(2)
    with left:
        st.markdown('<div class="section-title">FAQs per category</div>', unsafe_allow_html=True)
        if len(S.store.df):
            st.bar_chart(S.store.df["category"].value_counts(), color="#8b5cf6")
    with right:
        st.markdown('<div class="section-title">Unanswered questions</div>', unsafe_allow_html=True)
        if S.unanswered:
            for q in S.unanswered[-8:]:
                st.write("•", q)
        else:
            st.caption("None yet. Ask something on the Chat page.")


def admin_page():
    ui.hero("FAQ Management", "Add or remove FAQs. The NLP model is retrained instantly.")
    try:
        password = st.secrets.get("ADMIN_PASSWORD") or os.getenv("ADMIN_PASSWORD")
    except Exception:
        password = os.getenv("ADMIN_PASSWORD")
    if password and not S.admin_ok:
        entered = st.text_input("Admin password", type="password")
        if entered and entered == password:
            S.admin_ok = True
            st.rerun()
        elif entered:
            st.error("Incorrect password.")
        return

    with st.form("add_faq", clear_on_submit=True):
        st.subheader("➕ Add a FAQ")
        cats = S.store.categories()
        category = st.selectbox("Category", cats + ["➕ New category"] if cats else ["➕ New category"])
        new_cat = st.text_input("New category name (only if you chose New category)")
        question = st.text_input("Question")
        answer = st.text_area("Answer")
        if st.form_submit_button("Add FAQ", type="primary"):
            try:
                S.store.add(new_cat if category == "➕ New category" else category, question, answer)
                rebuild_engine()
                st.success("FAQ added and the chatbot has been updated.")
            except ValueError as exc:
                st.error(str(exc))
            except OSError as exc:
                st.error(f"Could not save the FAQ file: {exc}")

    st.subheader("🗑️ Delete a FAQ")
    if len(S.store.df):
        target = st.selectbox("Choose a FAQ", S.store.df["question"].tolist())
        if st.button("Delete selected FAQ"):
            try:
                S.store.delete(target)
                rebuild_engine()
                st.success("FAQ deleted.")
                st.rerun()
            except (ValueError, OSError) as exc:
                st.error(str(exc))
    else:
        st.info("No FAQs yet.")

    st.subheader("📋 All FAQs")
    search = st.text_input("Search FAQs")
    df = S.store.df
    if search:
        mask = df.apply(lambda r: search.lower() in " ".join(r.astype(str)).lower(), axis=1)
        df = df[mask]
    st.dataframe(df, hide_index=True)
    st.download_button("⬇ Download CSV", S.store.df.to_csv(index=False), "faqs.csv", "text/csv")
    st.caption("Note: on Streamlit Cloud, changes reset when the app restarts. Commit faqs.csv to keep them.")


def about_page():
    ui.hero("About", "How the chatbot understands your questions.")
    st.markdown("""
**Pipeline**
1. **Preprocessing:** lowercase, remove punctuation and extra spaces, tokenise, map synonyms, remove stop words, light stemming.
2. **TF-IDF:** every FAQ question and answer is turned into a weighted word and bigram vector (scikit-learn `TfidfVectorizer`).
3. **Cosine similarity:** your question is vectorised and compared with every FAQ; score = 80% question similarity + 20% answer similarity.
4. **Decision:** the best FAQ is returned if its score reaches the threshold, otherwise a friendly fallback with related questions.

Built for the CodeAlpha AI Internship (Task 2). No paid APIs or keys are required.
""")


{"💬 Chat": chat_page, "📊 Dashboard": dashboard_page, "🛠️ Admin": admin_page, "ℹ️ About": about_page}[page]()
