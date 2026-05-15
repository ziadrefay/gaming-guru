import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Gemly AI Ultra", page_icon="🎮", layout="wide")

# --- 2. CSS احترافي (حل مشكلة السهم + تحسين الشكل) ---
st.markdown("""
    <style>
        /* إخفاء الهيدر تماماً */
        header {visibility: hidden !important; height: 0px !important;}
        .stDeployButton {display:none !important;}
        footer {visibility: hidden !important;}

        /* إجبار سهم السايدبار على الظهور في كل الحالات */
        button[data-testid="stSidebarCollapseButton"] {
            visibility: visible !important;
            display: flex !important;
            position: fixed !important;
            top: 20px !important;
            left: 20px !important;
            z-index: 9999999 !important;
            background-color: #0a0a0a !important;
            border: 2px solid #00ffcc !important;
            border-radius: 10px !important;
            box-shadow: 0 0 15px #00ffcc !important;
            color: #00ffcc !important;
        }
        
        /* تأثير عند الوقوف على السهم */
        button[data-testid="stSidebarCollapseButton"]:hover {
            background-color: #00ffcc !important;
            color: #000 !important;
        }

        /* تنسيق خلفية التطبيق */
        .stApp {
            background: radial-gradient(circle at top, #1a1a1a 0%, #0a0a0a 100%);
            color: #ffffff;
        }

        /* تصميم كروت المحادثة */
        .stChatMessage {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(0, 255, 204, 0.2) !important;
            border-radius: 20px !important;
            backdrop-filter: blur(10px);
            margin-bottom: 15px !important;
            padding: 15px !important;
        }

        /* عنوان النيون */
        .neon-text {
            color: #00ffcc;
            text-align: center;
            font-size: 60px;
            font-weight: 800;
            text-shadow: 0 0 15px #00ffcc, 0 0 30px #0099ff;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }

        /* تنسيق صناديق الإدخال */
        .stChatInputContainer {
            padding-bottom: 20px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. تهيئة الذاكرة واللغات ---
if "messages" not in st.session_state:
    st.session_state.messages = []

languages = {
    "العربية": {
        "title": "GEMLY AI",
        "subtitle": "مساعدك الشخصي في عالم الألعاب والبرمجة",
        "clear": "🗑️ مسح المحادثة",
        "placeholder": "اكتب سؤالك هنا يا بطل...",
        "specs": "💻 فحص المواصفات"
    },
    "English": {
        "title": "GEMLY AI",
        "subtitle": "Your Ultimate Gaming & Tech Ally",
        "clear": "🗑️ Clear History",
        "placeholder": "Type your message, Legend...",
        "specs": "💻 Specs Check"
    }
}

# --- 4. القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h1 style='color:#00ffcc; text-shadow: 0 0 10px #00ffcc;'>🎮 GEMLY PANEL</h1>", unsafe_allow_html=True)
    lang_choice = st.selectbox("🌐 Choose Language", ["العربية", "English"])
    t = languages[lang_choice]
    
    st.markdown("---")
    if st.button(t["clear"]):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.info("Dev: Ziad & Gaming Guru 💎")

# --- 5. إعداد الموديل (Gemini 3.1 Flash Lite) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash') # التبديل لـ 1.5 لدعم الذاكرة بشكل أفضل
except:
    st.error("API Key Missing!")

# --- 6. عرض المحتوى الرئيسي ---
st.markdown(f'<p class="neon-text">{t["title"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align:center; opacity:0.7;">{t["subtitle"]}</p>', unsafe_allow_html=True)

# عرض الرسائل القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال الشات
if prompt := st.chat_input(t["placeholder"]):
    # إضافة سؤال المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد الرد
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                # سحب الذاكرة لزيادة الذكاء
                history = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages]
                # إرسال السياق كاملاً
                response = model.generate_content(f"Answer as Gemly AI in {lang_choice}. Be a gaming pro. Context: {history}")
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("Connection lost. Try again.")

# --- 7. قسم فحص المواصفات (أسفل الصفحة) ---
with st.expander(t["specs"]):
    cpu = st.text_input("Your Hardware:")
    game = st.text_input("Game Target:")
    if st.button("Get Performance Plan"):
        res = model.generate_content(f"Can {cpu} run {game}? best settings for FPS?")
        st.write(res.text)
