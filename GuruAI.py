import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والتصميم
st.set_page_config(
    page_title="Gaming Guru AI | خبير الألعاب",
    page_icon="🎮",
    layout="centered"
)

# 2. كود التصميم الاحترافي (CSS) - ستايل النيون اللي بتحبه
st.markdown("""
    <style>
    .stApp { background: #0a0a0a; color: #ffffff; }
    .main-title {
        font-family: 'Orbitron', sans-serif;
        color: #00ffcc;
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
        margin-bottom: 30px;
    }
    .stTextInput>div>div>input {
        background-color: #1a1a1a !important;
        color: #00ffcc !important;
        border: 2px solid #00ffcc !important;
        border-radius: 15px !important;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #00ffcc, #0099ff) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        transition: 0.5s !important;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4);
    }
    .stButton>button:hover {
        box-shadow: 0 0 30px #00ffcc !important;
        transform: translateY(-3px);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إعداد الذكاء الاصطناعي
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        # استخدام الموديل الحديث والمستقر
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction="أنت 'Gaming Guru AI'، خبير ألعاب محترف جداً ومساعد تقني للأجهزة. رد بحماس وبمصطلحات الجيمرز."
        )
    else:
        st.error("⚠️ خطأ: لم يتم العثور على API Key في Secrets")
        st.stop()
except Exception as e:
    st.error(f"❌ مشكلة في الاتصال: {e}")
    st.stop()

# 4. واجهة المستخدم
st.markdown('<p class="main-title">GAMING GURU AI</p>', unsafe_allow_html=True)

# تهيئة ذاكرة المحادثة (عشان يفتكرك)
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة السؤال
user_input = st.chat_input("اسأل خبير الألعاب عن أي شيء...")

if user_input:
    # إضافة سؤال المستخدم للذاكرة والعرض
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # رد الذكاء الاصطناعي
    with st.chat_message("assistant"):
        with st.spinner('جاري استدعاء الخبرات القتالية...'):
            try:
                response = model.generate_content(user_input)
                full_response = response.text
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

# القائمة الجانبية
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/681/681392.png", width=100)
    st.title("إعدادات Guru")
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.write("🔧 تم التطوير بواسطة: *Zizo & Gaming Guru Team*")
    st.write("🖥️ Optimized for: *HP EliteDesk*")
