import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Gemly AI | Supreme Edition", page_icon="💎", layout="wide")

# --- 2. محرك اللغات الشامل (The Global Engine) ---
languages_db = {
    "العربية": {"code": "ar", "dir": "rtl", "align": "right"},
    "English": {"code": "en", "dir": "ltr", "align": "left"},
    "日本語": {"code": "ja", "dir": "ltr", "align": "left"},
    "Español": {"code": "es", "dir": "ltr", "align": "left"},
    "Français": {"code": "fr", "dir": "ltr", "align": "left"},
    "Deutsch": {"code": "de", "dir": "ltr", "align": "left"},
    "Русский": {"code": "ru", "dir": "ltr", "align": "left"},
    "한국어": {"code": "ko", "dir": "ltr", "align": "left"}
}

# --- 3. الـ CSS الاحترافي (نفس تفاصيل الصورة بدقة) ---
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Cairo:wght@400;900&display=swap');

        /* إظهار السهم النيون بقوة */
        header {{background: transparent !important;}}
        button[data-testid="stSidebarCollapseButton"] {{
            background-color: #00ffcc !important;
            color: #000 !important;
            border: 2px solid #fff !important;
            box-shadow: 0 0 20px #00ffcc !important;
            top: 10px !important;
        }}

        /* الخلفية المجرة */
        .stApp {{
            background: radial-gradient(circle at center, #1a1a2e 0%, #020205 100%);
            background-attachment: fixed;
            color: white;
            font-family: 'Orbitron', 'Cairo', sans-serif;
        }}

        /* عنوان النيون والشعار (نفس الصورة) */
        .main-header {{
            text-align: center;
            margin-top: -60px;
            padding-bottom: 30px;
        }}
        .neon-text {{
            font-size: clamp(40px, 8vw, 80px);
            font-weight: 900;
            color: #fff;
            text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc, 0 0 40px #ff00ff;
            margin-bottom: 0;
        }}
        .tagline {{
            font-size: 18px;
            color: #00ffcc;
            letter-spacing: 5px;
            opacity: 0.8;
            margin-top: -10px;
        }}

        /* السايدبار الزجاجي */
        [data-testid="stSidebar"] {{
            background: rgba(0, 0, 0, 0.7) !important;
            backdrop-filter: blur(20px) !important;
            border-right: 1px solid rgba(0, 255, 204, 0.3);
        }}

        /* كروت الأخبار والقائمة */
        .nav-card {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(0, 255, 204, 0.2);
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 10px;
            transition: 0.3s;
        }}
        .nav-card:hover {{
            border-color: #ff00ff;
            box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
        }}

        /* الشات الاحترافي */
        [data-testid="stChatMessage"] {{
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 20px !important;
            margin-bottom: 15px !important;
        }}
    </style>
""", unsafe_allow_html=True)

# --- 4. القائمة الجانبية (The Master Hub) ---
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.markdown("<h1 style='color:#00ffcc; text-align:center;'>🌌 GEMLY HUB</h1>", unsafe_allow_html=True)
    
    sel_lang = st.selectbox("🌐 Universe Language", list(languages_db.keys()))
    lang_info = languages_db[sel_lang]
    
    st.markdown("---")
    # قسم الأخبار الحي (AI News)
    st.markdown(f"### 📡 Live Feed ({sel_lang})")
    with st.container():
        st.markdown(f"<div class='nav-card'>📖 Game Lore Stories</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='nav-card'>👤 Character Bios</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='nav-card'>📰 Global News 2026</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🗑️ Reset Matrix"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown(f"<br><div style='text-align:center;'><b>Ziad Zaza</b><br><small>Built by a gamer, for gamers</small></div>", unsafe_allow_html=True)

# --- 5. إعداد الذكاء الاصطناعي ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key Missing!")

# --- 6. الواجهة الرئيسية (التصميم البصري) ---
st.markdown(f"""
    <div class="main-header">
        <p class="neon-text">GEMLY AI</p>
        <p class="tagline">Built by a gamer, for gamers</p>
    </div>
""", unsafe_allow_html=True)

# عرض الشات بتنسيق اللغة المختار
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f"<div style='direction:{lang_info['dir']}; text-align:{lang_info['align']}'>{message['content']}</div>", unsafe_allow_html=True)

# إدخال الشات
if prompt := st.chat_input("Connect with Gemly..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🎮 Syncing with Game Servers..."):
            history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            
            # برمجة الموديل ليكون راوي قصص وخبير أخبار
            sys_prompt = f"""
            Role: You are Gemly AI. Legendary gaming expert, lore teller, and tech specialist.
            Language: Respond ONLY in {sel_lang}.
            Current Year: 2026.
            Tasks:
            1. Explain game stories (Lore) and character backgrounds deeply.
            2. Provide current gaming news for 2026.
            3. Optimize hardware performance.
            Context: {history}
            """
            
            response = model.generate_content(sys_prompt + "\nUser: " + prompt)
            st.markdown(f"<div style='direction:{lang_info['dir']}; text-align:{lang_info['align']}'>{response.text}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- 7. قسم الأخبار وفحص الأداء (تحت الشات) ---
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("🛠️ SYSTEM ANALYZER & DAILY NEWS"):
    c1, c2 = st.columns(2)
    hw = c1.text_input("Your Setup:", placeholder="GPU/CPU")
    gm = c2.text_input("Target Game:", placeholder="Game Title")
    if st.button("RUN DEEP ANALYSIS 🚀"):
        analysis_prompt = f"As Gemly AI, analyze if {hw} can run {gm}. Also give 3 latest gaming news titles for today in {sel_lang}."
        res = model.generate_content(analysis_prompt)
        st.info(res.text)
