import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة والـ CSS (النيون والشكل الاحترافي) ---
st.set_page_config(page_title="Gemly AI", page_icon="🎮", layout="wide")

st.markdown("""
    <style>
        header {visibility: hidden;}
        .stDeployButton {display:none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp { background: #0a0a0a; color: #ffffff; }
        .neon-text {
            color: #00ffcc;
            text-align: center;
            font-size: 50px;
            font-weight: bold;
            text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
            margin-bottom: 20px;
        }
        .stButton>button {
            width: 100%;
            background: linear-gradient(45deg, #00ffcc, #0099ff) !important;
            color: black !important;
            font-weight: bold !important;
            border-radius: 12px !important;
            border: none !important;
            height: 50px;
            transition: 0.4s;
        }
        .stButton>button:hover {
            box-shadow: 0 0 25px #00ffcc !important;
            transform: scale(1.02);
        }
        .stTextInput>div>div>input {
            background-color: #161616 !important;
            color: #00ffcc !important;
            border: 1px solid #00ffcc !important;
            border-radius: 10px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. نظام اللغات ---
languages = {
    "العربية": {
        "title": "GEMLY AI",
        "subtitle": "خبير الألعاب الأول المزود بذكاء Gemini 3.1",
        "news_btn": "📰 أخبار الألعاب العالمية",
        "input_placeholder": "اسأل عن مهمة، قصة، أو تحسين FPS...",
        "img_label": "🖼️ ارفع سكرين شوت من اللعبة (اختياري)",
        "submit": "إرسال السؤال",
        "specs_header": "💻 فحص توافق جهازك",
        "loading": "جاري استدعاء الخبرات القتالية..."
    },
    "English": {
        "title": "GEMLY AI",
        "subtitle": "The #1 Gaming Expert powered by Gemini 3.1",
        "news_btn": "📰 Global Gaming News",
        "input_placeholder": "Ask about missions, lore, or FPS boost...",
        "img_label": "🖼️ Upload Gameplay Screenshot (Optional)",
        "submit": "Send Question",
        "specs_header": "💻 PC Compatibility Check",
        "loading": "Summoning combat expertise..."
    }
}

# --- 3. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h1 style='color:#00ffcc;'>🎮 Gemly App</h1>", unsafe_allow_html=True)
    selected_lang = st.selectbox("🌐 Language", list(languages.keys()))
    t = languages[selected_lang]
    st.markdown("---")
    get_news = st.button(t["news_btn"])
    st.markdown("---")
    st.write("🚀 Version: 1.0 (Flash Lite)")
    st.write("👨‍💻 Dev: Ziad&Gaming Guru Team")

# --- 4. إعداد الموديل (Gemini 3.1 Flash Lite) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        model_name="gemini-3.1-flash-lite",
        system_instruction=f"You are Gemly AI, a pro gaming expert. Always respond in {selected_lang}. Use gaming slang and be very helpful with technical issues and game walkthroughs."
    )
except:
    st.error("API Key Missing!")

# --- 5. الواجهة الرئيسية ---
st.markdown(f'<p class="neon-text">{t["title"]}</p>', unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#bbb;'>{t['subtitle']}</p>", unsafe_allow_html=True)

if get_news:
    with st.spinner("🔍 Fetching news..."):
        news_res = model.generate_content("Give me 3 latest gaming news points.")
        st.info(news_res.text)

# --- ميزة الصور الجديدة ---
uploaded_file = st.file_uploader(t["img_label"], type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Current Screenshot", width=400)

user_query = st.text_input(t["input_placeholder"])

if st.button(t["submit"]):
    if user_query:
        with st.spinner(t["loading"]):
            try:
                # بما أن Lite يركز على النص، سنرسل الاستفسار النصي
                # وإذا كانت هناك صورة، يمكن للمستخدم وصفها في النص
                response = model.generate_content(user_query)
                st.markdown("### 💡 Answer:")
                st.success(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Write something first!")

# --- 6. أداة فحص المواصفات ---
st.markdown("---")
with st.expander(t["specs_header"]):
    col1, col2 = st.columns(2)
    with col1: cpu_gpu = st.text_input("CPU & GPU")
    with col2: game_name = st.text_input("Game Name")
    if st.button("Analyze Performance 🚀"):
        if cpu_gpu and game_name:
            res = model.generate_content(f"Can I run {game_name} on {cpu_gpu}? Give FPS tips.")
            st.write(res.text)
