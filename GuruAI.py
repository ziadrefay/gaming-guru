import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Gemly AI Ultra", page_icon="🎮", layout="wide")

# --- 2. كود الـ CSS (تنسيق الزرار والشكل النيون) ---
st.markdown("""
    <style>
        /* إخفاء الهيدر والفوتر */
        header {visibility: hidden !important; height: 0px !important;}
        .stDeployButton {display:none !important;}
        footer {visibility: hidden !important;}

        /* تنسيق زرار القائمة الجانبية (السهم) */
        button[data-testid="stSidebarCollapseButton"] {
            visibility: visible !important;
            display: flex !important;
            position: fixed !important;
            top: 15px !important;
            left: 15px !important;
            z-index: 9999999 !important;
            background-color: #1a1a1a !important;
            border: 2px solid #00ffcc !important;
            color: #00ffcc !important;
            border-radius: 50% !important;
            width: 45px !important;
            height: 45px !important;
            box-shadow: 0 0 15px #00ffcc !important;
        }

        /* تحسين شكل التطبيق */
        .stApp {
            background: #0a0a0a;
            color: #ffffff;
        }

        .neon-title {
            color: #00ffcc;
            text-align: center;
            font-size: 50px;
            font-weight: 900;
            text-shadow: 0 0 20px #00ffcc;
            margin-top: -30px;
        }

        /* تنسيق صندوق الشات ليكون في المنتصف */
        .stChatInputContainer {
            bottom: 20px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. الذاكرة واللغات ---
if "messages" not in st.session_state:
    st.session_state.messages = []

languages = {
    "العربية": {
        "title": "GEMLY AI",
        "subtitle": "مساعدك الذكي في الألعاب والتقنية",
        "clear": "🗑️ مسح المحادثة",
        "placeholder": "اكتب رسالتك هنا...",
        "specs": "💻 فحص توافق جهازك"
    },
    "English": {
        "title": "GEMLY AI",
        "subtitle": "Your Gaming & Tech AI Assistant",
        "clear": "🗑️ Clear Chat",
        "placeholder": "Type your message...",
        "specs": "💻 PC Specs Check"
    }
}

# --- 4. القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h1 style='color:#00ffcc;'>🎮 GEMLY PANEL</h1>", unsafe_allow_html=True)
    lang_choice = st.selectbox("🌐 Choose Language", ["العربية", "English"])
    t = languages[lang_choice]
    
    st.markdown("---")
    if st.button(t["clear"]):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.write("👨‍💻 Dev: Ziad Zaza")

# --- 5. إعداد الموديل ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # استخدمنا 1.5 فلاش لدعمه الكامل للمحادثات المستمرة
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key Missing!")

# --- 6. الواجهة الرئيسية ---
st.markdown(f'<p class="neon-title">{t["title"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align:center; opacity:0.7; margin-bottom:40px;">{t["subtitle"]}</p>', unsafe_allow_html=True)

# عرض فقاعات المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال المحادثة
if prompt := st.chat_input(t["placeholder"]):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # رد الذكاء الاصطناعي
    with st.chat_message("assistant"):
        with st.spinner("..."):
            try:
                # إرسال سياق المحادثة كاملة ليكون "فاكر" الكلام
                history_text = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                response = model.generate_content(f"Answer as Gemly AI (Pro Gamer). Lang: {lang_choice}. Context:\n{history_text}")
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error("Error connecting to Gemini.")

# --- 7. أداة فحص المواصفات ---
with st.expander(t["specs"]):
    hw = st.text_input("Hardware (CPU/GPU):")
    gm = st.text_input("Game Name:")
    if st.button("Analyze 🚀"):
        if hw and gm:
            res = model.generate_content(f"Can {hw} run {gm}? Give FPS tips.")
            st.write(res.text)
