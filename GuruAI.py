import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="GEMLY HUB | Real Identity", page_icon="💎", layout="wide")

# --- 2. محرك اللغات الشامل (Global Language Matrix) ---
languages_config = {
    "English": {"dir": "ltr", "align": "left", "font": "Orbitron"},
    "العربية": {"dir": "rtl", "align": "right", "font": "Cairo"},
    "Deutsch": {"dir": "ltr", "align": "left", "font": "Orbitron"},
    "Français": {"dir": "ltr", "align": "left", "font": "Orbitron"},
    "日本語": {"dir": "ltr", "align": "left", "font": "sans-serif"},
    "中文": {"dir": "ltr", "align": "left", "font": "sans-serif"},
    "Русский": {"dir": "ltr", "align": "left", "font": "Orbitron"},
    "Português": {"dir": "ltr", "align": "left", "font": "Orbitron"}
}

# --- 3. الـ CSS السحري (نفس الصورة بالملّي) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Cairo:wght@400;900&display=swap');

        /* الخلفية المجرة الكونية */
        .stApp {
            background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                        url('https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1600');
            background-size: cover;
            color: #fff;
            font-family: 'Orbitron', 'Cairo', sans-serif;
        }

        /* السايدبار المطابق للصورة */
        [data-testid="stSidebar"] {
            background: rgba(10, 10, 25, 0.95) !important;
            border-right: 1px solid rgba(0, 255, 204, 0.3);
            min-width: 320px !important;
        }
        
        .sidebar-header { color: #00ffcc; font-size: 24px; font-weight: 900; display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }
        
        .menu-item {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(0, 255, 204, 0.2);
            padding: 12px 15px;
            border-radius: 10px;
            margin-bottom: 8px;
            color: #fff;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: 0.3s;
        }
        .menu-item:hover { border-color: #ff00ff; box-shadow: 0 0 15px rgba(255, 0, 255, 0.3); cursor: pointer; }

        /* الهيدر الرئيسي (GEMLY AI) */
        .main-title-container { text-align: center; margin-top: -60px; }
        .main-title {
            font-size: 65px; font-weight: 900;
            background: linear-gradient(to right, #00ffcc, #ff00ff);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            margin-bottom: 0;
        }
        .tagline { font-size: 16px; letter-spacing: 4px; color: #eee; margin-top: -15px; }

        /* كارت القصة الكبير (الذي في منتصف الصورة) */
        .story-hero-card {
            background: rgba(0, 0, 0, 0.6);
            border: 2px solid #00ffcc;
            border-radius: 20px;
            padding: 2px;
            margin: 20px 0;
            overflow: hidden;
            position: relative;
        }
        .story-overlay {
            position: absolute; bottom: 20px; left: 20px; right: 20px;
            background: rgba(0, 255, 204, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid #00ffcc;
            padding: 15px; border-radius: 10px;
        }

        /* صندوق الشات والمدخلات */
        [data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(0, 255, 204, 0.15) !important;
            border-radius: 15px !important;
        }
        .stChatInputContainer { background: transparent !important; border: 1px solid #00ffcc44 !important; border-radius: 20px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. السايدبار (نفس محتوى الصورة) ---
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.markdown('<div class="sidebar-header">🕹️ GEMLY HUB</div>', unsafe_allow_html=True)
    
    # اختيار اللغة (أهم جزء)
    selected_lang = st.selectbox("Select Language", list(languages_config.keys()))
    l_cfg = languages_config[selected_lang]
    
    st.markdown("---")
    # القوائم بالترتيب المطابق للصورة
    items = [
        ("📖", "Game Lore & Stories"),
        ("👤", "Character Bios"),
        ("🗺️", "World History"),
        ("❓", "Game Trivia"),
        ("📰", "Global News")
    ]
    for icon, text in items:
        st.markdown(f'<div class="menu-item"><span>{icon}</span> {text}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🗑️ Clear Matrix Archive"):
        st.session_state.messages = []
        st.rerun()
    
    # بروفايل المطور
    st.markdown(f"""
        <div style='display:flex; align-items:center; gap:10px; padding-top:20px;'>
            <img src='https://avatars.githubusercontent.com/u/1?v=4' width='50' style='border-radius:50%; border:1px solid #00ffcc;'>
            <div><b>Ziad Zaza</b><br><small style='color:#00ffcc;'>Dev & Gamer</small></div>
        </div>
    """, unsafe_allow_html=True)

# --- 5. الذكاء الاصطناعي ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except: st.error("Missing API Key!")

# --- 6. الواجهة الرئيسية (التصميم البصري) ---
st.markdown(f"""
    <div class="main-title-container">
        <h1 class="main-title">GEMLY AI</h1>
        <p class="tagline">Built by a gamer, for gamers</p>
    </div>
""", unsafe_allow_html=True)

# عرض الكارت الكبير (Hero Story) كما في الصورة
st.markdown(f"""
    <div class="story-hero-card">
        <img src="https://wallpapers.com/images/featured/gaming-background-9vof8v8d29y80w66.jpg" style="width:100%; height:350px; object-fit:cover; opacity:0.6;">
        <div class="story-overlay">
            <h4 style="margin:0; color:#00ffcc;">GEMLY STORIES: THE FORGOTTEN ARCANA</h4>
            <p style="margin:5px 0; font-size:12px; color:#eee;">Discover the legend of the ancient world. Gemly is now analyzing 2026 lore...</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# عرض الشات
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(f"<div style='direction:{l_cfg['dir']}; text-align:{l_cfg['align']}'>{m['content']}</div>", unsafe_allow_html=True)

# الإدخال (شغال مع اللغات)
if prompt := st.chat_input("Speak to the Legend..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🎮 Connecting..."):
            history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            # برمجة الشخصية على سرد القصص والأخبار
            sys_msg = f"You are Gemly AI. Respond ONLY in {selected_lang}. You are a legendary gamer and lore teller. Context: {history}"
            response = model.generate_content(sys_msg + "\nUser: " + prompt)
            st.markdown(f"<div style='direction:{l_cfg['dir']}; text-align:{l_cfg['align']}'>{response.text}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
