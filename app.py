 import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import sys
import subprocess

# Try to import spacy, install if not available
try:
    import spacy
    from textblob import TextBlob
except ImportError as e:
    st.error(f"Missing required package: {e}")
    st.info("Please install required packages: `pip install spacy textblob`")
    st.stop()

import pyttsx3
import threading

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Download spacy model if not present
# -----------------------------
def download_spacy_model():
    """Download spacy model if not available"""
    try:
        nlp = spacy.load("en_core_web_sm")
        return nlp
    except OSError:
        with st.spinner("Downloading language model... This may take a moment."):
            try:
                subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
                nlp = spacy.load("en_core_web_sm")
                st.success("Language model downloaded successfully!")
                return nlp
            except Exception as e:
                st.error(f"Failed to download spacy model: {e}")
                st.info("Run this command manually: `python -m spacy download en_core_web_sm`")
                return None

# Load NLP Model
nlp = download_spacy_model()

# -----------------------------
# Groq Client
# -----------------------------
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY not found in environment variables!")
    st.info("Please add your GROQ_API_KEY to the .env file")
    client = None
else:
    client = Groq(api_key=api_key)

# -----------------------------
# Text-to-Speech Function (Jarvis Style)
# -----------------------------
def text_to_speech(text):
    """Convert text to speech using pyttsx3"""
    def speak():
        try:
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
            engine.stop()
        except Exception as e:
            st.warning(f"Voice synthesis failed: {str(e)}")
    
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
    
    /* User messages */
    [data-testid="stChatMessage"]:has(.user) {
        background: linear-gradient(90deg, #6b46c1, #7c3aed);
        color: white;
        border-bottom-right-radius: 4px;
    }
    
    /* Assistant messages */
    [data-testid="stChatMessage"]:has(.assistant) {
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
        border: none;
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
        z-index: 999;
    }
    
    /* Chat input styling */
    .stChatInput input {
        background-color: #1a1a24 !important;
        color: white !important;
        border: 1px solid #2a2a3a !important;
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
        st.session_state.quick_prompt = "Recommend the best flagship phones right now with detailed specifications"
    if st.button("💰 Best Under 50K", use_container_width=True):
        st.session_state.quick_prompt = "Best smartphones under 50000 PKR with value for money"
    if st.button("📸 Camera Kings", use_container_width=True):
        st.session_state.quick_prompt = "Best camera phones 2026 for photography enthusiasts"
    if st.button("⚡ Gaming Phones", use_container_width=True):
        st.session_state.quick_prompt = "Best gaming phones right now with cooling systems and high refresh rate"
    if st.button("🌿 Budget Friendly", use_container_width=True):
        st.session_state.quick_prompt = "Best phones under 30000 PKR with good performance"

    st.divider()
    
    # Voice settings
    st.markdown("### 🎙️ Jarvis Voice")
    voice_enabled = st.checkbox("Enable Voice Response", value=True)
    st.caption("Lumina will speak responses like Jarvis")
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.caption("Made with ❤️ for mobile lovers")

# -----------------------------
# NLP Functions
# -----------------------------
def analyze_sentiment(text):
    try:
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.2: return "positive"
        elif polarity < -0.2: return "negative"
        return "neutral"
    except:
        return "neutral"

def extract_entities(text):
    if nlp is None: return []
    try:
        doc = nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]
    except:
        return []

def detect_intent(text):
    text = text.lower()
    if any(word in text for word in ["hi", "hello", "hey", "greetings"]): return "greeting"
    elif any(word in text for word in ["price", "cost", "rate", "how much"]): return "price_inquiry"
    elif any(word in text for word in ["spec", "specification", "features", "details"]): return "specification_request"
    elif any(word in text for word in ["recommend", "best", "suggest", "top", "good"]): return "recommendation"
    elif any(word in text for word in ["compare", "vs", "versus", "difference"]): return "comparison"
    elif any(word in text for word in ["bye", "thank", "thanks", "goodbye"]): return "farewell"
    return "general_query"

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    # Add welcome message
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! I'm Lumina, your AI mobile shop assistant. How can I help you find the perfect smartphone today? 📱✨",
        "nlp_insights": {
            "sentiment": "positive",
            "intent": "greeting",
            "entities": []
        }
    }]

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

# Handle quick prompts
if "quick_prompt" in st.session_state and st.session_state.quick_prompt:
    prompt = st.session_state.quick_prompt
    del st.session_state.quick_prompt

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

    system_prompt = f"""You are Lumina, a premium and knowledgeable mobile shop assistant with Jarvis-like personality from Iron Man.
    Current Sentiment: {sentiment}
    Detected Intent: {intent}

    Guidelines:
    - Be elegant, professional, and helpful like Jarvis
    - Use emojis tastefully (📱, 🔥, 💰, ⚡, 📸)
    - When comparing phones, use beautiful markdown tables with proper formatting
    - Always mention key specs: Processor, RAM, Storage, Display, Camera, Battery
    - Keep responses conversational but informative (200-400 words max)
    - For greetings, be warm and enthusiastic
    - For farewells, end politely and offer future assistance
    - Provide specific model recommendations when asked
    - Include price ranges in PKR when relevant
    - Never recommend phones outside the user's budget range
    """

    with st.chat_message("assistant"):
        if not client:
            st.error("Groq API key not found! Please check your .env file.")
            full_response = "⚠️ I'm currently unable to connect. Please check the API configuration and try again."
        else:
            try:
                # Show typing indicator
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
st.markdown(f"""
<div class="jarvis-status">
    🟢 Jarvis Active | Voice {'ON' if voice_enabled else 'OFF'}
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Requirements.txt content for deployment
# -----------------------------
requirements_text = """
streamlit
groq
python-dotenv
spacy
textblob
pyttsx3
"""

# Note: For deployment, create a requirements.txt file with the above packages
# Also run: python -m spacy download en_core_web_sm
