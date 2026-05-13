import streamlit as st
import google.generativeai as genai

# --- 1. إعدادات الصفحة والـ CSS السحري (تصميم نيون + إخفاء أدوات الويب) ---
st.set_page_config(page_title="Gaming Guru AI", page_icon="🎮", layout="wide")

st.markdown("""
    <style>
        header {visibility: hidden;}
        .stDeployButton {display:none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp { background: #0a0a0a; color: #ffffff; }
        
        /* تصميم العنوان النيون */
        .main-title {
            font-family: 'Orbitron', sans-serif;
            color: #00ffcc;
            text-align: center;
            font-size: 45px;
            font-weight: bold;
            text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
        }

        /* تنسيق أزرار النيون */
        .stButton>button {
            width: 100%;
            background: linear-gradient(45deg, #00ffcc, #0099ff) !important;
            color: black !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            border: none !important;
            transition: 0.3s;
        }
        .stButton>button:hover {
            box-shadow: 0 0 20px #00ffcc !important;
            transform: translateY(-2px);
        }

        /* تنسيق حقل الإدخال */
        .stTextInput>div>div>input {
            background-color: #1a1a1a !important;
            color: #00ffcc !important;
            border: 1px solid #00ffcc !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. قاموس اللغات ---
languages = {
    "العربية": {
        "title": "GAMING GURU AI",
        "subtitle": "مساعدك الذكي لتطوير الأداء وحل المهام",
        "lang_label": "اختر اللغة",
        "input_label": "اسأل الجورو عن أي شيء (مهام، جرافيك، FPS)...",
        "button": "إرسال السؤال",
        "news_btn": "📰 آخر أخبار الألعاب",
        "img_label": "🖼️ حلل لقطة شاشة من اللعبة (اختياري)",
        "specs_title": "💻 فحص توافق جهازك",
        "chat_placeholder": "جاري استدعاء الخبرات القتالية..."
    },
    "English": {
        "title": "GAMING GURU AI",
        "subtitle": "Your AI Ally for Performance & Walkthroughs",
        "lang_label": "Select Language",
        "input_label": "Ask the Guru anything (Tasks, Graphics, FPS)...",
        "button": "Send Question",
        "news_btn": "📰 Latest Gaming News",
        "img_label": "🖼️ Analyze Gameplay Screenshot (Optional)",
        "specs_title": "💻 PC Compatibility Check",
        "chat_placeholder": "Summoning combat expertise..."
    }
}

# --- 3. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='color:#00ffcc;'>⚙️ Settings</h2>", unsafe_allow_html=True)
    selected_lang = st.selectbox("🌐 Language", list(languages.keys()))
    t = languages[selected_lang]
    
    st.markdown("---")
    # زرار الأخبار
    fetch_news = st.button(t["news_btn"])
    
    st.markdown("---")
    st.write("🔧 Dev: *Ziad & Gemly Team*")

# --- 4. إعداد الـ AI ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # موديل يدعم النصوص والصور معاً
    model = genai.GenerativeModel('gemini-1.5-flash') 
except:
    st.error("API Key Missing in Secrets!")

# --- 5. الواجهة الرئيسية ---
st.markdown(f'<p class="main-title">{t["title"]}</p>', unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'>{t['subtitle']}</p>", unsafe_allow_html=True)

# خاصية الأخبار (تظهر في الأعلى عند الضغط)
if fetch_news:
    with st.spinner("🚀 جاري جلب الأخبار..."):
        news_prompt = f"Give me the top 3 latest gaming news globally in {selected_lang}. Format as bullet points with emojis."
        news_res = model.generate_content(news_prompt)
        st.info(news_res.text)

# مدخلات المستخدم (نص + صورة)
user_input = st.text_input(t["input_label"])
uploaded_file = st.file_uploader(t["img_label"], type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Screenshot", width=300)

if st.button(t["button"]):
    if user_input:
        with st.spinner(t["chat_placeholder"]):
            try:
                # لو فيه صورة، نبعت النص والصورة مع بعض
                if uploaded_file:
                    from PIL import Image
                    img = Image.open(uploaded_file)
                    content = [f"Language: {selected_lang}. Question: {user_input}", img]
                else:
                    content = f"As a gaming expert, answer this in {selected_lang}: {user_input}"
                
                response = model.generate_content(content)
                st.markdown("### 💡 " + ("نصيحة الخبير:" if selected_lang == "العربية" else "Guru's Advice:"))
                st.success(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please type your question!")

# --- 6. فحص المواصفات (Expander) ---
with st.expander(t["specs_title"]):
    specs = st.text_area("Specs (RAM, GPU, CPU):")
    if st.button("Check FPS"):
        res = model.generate_content(f"Can these specs: {specs} run {user_input}? Answer in {selected_lang}")
        st.write(res.text)
