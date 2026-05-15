import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Gemly AI | Global Edition", page_icon="🎮", layout="wide")

# --- 2. كود الـ CSS الأسطوري (جمال استثنائي واستقرار كامل) ---
st.markdown("""
    <style>
        /* جعل الهيدر شفاف للحفاظ على السهم */
        header[data-testid="stHeader"] {
            background-color: rgba(0,0,0,0) !important;
            color: #00ffcc !important;
        }
        
        /* تصميم السهم النيون */
        button[data-testid="stSidebarCollapseButton"] {
            background-color: #111 !important;
            color: #00ffcc !important;
            border: 1px solid #00ffcc !important;
            box-shadow: 0 0 15px #00ffcc !important;
            border-radius: 8px !important;
        }

        /* الخلفية المتدرجة */
        .stApp {
            background: radial-gradient(circle at center, #151515 0%, #000000 100%);
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        /* العنوان الرئيسي النيون */
        .neon-title {
            color: #00ffcc;
            text-align: center;
            font-size: clamp(40px, 8vw, 70px);
            font-weight: 900;
            text-shadow: 0 0 20px #00ffcc, 0 0 40px #0099ff;
            margin-top: -60px;
            letter-spacing: 5px;
            text-transform: uppercase;
        }

        /* شعار الجيمرز المخصص */
        .tagline {
            color: #00ffcc;
            text-align: center;
            font-size: 18px;
            font-weight: 300;
            letter-spacing: 3px;
            margin-top: -15px;
            margin-bottom: 40px;
            opacity: 0.9;
            text-shadow: 0 0 10px #00ffcc;
        }

        /* فقاعات الشات الزجاجية */
        [data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid rgba(0, 255, 204, 0.15) !important;
            border-radius: 20px !important;
            backdrop-filter: blur(12px);
            margin-bottom: 20px !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        /* تحسين المدخلات */
        .stChatInputContainer {
            padding-bottom: 20px !important;
            background-color: transparent !important;
        }
        
        .stChatInputContainer > div {
            border: 1px solid #00ffcc !important;
            border-radius: 15px !important;
        }

        /* تخصيص السايدبار */
        section[data-testid="stSidebar"] {
            background-color: #080808 !important;
            border-right: 1px solid #00ffcc22;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. نظام الذاكرة ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. القائمة الجانبية (كل لغات العالم) ---
with st.sidebar:
    st.markdown("<h1 style='color:#00ffcc; text-align:center;'>🕹️ GEMLY HUB</h1>", unsafe_allow_html=True)
    
    # قائمة لغات موسعة
    languages = {
        "العربية": "Arabic", "English": "English", "Español": "Spanish", 
        "Français": "French", "Deutsch": "German", "日本語": "Japanese", 
        "한국어": "Korean", "Русский": "Russian", "中文": "Chinese"
    }
    selected_lang = st.selectbox("🌐 Select Language / اختر اللغة", list(languages.keys()))
    target_lang = languages[selected_lang]
    
    st.markdown("---")
    if st.button("🗑️ Clear History / مسح السجل"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; color:#555;'>Dev: Ziad Zaza<br>V 2.0 Gold</div>", unsafe_allow_html=True)

# --- 5. إعداد الذكاء الاصطناعي ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key Missing! Please check Streamlit Secrets.")

# --- 6. الواجهة الرئيسية ---
st.markdown('<p class="neon-title">GEMLY AI</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Built by a gamer, for gamers</p>', unsafe_allow_html=True)

# عرض الشات
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال المحادثة
if prompt := st.chat_input("Speak to the Legend..."):
    # حفظ رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد الرد
    with st.chat_message("assistant"):
        with st.spinner("🎮 Processing..."):
            try:
                # سحب السياق بالكامل
                context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                
                system_prompt = f"""
                You are Gemly AI, a world-class gaming expert and technical PC specialist.
                Current Language: {target_lang}.
                Style: Helpful, professional gamer slang, expert in FPS optimization and walkthroughs.
                Context of conversation: {context}
                """
                
                response = model.generate_content(system_prompt + "\nUser: " + prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("Matrix Error: Connection lost. Try again.")

# --- 7. قسم الأدوات الإضافية (بشكل جيمينج شيك) ---
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("🛠️ GAMER TOOLBOX (FPS & SPECS)"):
    col1, col2 = st.columns(2)
    with col1:
        hardware = st.text_input("Your PC Specs:", placeholder="e.g. i5 4th gen, GT 730")
    with col2:
        game = st.text_input("Target Game:", placeholder="e.g. Assassin's Creed Unity")
    
    if st.button("START PERFORMANCE ANALYSIS"):
        if hardware and game:
            with st.spinner("Analyzing hardware limits..."):
                analysis = model.generate_content(f"Act as a hardware expert. Can {hardware} run {game}? Give precise FPS estimates and 3 optimization steps in {target_lang}.")
                st.success(analysis.text)
