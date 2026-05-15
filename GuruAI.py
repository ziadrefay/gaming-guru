import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Gemly AI Pro", page_icon="🎮", layout="wide")

# --- 2. كود الـ CSS المطور (للسهم، الهيدر، وفقاعات الشات) ---
st.markdown("""
    <style>
        /* إخفاء الهيدر والفوتر */
        header {visibility: hidden !important;}
        .stDeployButton {display:none !important;}
        footer {visibility: hidden !important;}

        /* إظهار وتصميم سهم القائمة الجانبية (Sidebar Arrow) */
        [data-testid="stSidebarCollapseButton"] {
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
            box-shadow: 0 0 15px rgba(0, 255, 204, 0.4) !important;
        }

        /* خلفية البرنامج */
        .stApp { background: #0a0a0a; color: #ffffff; }

        /* تصميم فقاعات المحادثة */
        [data-testid="stChatMessage"] {
            background-color: #161616 !important;
            border: 1px solid #333 !important;
            border-radius: 15px !important;
            padding: 10px !important;
            margin-bottom: 10px !important;
        }
        
        .neon-text {
            color: #00ffcc;
            text-align: center;
            font-size: 50px;
            font-weight: bold;
            text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
            margin-bottom: 5px;
        }

        /* تنسيق أزرار النيون */
        .stButton>button {
            width: 100%;
            background: linear-gradient(45deg, #00ffcc, #0099ff) !important;
            color: black !important;
            font-weight: bold !important;
            border-radius: 12px !important;
            border: none !important;
            transition: 0.4s;
        }
        .stButton>button:hover {
            box-shadow: 0 0 25px #00ffcc !important;
            transform: scale(1.02);
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. نظام اللغات والذاكرة ---
languages = {
    "العربية": {
        "title": "GEMLY AI",
        "subtitle": "خبير الألعاب الأول المزود بذكاء Gemini 3.1",
        "news_btn": "📰 أخبار الألعاب",
        "clear_btn": "🗑️ مسح المحادثة",
        "input_placeholder": "اسأل Gemly عن أي شيء في عالم الألعاب...",
        "img_label": "🖼️ ارفع سكرين شوت (اختياري)",
        "specs_header": "💻 فحص توافق جهازك",
        "loading": "جاري تحليل البيانات القتالية..."
    },
    "English": {
        "title": "GEMLY AI",
        "subtitle": "The #1 Gaming Expert powered by Gemini 3.1",
        "news_btn": "📰 Gaming News",
        "clear_btn": "🗑️ Clear Chat",
        "input_placeholder": "Ask Gemly anything about gaming...",
        "img_label": "🖼️ Upload Screenshot (Optional)",
        "specs_header": "💻 PC Compatibility Check",
        "loading": "Analyzing combat data..."
    }
}

# تهيئة ذاكرة المحادثة في الـ Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h1 style='color:#00ffcc;'>🎮 Gemly App</h1>", unsafe_allow_html=True)
    selected_lang = st.selectbox("🌐 Language", list(languages.keys()))
    t = languages[selected_lang]
    
    st.markdown("---")
    if st.button(t["news_btn"]):
        st.session_state.get_news = True
    
    if st.button(t["clear_btn"]):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.write("👨‍💻 Dev: Ziad & Gemly Team")

# --- 5. إعداد الموديل ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        model_name="gemini-3.1-flash-lite",
        system_instruction=f"You are Gemly AI, a pro gaming expert. Always respond in {selected_lang}. Be helpful with technical issues and game walkthroughs."
    )
except:
    st.error("API Key Missing!")

# --- 6. الواجهة الرئيسية ---
st.markdown(f'<p class="neon-text">{t["title"]}</p>', unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#bbb; margin-bottom:30px;'>{t['subtitle']}</p>", unsafe_allow_html=True)

# عرض الأخبار إذا ضغط الزر
if st.session_state.get(f"get_news"):
    with st.spinner("🔍 Fetching news..."):
        news_res = model.generate_content("Give me 3 short gaming news points.")
        st.info(news_res.text)
        st.session_state.get_news = False

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# رفع الصور
with st.expander(t["img_label"]):
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(Image.open(uploaded_file), width=300)

# منطقة إدخال الشات (الاحترافية)
if prompt := st.chat_input(t["input_placeholder"]):
    # إضافة رسالة اليوزر للذاكرة وعرضها
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # رد الـ AI
    with st.chat_message("assistant"):
        with st.spinner(t["loading"]):
            try:
                # إرسال المحادثة كاملة كـ Context (سياق)
                history_context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                response = model.generate_content(f"History:\n{history_context}\nUser: {prompt}")
                
                full_response = response.text
                st.markdown(full_response)
                # إضافة رد الـ AI للذاكرة
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error: {e}")

# --- 7. أداة فحص المواصفات (Expander أسفل الشات) ---
st.markdown("<br>", unsafe_allow_html=True)
with st.expander(t["specs_header"]):
    col1, col2 = st.columns(2)
    with col1: cpu_gpu = st.text_input("CPU & GPU")
    with col2: game_name = st.text_input("Game Name")
    if st.button("Analyze Performance 🚀"):
        if cpu_gpu and game_name:
            res = model.generate_content(f"Can I run {game_name} on {cpu_gpu}? Give FPS tips.")
            st.write(res.text)
