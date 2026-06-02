import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import sys
import subprocess
import pyttsx3
import threading

# Try to import spacy and textblob
try:
    import spacy
    from textblob import TextBlob
except ImportError as e:
    st.error(f"Missing required package: {e}")
    st.info("Please install required packages: `pip install spacy textblob`")
    st.stop()

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Download spacy model if not present
# -----------------------------
def download_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        with st.spinner("Downloading language model... This may take a moment."):
            try:
                subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
                st.success("Language model downloaded successfully!")
                return spacy.load("en_core_web_sm")
            except Exception as e:
                st.error(f"Failed to download spacy model: {e}")
                st.info("Run: `python -m spacy download en_core_web_sm`")
                return None

nlp = download_spacy_model()

# -----------------------------
# Groq Client
# -----------------------------
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

# -----------------------------
# Text-to-Speech (Jarvis Style)
# -----------------------------
def text_to_speech(text):
    def speak():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 175)
            engine.setProperty('volume', 0.95)
            
            voices = engine.getProperty('voices')
            for voice in voices:
                if any(x in voice.name.lower() for x in ['english', 'us', 'david']):
                    engine.setProperty('voice', voice.id)
                    break
            
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            st.warning(f"Voice synthesis failed: {str(e)}")
    
    threading.Thread(target=speak, daemon=True).start()

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Lumina • Premium Mobile Shop",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Enhanced Styling - Premium Graphic Design
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1428 100%);
        color: #ffffff;
    }
    
    /* Main Title */
    .main-title {
        font-size: 3.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #c026d3, #7c3aed, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.3rem;
        letter-spacing: -2px;
    }
    
    .subtitle {
        text-align: center;
        color: #a5b4fc;
        font-size: 1.25rem;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }

    /* Chat Messages - Glassmorphism */
    .stChatMessage {
        border-radius: 20px;
        padding: 18px 22px;
        margin-bottom: 18px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(12px);
    }
    
    .stChatMessage[data-testid="stChatMessage"][role="user"] {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
    }
    
    .stChatMessage[data-testid="stChatMessage"][role="assistant"] {
        background: rgba(30, 30, 46, 0.85);
    }

    /* Sidebar */
    .sidebar .stButton button {
        width: 100%;
        border-radius: 16px;
        height: 54px;
        font-weight: 600;
        background: linear-gradient(90deg, #1f1f2e, #312e81);
        color: white;
        border: none;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .sidebar .stButton button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 25px rgba(124, 58, 237, 0.4);
        background: linear-gradient(90deg, #6d28d9, #4f46e5);
    }

    /* Input */
    .stChatInput input {
        background-color: #1a1730 !important;
        color: white !important;
        border: 2px solid #4338ca !important;
        border-radius: 20px;
        padding: 14px 20px;
    }

    /* Status Indicator */
    .jarvis-status {
        position: fixed;
        bottom: 25px;
        right: 25px;
        background: rgba(15, 23, 42, 0.95);
        padding: 10px 20px;
        border-radius: 30px;
        font-size: 13px;
        border: 1px solid #6366f1;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        z-index: 1000;
        font-family: 'Courier New', monospace;
    }

    h1, h2, h3 {
        color: #e0e7ff;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.markdown('<h1 class="main-title">LUMINA</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Premium AI Mobile Experience • Powered by Jarvis Intelligence</p>', unsafe_allow_html=True)

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
    st.caption("Lumina speaks with elegant Jarvis personality")
    
    st.divider()
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption("Designed with ❤️ for mobile enthusiasts")

# -----------------------------
# NLP Functions
# -----------------------------
def analyze_sentiment(text):
    try:
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.2:
            return "positive"
        elif polarity < -0.2:
            return "negative"
        return "neutral"
    except:
        return "neutral"

def extract_entities(text):
    if nlp is None:
        return []
    try:
        doc = nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]
    except:
        return []

def detect_intent(text):
    text = text.lower()
    if any(word in text for word in ["hi", "hello", "hey"]):
        return "greeting"
    elif any(word in text for word in ["price", "cost", "rate"]):
        return "price_inquiry"
    elif any(word in text for word in ["spec", "specification", "features"]):
        return "specification_request"
    elif any(word in text for word in ["recommend", "best", "suggest"]):
        return "recommendation"
    elif any(word in text for word in ["compare", "vs", "versus"]):
        return "comparison"
    elif any(word in text for word in ["bye", "thank", "goodbye"]):
        return "farewell"
    return "general_query"

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! I'm Lumina, your personal premium mobile assistant. How may I help you find your perfect smartphone today? 📱✨",
        "nlp_insights": {"sentiment": "positive", "intent": "greeting", "entities": []}
    }]

if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = ""

# -----------------------------
# Display Chat History
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "nlp_insights" in msg:
            with st.expander("🔍 Analysis", expanded=False):
                st.json(msg["nlp_insights"])

# -----------------------------
# Chat Input & Logic
# -----------------------------
prompt = st.chat_input("Ask anything about smartphones... (Lumina will respond with voice)")

# Handle quick prompts
if st.session_state.quick_prompt:
    prompt = st.session_state.quick_prompt
    st.session_state.quick_prompt = ""

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # NLP Analysis
    sentiment = analyze_sentiment(prompt)
    entities = extract_entities(prompt)
    intent = detect_intent(prompt)

    nlp_insights = {
        "sentiment": sentiment,
        "intent": intent,
        "entities": [{"text": e[0], "label": e[1]} for e in entities]
    }

    system_prompt = f"""You are Lumina, a premium and knowledgeable mobile shop assistant with Jarvis-like personality.
    Current Sentiment: {sentiment}
    Detected Intent: {intent}

    Guidelines:
    - Be elegant, professional, and helpful like Jarvis from Iron Man
    - Use emojis tastefully (📱, 🔥, 💰, ⚡, 📸)
    - When comparing phones, use beautiful markdown tables
    - Always mention key specs: Processor, RAM, Storage, Display, Camera, Battery
    - Keep responses conversational but informative
    - Be friendly and enthusiastic for greetings
    - For farewells, end politely
    """

    with st.chat_message("assistant"):
        if not client:
            st.error("Groq API key not found! Please add it to .env file")
            full_response = "⚠️ I need a valid Groq API key to work. Please check your configuration."
        else:
            try:
                with st.spinner("Lumina is thinking..."):
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
                    
                    # Jarvis Voice Response
                    if voice_enabled and full_response and len(full_response) > 10:
                        text_to_speech(full_response)

            except Exception as e:
                full_response = f"⚠️ I encountered an error: {str(e)}"
                st.error(full_response)

    # Add assistant message to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response,
        "nlp_insights": nlp_insights
    })

    st.rerun()

# Jarvis Status Indicator
status_text = "🟢 Jarvis Active"
if not client:
    status_text = "🔴 API Missing"
elif voice_enabled:
    status_text = "🟢 Jarvis Active | Voice ON"
else:
    status_text = "🟡 Jarvis Active | Voice OFF"

st.markdown(f"""
<div class="jarvis-status">
    {status_text}
</div>
""", unsafe_allow_html=True)
