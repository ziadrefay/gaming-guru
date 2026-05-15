import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Gemly AI | Global", page_icon="🎮", layout="wide")

# --- 2. نظام اللغات المتكامل (Dictionary) ---
languages_content = {
    "العربية": {
        "title": "GEMLY AI",
        "tagline": "صنع بواسطة جيمر، من أجل الجيمرز",
        "sidebar_title": "🕹️ لوحة التحكم",
        "clear_btn": "🗑️ مسح المحادثة",
        "input_msg": "اسأل Gemly أي حاجة...",
        "specs_title": "🛠️ أدوات الجيمرز (الفريمات والمواصفات)",
        "run_btn": "ابدأ التحليل",
        "dev_text": "تطوير: زياد زازا"
    },
    "English": {
        "title": "GEMLY AI",
        "tagline": "Built by a gamer, for gamers",
        "sidebar_title": "🕹️ GEMLY HUB",
        "clear_btn": "🗑️ Clear History",
        "input_msg": "Speak to the Legend...",
        "specs_title": "🛠️ GAMER TOOLBOX (FPS & SPECS)",
        "run_btn": "START ANALYSIS",
        "dev_text": "Dev: Ziad Zaza"
    },
    "Español": {
        "title": "GEMLY AI",
        "tagline": "Creado por un jugador, para jugadores",
        "sidebar_title": "🕹️ PANEL GEMLY",
        "clear_btn": "🗑️ Borrar historial",
        "input_msg": "Habla con la leyenda...",
        "specs_title": "🛠️ HERRAMIENTAS (FPS Y SPECS)",
        "run_btn": "INICIAR ANÁLISIS",
        "dev_text": "Dev: Ziad Zaza"
    }
}

# --- 3. الـ CSS (نفس التصميم الاحترافي مع استقرار السهم) ---
st.markdown("""
    <style>
        header[data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; }
        button[data-testid="stSidebarCollapseButton"] {
            background-color: #111 !important; color: #00ffcc !important;
            border: 1px solid #00ffcc !important; box-shadow: 0 0 10px #00ffcc !important;
        }
        .stApp { background: radial-gradient(circle at center, #151515 0%, #000000 100%); color: white; }
        .neon-title {
            color: #00ffcc; text-align: center; font-size: 60px; font-weight: 900;
            text-shadow: 0 0 20px #00ffcc; margin-top: -60px;
        }
        .tagline {
            color: #00ffcc; text-align: center; font-size: 18px; letter-spacing: 2px;
            margin-top: -15px; margin-bottom: 30px; text-shadow: 0 0 5px #00ffcc;
        }
        [data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(0, 255, 204, 0.2) !important; border-radius: 15px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 4. القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown(f"<h1 style='color:#00ffcc; text-align:center;'>🕹️</h1>", unsafe_allow_html=True)
    selected_lang = st.selectbox("🌐 Select Language", list(languages_content.keys()))
    
    # استدعاء نصوص اللغة المختارة
    txt = languages_content[selected_lang]
    
    st.markdown(f"<h2 style='color:#00ffcc; text-align:center;'>{txt['sidebar_title']}</h2>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button(txt['clear_btn']):
        st.session_state.messages = []
        st.rerun()
    st.write(f"V 2.5 | {txt['dev_text']}")

# --- 5. تهيئة الذاكرة والـ AI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key Missing!")

# --- 6. الواجهة الرئيسية (تتغير لغتها فوراً) ---
st.markdown(f'<p class="neon-title">{txt["title"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="tagline">{txt["tagline"]}</p>', unsafe_allow_html=True)

# عرض الشات
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال الشات
if prompt := st.chat_input(txt['input_msg']):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🎮..."):
            try:
                history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                # إجبار الـ AI على الرد بنفس اللغة المختارة
                response = model.generate_content(f"Answer in {selected_lang}. You are Gemly AI (Gaming Expert). Context:\n{history}\nUser: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error("Error!")

# --- 7. قسم المواصفات (يتغير لغته فوراً) ---
st.markdown("<br>", unsafe_allow_html=True)
with st.expander(txt['specs_title']):
    col1, col2 = st.columns(2)
    with col1: hw = st.text_input("GPU/CPU:")
    with col2: gm = st.text_input("Game:")
    if st.button(txt['run_btn']):
        res = model.generate_content(f"Can {hw} run {gm}? FPS tips in {selected_lang}.")
        st.info(res.text)
