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

# ====================== PREMIUM STYLING ======================
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
        font-size: 4.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #3B82F6, #8B5CF6, #22D3EE);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: -3px;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        text-align: center;
        color: #94A3B8;
        font-size: 1.4rem;
        max-width: 700px;
        margin: 0 auto 2rem;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(51, 65, 85, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
    }

    /* Chat Messages */
    .stChatMessage {
        border-radius: 20px;
        padding: 18px 24px;
        margin-bottom: 18px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(148, 163, 184, 0.1);
        transition: all 0.3s ease;
    }

    .stChatMessage:hover {
        transform: translateY(-3px);
    }

    /* User messages */
    [data-testid="stChatMessage"]:has(div[data-testid="stChatMessageContent"]) {
        background: linear-gradient(135deg, #3B82F6, #6366F1) !important;
        color: white !important;
        margin-left: 12%;
    }

    /* Assistant messages container */
    [data-testid="stChatMessage"]:has(div[data-testid="stChatMessageContent"]) + div {
        background: #1E293B !important;
        color: #E2E8F0 !important;
        margin-right: 12%;
    }
    
    /* Force white text for ALL chat content */
    [data-testid="stChatMessage"] {
        color: #FFFFFF !important;
    }
    
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] div,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] td,
    [data-testid="stChatMessage"] th,
    [data-testid="stChatMessage"] strong,
    [data-testid="stChatMessage"] em {
        color: #FFFFFF !important;
    }
    
    /* Blue accent for assistant responses - specific links and highlights */
    [data-testid="stChatMessage"]:has(div[data-testid="stChatMessageContent"]) a,
    [data-testid="stChatMessage"]:has(div[data-testid="stChatMessageContent"]) strong,
    [data-testid="stChatMessage"]:has(div[data-testid="stChatMessageContent"]) em {
        color: #60A5FA !important;
    }
    
    /* Assistant message specific styling */
    .stChatMessage [data-testid="stChatMessageContent"] {
        color: #E2E8F0 !important;
    }
    
    /* Tables in assistant responses */
    [data-testid="stChatMessage"] table {
        color: #FFFFFF !important;
        background-color: #1E293B !important;
    }
    
    [data-testid="stChatMessage"] th {
        background: linear-gradient(135deg, #3B82F6, #6366F1) !important;
        color: white !important;
        padding: 10px;
        border-radius: 8px;
    }
    
    [data-testid="stChatMessage"] td {
        background-color: #334155 !important;
        color: #E2E8F0 !important;
        padding: 8px;
    }
    
    /* Code blocks */
    [data-testid="stChatMessage"] code {
        background-color: #0F172A !important;
        color: #60A5FA !important;
        padding: 2px 6px;
        border-radius: 6px;
    }
    
    [data-testid="stChatMessage"] pre {
        background-color: #0F172A !important;
        color: #E2E8F0 !important;
    }

    /* Buttons */
    .stButton button {
        border-radius: 16px;
        height: 52px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        color: white !important;
    }

    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #1E293B !important;
        border-right: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #E2E8F0 !important;
    }

    /* Input Field */
    .stChatInput input {
        background: #1E293B !important;
        color: #FFFFFF !important;
        border: 2px solid #3B82F6 !important;
        border-radius: 9999px;
        padding: 16px 24px;
        font-size: 1.05rem;
    }
    
    .stChatInput input::placeholder {
        color: #94A3B8 !important;
    }

    /* Quick Pills */
    .pill-button {
        background: #334155;
        border: 1px solid #475569;
        color: #CBD5E1;
        border-radius: 50px;
        padding: 12px 20px;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .pill-button:hover {
        background: linear-gradient(90deg, #3B82F6, #8B5CF6);
        color: white;
        border-color: transparent;
        transform: translateY(-2px);
    }

    h1, h2, h3, label {
        color: #FFFFFF !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #1E293B !important;
        color: #60A5FA !important;
    }
    
    .streamlit-expanderContent {
        background-color: #0F172A !important;
        color: #E2E8F0 !important;
    }
    
    /* Status messages */
    .stAlert {
        background-color: #1E293B !important;
        color: #E2E8F0 !important;
    }
    
    /* Spinner text */
    .stSpinner > div {
        color: #60A5FA !important;
    }
</style>
""", unsafe_allow_html=True)

# ====================== HELPERS ======================
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
        "content": "Hello! I'm **Lumina** — your intelligent AI mobile advisor. How can I help you find the perfect smartphone today? 📱✨"
    }]

# ====================== HERO SECTION ======================
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.markdown('<h1 class="main-title">LUMINA</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Premium AI Mobile Advisor • Real-time Intelligence • Powered by Groq</p>', unsafe_allow_html=True)

# ====================== QUICK PROMPTS ======================
st.markdown("### Popular Searches")
pill_cols = st.columns(5)

quick_prompts = [
    ("🔥 Top Flagships 2026", "Recommend the best flagship phones in 2026 with detailed specs"),
    ("💰 Under 50K", "Best smartphones under 50000 PKR with value for money"),
    ("📸 Camera Kings", "Best camera phones for photography in Pakistan with megapixel details"),
    ("⚡ Gaming Beast", "Best gaming phones with high refresh rate and cooling systems"),
    ("🌟 Value Picks", "Best value for money smartphones right now under 100K PKR")
]

for i, (label, prompt) in enumerate(quick_prompts):
    with pill_cols[i]:
        if st.button(label, key=f"pill_{i}", use_container_width=True):
            st.session_state.quick_prompt = prompt

st.divider()

# ====================== CHAT INTERFACE ======================
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("### Navigation")
    st.button("🏠 Home", use_container_width=True)
    st.button("📱 All Smartphones", use_container_width=True)
    st.button("🔍 Compare Phones", use_container_width=True)
    st.button("📸 Camera Hub", use_container_width=True)
    st.button("🎮 Gaming Zone", use_container_width=True)
    st.button("💎 Premium Picks", use_container_width=True)

    st.divider()
    st.markdown("### Settings")
    voice_enabled = st.checkbox("🔊 Enable Voice Response", value=False)
    st.caption("Lumina v2.2 • Premium Experience")

# ====================== CHAT INPUT ======================
prompt = st.chat_input("Ask anything about smartphones...")

if "quick_prompt" in st.session_state and st.session_state.quick_prompt:
    prompt = st.session_state.quick_prompt
    del st.session_state.quick_prompt

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)

    # Analysis
    sentiment = analyze_sentiment(prompt)
    intent = detect_intent(prompt)

    system_prompt = f"""You are Lumina, a premium, witty, and highly knowledgeable AI mobile advisor.
    Speak elegantly with a touch of personality. Use emojis tastefully.
    Current sentiment: {sentiment}
    Detected intent: {intent}
    Always mention key specs and current price ranges in PKR when recommending phones.
    Format responses with proper markdown, use tables for comparisons, and bold text for important specs.
    Be conversational but informative. Limit responses to 400 words max.
    Use 📱, 🔥, 💰, ⚡, 📸 emojis where appropriate."""

    # Assistant response
    with chat_container:
        with st.chat_message("assistant"):
            if not client:
                st.error("⚠️ Groq API key is missing. Please check your .env file.")
                full_response = "API configuration error. Please add your Groq API key."
            else:
                with st.spinner("Lumina is thinking..."):
                    try:
                        # Updated to use the correct model name
                        stream = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",  # ✅ Fixed: Updated to active model
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
