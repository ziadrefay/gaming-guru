import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Gemly AI | Gamer Edition", page_icon="🎮", layout="wide")

# --- 2. كود الـ CSS المتطور (التصميم الاحترافي) ---
st.markdown("""
    <style>
        /* الخلفية العامة */
        .stApp {
            background: radial-gradient(circle at center, #111 0%, #000 100%);
            color: #ffffff;
        }
        
        /* تأثير النيون للعنوان مع أنيميشن */
        .neon-title {
            color: #00ffcc;
            text-align: center;
            font-size: 65px;
            font-weight: 900;
            text-shadow: 0 0 10px #00ffcc, 0 0 30px #00ffcc;
            margin-bottom: 0px;
            animation: pulse 2s infinite;
        }

        /* تصميم الشعار الخاص بك */
        .tagline {
            color: #00ffcc;
            text-align: center;
            font-size: 18px;
            font-style: italic;
            letter-spacing: 2px;
            margin-top: -10px;
            margin-bottom: 30px;
            opacity: 0.8;
            text-shadow: 0 0 5px #00ffcc;
        }

        @keyframes pulse {
            0% { transform: scale(1); text-shadow: 0 0 10px #00ffcc; }
            50% { transform: scale(1.02); text-shadow: 0 0 25px #00ffcc, 0 0 40px #0099ff; }
            100% { transform: scale(1); text-shadow: 0 0 10px #00ffcc; }
        }

        /* تحسين شكل فقاعات الدردشة (Glassmorphism) */
        [data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(0, 255, 204, 0.2) !important;
            border-radius: 20px !important;
            backdrop-filter: blur(10px);
            padding: 20px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }

        /* تعديل شكل الشريط الجانبي */
        [data-testid="stSidebar"] {
            background-color: #050505 !important;
            border-right: 1px solid #00ffcc33;
        }

        /* أزرار نيون */
        .stButton>button {
            border: 1px solid #00ffcc !important;
            background: transparent !important;
            color: #00ffcc !important;
            transition: 0.3s;
            border-radius: 10px !important;
        }
        .stButton>button:hover {
            background: #00ffcc !important;
            color: black !important;
            box-shadow: 0 0 20px #00ffcc;
        }

        /* إخفاء الهيدر بشكل شيك */
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. تهيئة الذاكرة ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h1 style='color:#00ffcc; text-align:center;'>🕹️ GEMLY PANEL</h1>", unsafe_allow_html=True)
    lang_choice = st.selectbox("🌐 Choose Language", ["العربية", "English"])
    st.markdown("---")
    if st.button("🗑️ Clear Archive"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write("🛠️ **Engine:** Gemini 3.1-flash-lite")
    st.write("👨‍💻 **Dev:** Ziad Zaza")

# --- 5. إعداد الموديل ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key Missing!")

# --- 6. الواجهة الرئيسية ---
st.markdown('<p class="neon-title">GEMLY AI</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Built by a gamer, for gamers</p>', unsafe_allow_html=True)

# عرض سجل المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة إدخال الشات (Chat Input)
if prompt := st.chat_input("What's on your mind, Legend?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            try:
                history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                response = model.generate_content(f"You are Gemly AI, a legendary gaming expert. Answer in {lang_choice}. Context:\n{history}")
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("Connection glitch! Try again.")

# --- 7. قسم فحص المواصفات (تصميم أنيق) ---
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("🚀 PC PERFORMANCE ANALYZER"):
    col1, col2 = st.columns(2)
    with col1: hw = st.text_input("Your Specs (e.g. GTX 1650, 8GB RAM)")
    with col2: gm = st.text_input("Game Title")
    
    if st.button("RUN ANALYSIS"):
        if hw and gm:
            with st.spinner("Calculating FPS..."):
                res = model.generate_content(f"Analyze if {hw} can run {gm}. Provide expected FPS and optimization tips in {lang_choice}.")
                st.info(res.text)
