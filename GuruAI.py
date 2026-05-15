import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة (يجب أن يكون أول سطر) ---
st.set_page_config(page_title="Gemly AI | Pro", page_icon="🎮", layout="wide")

# --- 2. كود الـ CSS الذكي (إظهار السهم وتجميل الشكل) ---
st.markdown("""
    <style>
        /* بدلاً من إخفاء الهيدر، سنقوم بتلوينه بلون الخلفية ليختفي بصرياً فقط */
        header[data-testid="stHeader"] {
            background-color: rgba(0,0,0,0) !important;
            color: #00ffcc !important;
        }
        
        /* تلوين السهم وتكبيره عشان تشوفه بوضوح */
        button[data-testid="stSidebarCollapseButton"] {
            background-color: #1a1a1a !important;
            color: #00ffcc !important;
            border: 1px solid #00ffcc !important;
            box-shadow: 0 0 10px #00ffcc !important;
        }

        .stApp {
            background: radial-gradient(circle at center, #111 0%, #000 100%);
            color: #ffffff;
        }

        /* عنوان النيون والشعار */
        .neon-title {
            color: #00ffcc;
            text-align: center;
            font-size: 50px;
            font-weight: 900;
            text-shadow: 0 0 15px #00ffcc;
            margin-top: -60px; /* لرفع العنوان مكان الهيدر */
        }
        .tagline {
            color: #00ffcc;
            text-align: center;
            font-size: 16px;
            font-style: italic;
            margin-top: -10px;
            margin-bottom: 30px;
            opacity: 0.8;
            text-shadow: 0 0 5px #00ffcc;
        }

        /* تنسيق الشات */
        [data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(0, 255, 204, 0.2) !important;
            border-radius: 15px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. تهيئة الذاكرة ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='color:#00ffcc; text-align:center;'>🕹️ GEMLY PANEL</h2>", unsafe_allow_html=True)
    lang_choice = st.selectbox("🌐 Choose Language", ["العربية", "English"])
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write("👨‍💻 **Dev:** Ziad Zaza")

# --- 5. إعداد الموديل ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key Missing! ضيفه في الـ Secrets")

# --- 6. الواجهة الرئيسية ---
st.markdown('<p class="neon-title">GEMLY AI</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Built by a gamer, for gamers</p>', unsafe_allow_html=True)

# عرض سجل المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال الشات
if prompt := st.chat_input("Ask Gemly something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤖"):
            try:
                history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                response = model.generate_content(f"Answer as Gemly AI (Gamer Expert) in {lang_choice}. Context:\n{history}\nUser: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error("Error!")

# --- 7. فحص المواصفات ---
with st.expander("🚀 PC PERFORMANCE ANALYZER"):
    hw = st.text_input("Your Specs:")
    gm = st.text_input("Game Title:")
    if st.button("RUN ANALYSIS"):
        res = model.generate_content(f"Can {hw} run {gm}? Give optimization tips.")
        st.info(res.text)
