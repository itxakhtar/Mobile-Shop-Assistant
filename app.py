import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import sys
import subprocess
import threading
import time

# Optional packages with graceful fallback
try:
    import spacy
    from textblob import TextBlob
except ImportError:
    spacy = None
    TextBlob = None

load_dotenv()

# -----------------------------
# Spacy Model Download
# -----------------------------
@st.cache_resource
def load_nlp_model():
    if not spacy:
        return None
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        try:
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
            return spacy.load("en_core_web_sm")
        except:
            return None

nlp = load_nlp_model()

# -----------------------------
# Groq Client
# -----------------------------
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

# -----------------------------
# Text-to-Speech (Disabled by default on cloud)
# -----------------------------
def text_to_speech(text):
    try:
        import pyttsx3
        def speak():
            engine = pyttsx3.init()
            engine.setProperty('rate', 172)
            engine.setProperty('volume', 0.9)
            voices = engine.getProperty('voices')
            for voice in voices:
                if 'english' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            engine.say(text[:500])  # Limit length for performance
            engine.runAndWait()
        threading.Thread(target=speak, daemon=True).start()
    except:
        pass  # TTS not available on Streamlit Cloud

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Lumina • AI Mobile Advisor",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com',
        'Report a bug': 'https://github.com',
    }
)

# -----------------------------
# Premium Futuristic Styling (Glassmorphism + Neon)
# -----------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a0f2e 50%, #0f172a 100%);
        color: #e0e7ff;
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 4.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #c026d3, #7c3aed, #db2777);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: -3px;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.35rem;
        max-width: 680px;
        margin: 0 auto 2.5rem;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    /* Chat Bubbles */
    .stChatMessage {
        border-radius: 22px;
        padding: 18px 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(255,255,255,0.08);
        transition: transform 0.2s ease;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
    }
    
    .stChatMessage[data-testid="stChatMessage"][role="user"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        margin-left: 15%;
    }
    
    .stChatMessage[data-testid="stChatMessage"][role="assistant"] {
        background: rgba(30, 27, 55, 0.85);
        color: #e0e7ff;
        margin-right: 15%;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 15, 30, 0.95) !important;
        backdrop-filter: blur(16px);
    }
    
    .sidebar .stButton button {
        border-radius: 16px;
        height: 52px;
        font-weight: 600;
        background: rgba(30, 30, 50, 0.8);
        border: 1px solid #6366f1;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .sidebar .stButton button:hover {
        background: #6366f1;
        transform: scale(1.03);
        color: white;
    }

    /* Input */
    .stChatInput input {
        background: rgba(30, 30, 50, 0.9) !important;
        color: #e0e7ff !important;
        border: 2px solid #6366f1 !important;
        border-radius: 9999px;
        padding: 16px 24px;
        font-size: 1.05rem;
    }

    /* Status */
    .status-bar {
        position: fixed;
        bottom: 24px;
        right: 24px;
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(12px);
        padding: 10px 20px;
        border-radius: 50px;
        border: 1px solid #6366f1;
        font-size: 0.9rem;
        z-index: 1000;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
    }

    h1, h2, h3, label {
        color: #e0e7ff !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Helper Functions
# -----------------------------
def analyze_sentiment(text):
    if not TextBlob:
        return "neutral"
    try:
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.2: return "positive"
        elif polarity < -0.2: return "negative"
        return "neutral"
    except:
        return "neutral"

def detect_intent(text):
    text = text.lower()
    if any(w in text for w in ["hi", "hello", "hey"]):
        return "greeting"
    elif any(w in text for w in ["price", "cost", "how much"]):
        return "price_inquiry"
    elif any(w in text for w in ["spec", "specification", "features"]):
        return "specification_request"
    elif any(w in text for w in ["recommend", "best", "suggest"]):
        return "recommendation"
    elif any(w in text for w in ["compare", "vs", "versus"]):
        return "comparison"
    return "general_query"

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! I'm Lumina — your intelligent AI mobile advisor. How can I help you discover the perfect smartphone today?"
    }]

# -----------------------------
# Hero Header
# -----------------------------
col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    st.markdown('<h1 class="main-title">LUMINA</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Futuristic AI Mobile Advisor • Powered by Groq • Jarvis Intelligence</p>', unsafe_allow_html=True)

# Quick Action Pills
st.markdown("### Popular Searches")
pill_cols = st.columns(5)
quick_prompts = [
    ("🔥 Top Flagships", "Recommend the best flagship phones 2026"),
    ("💰 Under 50K", "Best phones under 50000 PKR"),
    ("📸 Camera Kings", "Best camera phones for photography"),
    ("⚡ Gaming", "Best gaming phones with high refresh rate"),
    ("🌟 Value Picks", "Best value for money smartphones")
]

for i, (label, prompt) in enumerate(quick_prompts):
    with pill_cols[i]:
        if st.button(label, use_container_width=True, key=f"pill_{i}"):
            st.session_state.quick_prompt = prompt

st.divider()

# -----------------------------
# Main Chat Area
# -----------------------------
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# -----------------------------
# Sidebar - Premium Navigation
# -----------------------------
with st.sidebar:
    st.markdown("### ✨ Explore")
    
    st.button("🏠 Home", use_container_width=True)
    st.button("📱 All Phones", use_container_width=True)
    st.button("🔍 Compare Phones", use_container_width=True)
    st.button("📸 Camera Hub", use_container_width=True)
    st.button("🎮 Gaming Zone", use_container_width=True)
    
    st.divider()
    st.markdown("### 🎙️ Voice Settings")
    voice_enabled = st.toggle("Enable Jarvis Voice", value=False)  # Default off for cloud
    
    st.divider()
    if st.button("🗑️ Clear Conversation", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Lumina v2.1 • Premium AI Experience")

# -----------------------------
# Chat Input
# -----------------------------
prompt = st.chat_input("Ask about any smartphone...")

if "quick_prompt" in st.session_state and st.session_state.quick_prompt:
    prompt = st.session_state.quick_prompt
    del st.session_state.quick_prompt

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)

    # NLP Insights
    sentiment = analyze_sentiment(prompt)
    intent = detect_intent(prompt)

    system_prompt = f"""You are Lumina, a premium, witty, and highly knowledgeable AI mobile advisor with a Jarvis-like personality.
    Speak elegantly and professionally. Use emojis tastefully.
    Current user sentiment: {sentiment}
    Detected intent: {intent}
    Always include key specifications and current price ranges in PKR when recommending phones.
    """

    with chat_container:
        with st.chat_message("assistant"):
            if not client:
                full_response = "⚠️ Groq API key is missing. Please configure it in your .env file."
                st.error(full_response)
            else:
                with st.spinner("Lumina is thinking..."):
                    try:
                        stream = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
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
                        
                        if voice_enabled:
                            text_to_speech(full_response)
                            
                    except Exception as e:
                        full_response = f"Error: {str(e)}"
                        st.error(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()

# -----------------------------
# Status Bar
# -----------------------------
st.markdown(f"""
<div class="status-bar">
    🟢 Lumina Online • Groq Powered • Voice: {'ON' if voice_enabled else 'OFF'}
</div>
""", unsafe_allow_html=True)
