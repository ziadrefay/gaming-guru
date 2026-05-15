import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Gemly AI | Stable", page_icon="🎮", layout="wide")

# --- 2. إدارة حالة القائمة الجانبية (Session State) ---
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

# --- 3. كود الـ CSS الخارق (ثبات الزرار وتنسيق النيون) ---
st.markdown(f"""
    <style>
        /* إخفاء الهيدر الأصلي تماماً عشان ميبوظش السهم */
        header {{visibility: hidden !important;}}
        footer {{visibility: hidden !important;}}
        
        .stApp {{
            background: radial-gradient(circle at center, #111 0%, #000 100%);
            color: #ffffff;
        }}

        /* تصميم العنوان والشعار */
        .neon-title {{
            color: #00ffcc;
            text-align: center;
            font-size: 55px;
            font-weight: 900;
            text-shadow: 0 0 15px #00ffcc;
            margin-top: -40px;
        }}
        .tagline {{
            color: #00ffcc;
            text-align: center;
            font-size: 16px;
            font-style: italic;
            margin-top: -10px;
            margin-bottom: 20px;
            opacity: 0.8;
        }}

        /* تصميم زرار القائمة الخاص بنا (Floating Button) */
        .stButton>button[key="toggle_btn"] {{
            position: fixed !important;
            top: 20px !important;
            left: 20px !important;
            z-index: 999999 !important;
            width: 50px !important;
            height: 50px !important;
            border-radius: 50% !important;
            background: #1a1a1a !important;
            border: 2px solid #00ffcc !important;
            color: #00ffcc !important;
            font-size: 20px !important;
            box-shadow: 0 0 15px #00ffcc !important;
        }}
    </style>
""", unsafe_allow_html=True)

# --- 4. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='color:#00ffcc; text-align:center;'>🕹️ GEMLY PANEL</h2>", unsafe_allow_html=True)
    lang_choice = st.selectbox("🌐 Choose Language", ["العربية", "English"])
    st.markdown("---")
    if st.button("🗑️ Clear Archive"):
        st.session_state.messages = []
        st.rerun()
    st.write("🛠️ Engine: Gemini 1.5 Pro")
    st.write("👨‍💻 Dev: Ziad Zaza")

# --- 5. إعداد الموديل والذاكرة ---
if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key Missing!")

# --- 6. الواجهة الرئيسية ---
# عرض العنوان والشعار
st.markdown('<p class="neon-title">GEMLY AI</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Built by a gamer, for gamers</p>', unsafe_allow_html=True)

# عرض سجل الشات
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة إدخال الشات
if prompt := st.chat_input("What's on your mind, Legend?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤖"):
            try:
                history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                response = model.generate_content(f"Answer as Gemly AI (Gaming Expert) in {lang_choice}. Context:\n{history}\nUser: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error("Glitch in the matrix! Try again.")

# --- 7. قسم فحص المواصفات ---
with st.expander("🚀 PC PERFORMANCE ANALYZER"):
    hw = st.text_input("Your Specs:")
    gm = st.text_input("Game Title:")
    if st.button("RUN ANALYSIS"):
        res = model.generate_content(f"Can {hw} run {gm}? Give tips.")
        st.info(res.text)
