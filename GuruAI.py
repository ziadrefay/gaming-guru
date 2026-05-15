import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة (لازم تكون أول سطر) ---
st.set_page_config(page_title="Gemly AI", page_icon="🎮", layout="wide")

# --- 2. كود الـ CSS (لتحسين الشكل فقط بدون إخفاء الهيدر) ---
st.markdown("""
    <style>
        /* تغيير شكل الخلفية والألوان */
        .stApp {
            background-color: #0a0a0a;
            color: #ffffff;
        }
        
        /* تصميم عنوان النيون */
        .neon-title {
            color: #00ffcc;
            text-align: center;
            font-size: 50px;
            font-weight: bold;
            text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
        }

        /* تحسين شكل فقاعات الدردشة */
        [data-testid="stChatMessage"] {
            background-color: #1a1a1a !important;
            border: 1px solid #00ffcc33 !important;
            border-radius: 15px !important;
        }
        
        /* تلوين سهم القائمة الجانبية عشان يبان */
        button[data-testid="stSidebarCollapseButton"] {
            color: #00ffcc !important;
            background-color: #1a1a1a !important;
            border: 1px solid #00ffcc !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. تهيئة الذاكرة (Chat History) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h1 style='color:#00ffcc;'>🎮 GEMLY PANEL</h1>", unsafe_allow_html=True)
    lang_choice = st.selectbox("🌐 Language", ["العربية", "English"])
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.write("👨‍💻 Dev: Ziad Zaza")

# --- 5. إعداد الموديل ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key Missing! ضيف المفتاح في الـ Secrets")

# --- 6. الواجهة الرئيسية ---
st.markdown('<p class="neon-title">GEMLY AI</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#bbb;'>Your Pro Gaming Assistant</p>", unsafe_allow_html=True)

# عرض الشات القديم
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة إدخال الشات
if prompt := st.chat_input("Ask me anything about gaming..."):
    # إضافة سؤالك
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # رد الـ AI
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # تجميع الذاكرة عشان يفتكر الكلام
                history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                response = model.generate_content(f"You are Gemly AI. Answer in {lang_choice}. Context:\n{history}")
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")

# --- 7. فحص المواصفات (أسفل الصفحة) ---
with st.expander("💻 Check PC Specs"):
    hw = st.text_input("Your PC (CPU/GPU):")
    gm = st.text_input("Game Title:")
    if st.button("Can I Run It?"):
        res = model.generate_content(f"Can {hw} run {gm}? Give FPS tips.")
        st.write(res.text)
