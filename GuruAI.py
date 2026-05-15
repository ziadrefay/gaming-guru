import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Gemly AI Ultra", page_icon="🎮", layout="wide")

# --- 2. كود الـ CSS (للتصميم فقط) ---
st.markdown("""
    <style>
        header {visibility: hidden !important; height: 0px !important;}
        footer {visibility: hidden !important;}
        .stApp { background: #0a0a0a; color: #ffffff; }
        
        /* تصميم النيون للعنوان */
        .neon-title {
            color: #00ffcc;
            text-align: center;
            font-size: 50px;
            font-weight: 900;
            text-shadow: 0 0 20px #00ffcc;
            margin-top: -50px;
        }
        
        /* تنسيق فقاعات الشات */
        [data-testid="stChatMessage"] {
            background-color: #161616 !important;
            border: 1px solid #00ffcc33 !important;
            border-radius: 15px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. إدارة حالة القائمة الجانبية (The Fix) ---
# بنستخدم Session State عشان نتحكم في ظهور القائمة
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

# --- 4. القائمة الجانبية ---
# الزرار ده هو اللي هيظهر في الزاوية دايماً
with st.sidebar:
    st.markdown("<h1 style='color:#00ffcc;'>🎮 GEMLY PANEL</h1>", unsafe_allow_html=True)
    lang_choice = st.selectbox("🌐 Language", ["العربية", "English"])
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 5. إعداد الموديل والذاكرة ---
if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key Missing!")

# --- 6. الواجهة الرئيسية ---
# ده زرار "بديل" للسهم، لو القائمة اتقفلت هيفضل موجود فوق
col_btn, col_title = st.columns([1, 10])
with col_btn:
    # ملاحظة: Streamlit لا يدعم فتح السايدبار برمجياً بسهولة إلا عبر الزر الأصلي
    # لذا سنعيد إظهار الزر الأصلي بقوة CSS في مكانه الصحيح
    st.markdown("""
        <style>
            button[data-testid="stSidebarCollapseButton"] {
                visibility: visible !important;
                display: flex !important;
                position: fixed !important;
                top: 10px !important;
                left: 10px !important;
                z-index: 1000000 !important;
                background-color: #00ffcc !important;
                color: black !important;
                border-radius: 5px !important;
            }
        </style>
    """, unsafe_allow_html=True)

st.markdown(f'<p class="neon-title">GEMLY AI</p>', unsafe_allow_html=True)

# عرض الشات
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال الشات
if prompt := st.chat_input("Ask Gemly..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("..."):
            history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            response = model.generate_content(f"You are Gemly AI. Answer in {lang_choice}. Context:\n{history}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
