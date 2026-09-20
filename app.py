import os
import streamlit as st
from rag import FitnessRetriever
from llm import stream_answer, generate_answer

# Reads from Streamlit secrets first (used on Streamlit Cloud), then falls
# back to a local environment variable. Never hardcode the key here.
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except Exception:
    HF_TOKEN = os.environ.get("HF_TOKEN", "")

st.set_page_config(page_title="Coach — Fitness RAG Chat", page_icon="🏋️", layout="centered")

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp { background-color: #14171A; }
    section[data-testid="stSidebar"] { background-color: #1A1D20; border-right: 1px solid #2C3135; }
    h1, h2, h3 { color: #F3F1EC; }

    /* Header banner */
    .coach-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 18px 22px;
        margin-bottom: 18px;
        background: linear-gradient(135deg, #1D2124 0%, #23282c 100%);
        border: 1px solid #2C3135;
        border-radius: 10px;
    }
    .coach-header-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #F3F1EC;
        margin: 0;
    }
    .coach-header-sub {
        font-size: 0.82rem;
        color: #8A8F94;
        margin-top: 2px;
    }
    .coach-badge {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        padding: 5px 12px;
        border-radius: 999px;
        white-space: nowrap;
    }
    .coach-badge-live {
        background: rgba(213, 255, 61, 0.14);
        color: #D5FF3D;
        border: 1px solid rgba(213, 255, 61, 0.35);
    }
    .coach-badge-local {
        background: rgba(138, 143, 148, 0.14);
        color: #B8BCC0;
        border: 1px solid rgba(138, 143, 148, 0.3);
    }

    /* Chat bubbles */
    div[data-testid="stChatMessage"] {
        background-color: #1D2124;
        border: 1px solid #2C3135;
        border-radius: 12px;
        padding: 4px 6px;
        margin-bottom: 6px;
    }

    /* Sidebar quick-prompt buttons */
    section[data-testid="stSidebar"] button {
        border-radius: 8px !important;
        text-align: left !important;
        font-size: 0.85rem !important;
    }

    /* Sidebar section labels */
    .coach-sidebar-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        color: #8A8F94;
        text-transform: uppercase;
        margin: 14px 0 6px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
badge_class = "coach-badge-live" if HF_TOKEN else "coach-badge-local"
badge_text = "⚡ Llama 3.1 8B live" if HF_TOKEN else "📚 Knowledge base only"

st.markdown(
    f"""
    <div class="coach-header">
        <div>
            <p class="coach-header-title">🏋️ Coach</p>
            <p class="coach-header-sub">Fitness Q&A · splits, form, nutrition, recovery</p>
        </div>
        <div class="coach-badge {badge_class}">{badge_text}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Retriever (cached across reruns)
# ---------------------------------------------------------------------------
@st.cache_resource
def get_retriever():
    return FitnessRetriever()


retriever = get_retriever()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🏋️ Coach")
    st.caption("Ask a question or tap a prompt below to get started.")

    st.markdown('<p class="coach-sidebar-label">Workouts</p>', unsafe_allow_html=True)
    for ex in ["Build me a 4-day split", "20 minute workout no equipment", "Beginner full-body plan"]:
        if st.button(ex, use_container_width=True, key=f"wo-{ex}"):
            st.session_state.pending_input = ex

    st.markdown('<p class="coach-sidebar-label">Form &amp; technique</p>', unsafe_allow_html=True)
    for ex in ["How do I fix my squat depth?", "Deadlift form check", "Why does my shoulder hurt benching?"]:
        if st.button(ex, use_container_width=True, key=f"form-{ex}"):
            st.session_state.pending_input = ex

    st.markdown('<p class="coach-sidebar-label">Nutrition &amp; recovery</p>', unsafe_allow_html=True)
    for ex in ["How much protein do I need?", "My lower back hurts after deadlifts", "How do I stay motivated?"]:
        if st.button(ex, use_container_width=True, key=f"nut-{ex}"):
            st.session_state.pending_input = ex

    st.divider()

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption(
        "Not medical advice. For pain, injuries, or medical conditions, "
        "consult a doctor or physical therapist."
    )

# ---------------------------------------------------------------------------
# Chat history
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

AVATARS = {"user": "🙋", "assistant": "🏋️"}

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=AVATARS.get(msg["role"])):
        st.markdown(msg["content"])

if not st.session_state.messages:
    st.info("👋 Tap a prompt in the sidebar, or type your own question below.")

user_input = st.chat_input("Ask about workouts, form, nutrition, recovery...")

# Support sidebar example buttons triggering a message too
if "pending_input" in st.session_state:
    user_input = st.session_state.pop("pending_input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar=AVATARS["user"]):
        st.markdown(user_input)

    if HF_TOKEN:
        matches = retriever.query(user_input, top_k=3)
        context = [m.answer for m in matches]
        gen = stream_answer(HF_TOKEN, user_input, context)

        # Peek at the first chunk: if the connection failed outright, our
        # generator yields exactly one "[LLM error]" chunk and stops -
        # catch that case before rendering anything, so we can fall back
        # cleanly instead of streaming an error message to the user.
        first_chunk = next(gen, None)

        if first_chunk is not None and first_chunk.startswith("[LLM error]"):
            reply = retriever.answer(user_input) + f"\n\n*(Model unavailable: {first_chunk})*"
            with st.chat_message("assistant", avatar=AVATARS["assistant"]):
                st.markdown(reply)
        else:
            def _combined():
                if first_chunk:
                    yield first_chunk
                yield from gen

            with st.chat_message("assistant", avatar=AVATARS["assistant"]):
                reply = st.write_stream(_combined())
    else:
        reply = retriever.answer(user_input)
        with st.chat_message("assistant", avatar=AVATARS["assistant"]):
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})