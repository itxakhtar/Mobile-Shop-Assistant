import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import sys
import subprocess
import pyttsx3
import threading

try:
    import spacy
    from textblob import TextBlob
except ImportError as e:
    st.error(f"Missing required package: {e}")
    st.stop()

load_dotenv()

def download_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        with st.spinner("Downloading language model..."):
            try:
                subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
                return spacy.load("en_core_web_sm")
            except:
                return None

nlp = download_spacy_model()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

def text_to_speech(text):
    def speak():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 175)
            engine.setProperty('volume', 0.95)
            voices = engine.getProperty('voices')
            for voice in voices:
                if any(x in voice.name.lower() for x in ['english', 'us']):
                    engine.setProperty('voice', voice.id)
                    break
            engine.say(text)
            engine.runAndWait()
        except:
            pass
    threading.Thread(target=speak, daemon=True).start()

st.set_page_config(
    page_title="Lumina • Premium Mobile Shop",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== IMPROVED STYLING ====================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1428 100%);
        color: #e0e7ff;
    }
    
    /* Main Title */
    .main-title {
        font-size: 3.9rem;
        font-weight: 900;
        background: linear-gradient(90deg, #c026d3, #7c3aed, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: -2px;
    }
    
    .subtitle {
        text-align: center;
        color: #c4d0ff;
        font-size: 1.3rem;
        margin-bottom: 2.5rem;
    }

    /* Chat Messages */
    .stChatMessage {
        border-radius: 20px;
        padding: 18px 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .stChatMessage[data-testid="stChatMessage"][role="user"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
    }
    
    .stChatMessage[data-testid="stChatMessage"][role="assistant"] {
        background: rgba(30, 30, 50, 0.9);
        color: #e0e7ff;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #161622 !important;
    }
    
    .sidebar .stButton button {
        width: 100%;
        border-radius: 16px;
        height: 56px;
        font-weight: 600;
        background: #1e1e2e;
        color: #e0e7ff;
        border: 1px solid #4f46e5;
        transition: all 0.4s ease;
    }
    
    .sidebar .stButton button:hover {
        background: #6366f1;
        color: white;
        transform: translateY(-3px);
    }

    /* Chat Input */
    .stChatInput input {
        background-color: #1e1e2e !important;
        color: #e0e7ff !important;
        border: 2px solid #6366f1 !important;
        border-radius: 20px;
    }

    /* Text Elements */
    h1, h2, h3, h4, p, span, div, label {
        color: #e0e7ff !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #1e1e2e !important;
        color: #e0e7ff !important;
    }

    /* Jarvis Status */
    .jarvis-status {
        position: fixed;
        bottom: 25px;
        right: 25px;
        background: rgba(15, 23, 42, 0.95);
        padding: 10px 22px;
        border-radius: 30px;
        font-size: 13.5px;
        border: 1px solid #818cf8;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
        z-index: 1000;
        color: #c4d0ff;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.markdown('<h1 class="main-title">LUMINA</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Premium AI Mobile Shop Assistant • Jarvis Voice Enabled</p>', unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("### ✨ Quick Recommendations")
    
    quick_buttons = {
        "🔥 Best Flagships 2026": "Recommend the best flagship phones right now with detailed specifications",
        "💰 Best Under 50K": "Best smartphones under 50000 PKR with maximum value for money",
        "📸 Camera Kings": "Best camera phones 2026 for photography enthusiasts",
        "⚡ Gaming Phones": "Best gaming phones with best cooling and high refresh rate",
        "🌿 Budget Friendly": "Best phones under 30000 PKR with good performance"
    }
    
    for label, prompt_text in quick_buttons.items():
        if st.button(label, use_container_width=True):
            st.session_state.quick_prompt = prompt_text

    st.divider()
    st.markdown("### 🎙️ Jarvis Voice")
    voice_enabled = st.checkbox("Enable Voice Response", value=True)
    
    st.divider()
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# Rest of your code (NLP + Chat Logic) remains same
# -----------------------------
# ... [Keep all your existing NLP functions, session state, chat logic, etc.] ...

# Just replace your previous styling section with the new one above.

# Status Indicator
st.markdown(f"""
<div class="jarvis-status">
    🟢 Lumina Active • Jarvis Voice {'ON' if voice_enabled else 'OFF'}
</div>
""", unsafe_allow_html=True)
