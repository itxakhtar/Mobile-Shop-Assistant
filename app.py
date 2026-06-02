import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import spacy
from textblob import TextBlob
import pyttsx3
import threading

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Load NLP Model
# -----------------------------
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.error("Spacy model not found. Run: `python -m spacy download en_core_web_sm`")
    nlp = None

# -----------------------------
# Groq Client
# -----------------------------
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

# -----------------------------
# Text-to-Speech Function (Jarvis Style)
# -----------------------------
def text_to_speech(text):
    """Convert text to speech using pyttsx3"""
    def speak():
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)  # Speed of speech
        engine.setProperty('volume', 0.9)  # Volume (0-1)
        
        # Set voice to a more natural one if available
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'english' in voice.name.lower() or 'us' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        engine.say(text)
        engine.runAndWait()
    
    # Run in a separate thread to not block the UI
    threading.Thread(target=speak, daemon=True).start()

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Lumina • Mobile Shop",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom Styling - Jarvis Theme
# -----------------------------
st.markdown("""
<style>
    /* Solid Dark Block Background */
    .stApp {
        background-color: #0a0a0f !important;
        color: #ffffff !important;
    }
    
    /* Ensure all text is white */
    .stMarkdown, .stTextInput, .stSelectbox, .stButton, p, h1, h2, h3, h4, h5, h6, span, div {
        color: #ffffff !important;
    }

    /* Chat Messages */
    .stChatMessage {
        border-radius: 18px;
        padding: 16px 20px;
        margin-bottom: 16px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    }
    
    .stChatMessage.user {
        background: linear-gradient(90deg, #6b46c1, #7c3aed);
        color: white;
        border-bottom-right-radius: 4px;
    }
    
    .stChatMessage.assistant {
        background: #16161f;
        border: 1px solid #2a2a3a;
        border-bottom-left-radius: 4px;
    }

    /* Title */
    .main-title {
        font-size: 3.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #c084fc, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.4rem;
    }
    
    .subtitle {
        text-align: center;
        color: #b3b3cc;
        font-size: 1.15rem;
        margin-bottom: 2.2rem;
    }

    /* Sidebar */
    .sidebar .stButton button {
        width: 100%;
        border-radius: 12px;
        height: 52px;
        font-weight: 600;
        background-color: #1f1f2e;
        color: white;
        transition: all 0.3s ease;
    }
    
    .sidebar .stButton button:hover {
        background-color: #7c3aed;
        transform: translateY(-2px);
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #1a1a24 !important;
        color: white !important;
    }
    
    /* Jarvis Status Indicator */
    .jarvis-status {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #1f1f2e;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 12px;
        border-left: 3px solid #7c3aed;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown('<h1 class="main-title">LUMINA</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Premium AI Mobile Shop Assistant • Jarvis Voice Enabled</p>', unsafe_allow_html=True)

# -----------------------------
# Sidebar - Quick Actions
# -----------------------------
with st.sidebar:
    st.markdown("### ✨ Quick Recommendations")
    
    if st.button("🔥 Best Flagships 2026", use_container_width=True):
        st.session_state.quick_prompt = "Recommend the best flagship phones right now"
    if st.button("💰 Best Under 50K", use_container_width=True):
        st.session_state.quick_prompt = "Best smartphones under 50000 PKR"
    if st.button("📸 Camera Kings", use_container_width=True):
        st.session_state.quick_prompt = "Best camera phones 2026"
    if st.button("⚡ Gaming Phones", use_container_width=True):
        st.session_state.quick_prompt = "Best gaming phones right now"
    if st.button("🌿 Budget Friendly", use_container_width=True):
        st.session_state.quick_prompt = "Best phones under 30000 PKR"

    st.divider()
    
    # Voice settings
    st.markdown("### 🎙️ Jarvis Voice")
    voice_enabled = st.checkbox("Enable Voice Response", value=True)
    st.caption("Lumina will speak responses like Jarvis")
    
    st.divider()
    st.caption("Made with ❤️ for mobile lovers")

# -----------------------------
# NLP Functions
# -----------------------------
def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.2: return "positive"
    elif polarity < -0.2: return "negative"
    return "neutral"

def extract_entities(text):
    if nlp is None: return []
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def detect_intent(text):
    text = text.lower()
    if any(word in text for word in ["hi", "hello", "hey"]): return "greeting"
    elif any(word in text for word in ["price", "cost", "rate"]): return "price_inquiry"
    elif any(word in text for word in ["spec", "specification"]): return "specification_request"
    elif any(word in text for word in ["recommend", "best", "suggest"]): return "recommendation"
    elif any(word in text for word in ["compare", "vs", "versus"]): return "comparison"
    elif any(word in text for word in ["bye", "thank"]): return "farewell"
    return "general_query"

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_response" not in st.session_state:
    st.session_state.last_response = ""

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

if prompt or ("quick_prompt" in st.session_state and st.session_state.quick_prompt):
    if "quick_prompt" in st.session_state:
        prompt = st.session_state.quick_prompt
        del st.session_state.quick_prompt

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

    Be elegant, professional, and helpful like Jarvis from Iron Man. Use emojis tastefully.
    When comparing phones, use beautiful markdown tables.
    Always mention key specs: Processor, RAM, Storage, Display, Camera, Battery.
    Keep responses conversational but informative.
    """

    with st.chat_message("assistant"):
        if not client:
            st.error("Groq API key not found!")
            full_response = "I'm currently unable to connect. Please check API configuration."
        else:
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
                
                # Jarvis Voice Response
                if voice_enabled and full_response:
                    with st.spinner("🎙️ Lumina is speaking..."):
                        text_to_speech(full_response)
                        st.session_state.last_response = full_response

            except Exception as e:
                full_response = f"⚠️ Sorry, something went wrong: {str(e)}"
                st.error(full_response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response,
        "nlp_insights": nlp_insights
    })

    st.rerun()

# Jarvis Status Indicator
st.markdown(f"""
<div class="jarvis-status">
    🟢 Jarvis Active | Voice {'ON' if voice_enabled else 'OFF'}
</div>
""", unsafe_allow_html=True)