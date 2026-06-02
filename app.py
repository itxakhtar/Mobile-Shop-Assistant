import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from textblob import TextBlob

load_dotenv()

# ====================== GROQ CLIENT ======================
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="Lumina • AI Mobile Advisor",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ====================== PREMIUM RESPONSIVE STYLING ======================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');

    .stApp {
        background: #0F172A;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }

    /* Hero Title */
    .main-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 4.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #3B82F6, #8B5CF6, #22D3EE);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: -2px;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        text-align: center;
        color: #94A3B8;
        font-size: 1.35rem;
        max-width: 720px;
        margin: 0 auto 2rem;
    }

    /* Glassmorphism */
    .glass-card {
        background: rgba(51, 65, 85, 0.65);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.35);
    }

    /* Chat Messages */
    .stChatMessage {
        border-radius: 20px;
        padding: 18px 24px;
        margin-bottom: 18px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }

    .stChatMessage:hover {
        transform: translateY(-3px);
    }

    .stChatMessage[data-testid="stChatMessage"][role="user"] {
        background: linear-gradient(135deg, #3B82F6, #6366F1) !important;
        color: #FFFFFF !important;
        margin-left: 10%;
    }

    .stChatMessage[data-testid="stChatMessage"][role="assistant"] {
        background: #1E293B !important;
        color: #E2E8F0 !important;
        margin-right: 10%;
    }

    /* Sidebar Navigation */
    section[data-testid="stSidebar"] {
        background: #1E293B !important;
    }

    .nav-item {
        background: #334155;
        border-radius: 16px;
        padding: 14px 18px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 1px solid rgba(148, 163, 184, 0.15);
        color: #E2E8F0 !important;
        font-weight: 500;
    }

    .nav-item:hover {
        background: linear-gradient(90deg, #3B82F6, #8B5CF6);
        color: #FFFFFF !important;
        transform: translateX(8px);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
    }

    /* Popular Searches */
    .popular-card {
        background: #334155;
        border-radius: 18px;
        padding: 16px 20px;
        text-align: center;
        border: 1px solid #475569;
        transition: all 0.3s ease;
        height: 100%;
        color: #E2E8F0 !important;
    }

    .popular-card:hover {
        background: linear-gradient(135deg, #3B82F6, #8B5CF6);
        color: #FFFFFF !important;
        transform: translateY(-6px);
        border-color: #3B82F6;
    }

    /* Buttons */
    .stButton button {
        border-radius: 16px;
        height: 52px;
        font-weight: 600;
        transition: all 0.3s ease;
        color: #FFFFFF !important;
    }

    .stButton button:hover {
        transform: scale(1.04);
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
    }

    /* Input */
    .stChatInput input {
        background: #1E293B !important;
        color: #FFFFFF !important;
        border: 2px solid #3B82F6 !important;
        border-radius: 9999px;
        padding: 16px 24px;
    }

    .stChatInput input::placeholder {
        color: #94A3B8 !important;
    }

    /* Responsive Adjustments */
    @media (max-width: 768px) {
        .main-title { font-size: 2.8rem !important; letter-spacing: -1px; }
        .subtitle { font-size: 1.1rem !important; }
        .stChatMessage { margin-left: 0 !important; margin-right: 0 !important; }
        .pill_cols { flex-direction: column; }
    }

    @media (max-width: 480px) {
        .main-title { font-size: 2.4rem !important; }
    }

    /* High Contrast Fixes */
    h1, h2, h3, label, p, span, div {
        color: #FFFFFF !important;
    }

    .stMarkdown, .stMarkdown p, .stMarkdown li {
        color: #E2E8F0 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ====================== HELPERS ======================
def analyze_sentiment(text):
    try:
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.2: return "positive"
        elif polarity < -0.2: return "negative"
        return "neutral"
    except:
        return "neutral"

def detect_intent(text):
    text = text.lower()
    if any(w in text for w in ["hi", "hello", "hey", "assalam"]):
        return "greeting"
    elif any(w in text for w in ["price", "cost", "how much", "rate"]):
        return "price_inquiry"
    elif any(w in text for w in ["spec", "specification", "features", "detail"]):
        return "specification_request"
    elif any(w in text for w in ["recommend", "best", "suggest", "good"]):
        return "recommendation"
    elif any(w in text for w in ["compare", "vs", "versus"]):
        return "comparison"
    return "general_query"

# ====================== SESSION STATE ======================
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! I'm **Lumina** — your intelligent AI mobile advisor. How can I help you find the perfect smartphone today? 📱"
    }]

# ====================== HERO ======================
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.markdown('<h1 class="main-title">LUMINA</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Premium AI Mobile Advisor • Powered by Groq • Real-time Intelligence</p>', unsafe_allow_html=True)

# ====================== POPULAR SEARCHES (Modern Cards) ======================
st.markdown("### Popular Searches")
cols = st.columns(5)

quick_prompts = [
    ("🔥 Top Flagships", "Recommend the best flagship phones in 2026 with detailed specs"),
    ("💰 Under 50K", "Best smartphones under 50000 PKR with best value"),
    ("📸 Camera Kings", "Best camera phones for photography in Pakistan"),
    ("⚡ Gaming Beast", "Best gaming phones with high refresh rate & cooling"),
    ("🌟 Value Picks", "Best value for money smartphones under 100K PKR")
]

for i, (label, prompt) in enumerate(quick_prompts):
    with cols[i]:
        if st.button(label, key=f"pill_{i}", use_container_width=True):
            st.session_state.quick_prompt = prompt

st.divider()

# ====================== CHAT ======================
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ====================== SIDEBAR - Modern Navigation Cards ======================
with st.sidebar:
    st.markdown("### Navigation")
    
    nav_items = [
        ("🏠 Home", "home"),
        ("📱 All Smartphones", "phones"),
        ("🔍 Compare Phones", "compare"),
        ("📸 Camera Hub", "camera"),
        ("🎮 Gaming Zone", "gaming"),
        ("💎 Premium Picks", "premium")
    ]
    
    for label, key in nav_items:
        st.markdown(f"""
            <div class="nav-item" onclick="window.location.reload();">
                {label}
            </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Settings")
    st.checkbox("🔊 Enable Voice Response", value=False)
    st.caption("Lumina v2.3 • Premium SaaS Experience")

# ====================== CHAT INPUT ======================
prompt = st.chat_input("Ask anything about smartphones...")

if "quick_prompt" in st.session_state and st.session_state.quick_prompt:
    prompt = st.session_state.quick_prompt
    del st.session_state.quick_prompt

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)

    sentiment = analyze_sentiment(prompt)
    intent = detect_intent(prompt)

    system_prompt = f"""You are Lumina, a premium witty AI mobile advisor.
    Speak elegantly. Use emojis tastefully.
    Sentiment: {sentiment} | Intent: {intent}
    Always include key specs and current prices in PKR.
    Use markdown tables for comparisons."""

    with chat_container:
        with st.chat_message("assistant"):
            if not client:
                st.error("⚠️ Groq API key missing.")
                full_response = "Please configure your API key."
            else:
                with st.spinner("Lumina is thinking..."):
                    try:
                        stream = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.75,
                            max_tokens=1024,
                            stream=True
                        )
                        response_placeholder = st.empty()
                        full_response = ""
                        for chunk in stream:
                            if chunk.choices[0].delta.content:
                                full_response += chunk.choices[0].delta.content
                                response_placeholder.markdown(full_response + "▌")
                        response_placeholder.markdown(full_response)
                    except Exception as e:
                        full_response = f"Error: {str(e)}"
                        st.error(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()
