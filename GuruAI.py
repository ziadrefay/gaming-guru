import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="GEMLY HUB | Ultimate", page_icon="💎", layout="wide")

# --- 2. محرك اللغات والواجهة (UI Translation Engine) ---
languages_map = {
    "English": {"dir": "ltr", "align": "left", "font": "Orbitron"},
    "العربية": {"dir": "rtl", "align": "right", "font": "Cairo"},
    "日本語": {"dir": "ltr", "align": "left", "font": "Sansom"},
    "Español": {"dir": "ltr", "align": "left", "font": "Orbitron"},
    "Français": {"dir": "ltr", "align": "left", "font": "Orbitron"},
    "Deutsch": {"dir": "ltr", "align": "left", "font": "Orbitron"},
    "Русский": {"dir": "ltr", "align": "left", "font": "Orbitron"}
}

# --- 3. الـ CSS الاحترافي المطابق للصورة ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Cairo:wght@400;900&display=swap');

        /* إخفاء الهيدر مع الحفاظ على زر السايدبار النيون */
        header {background: transparent !important;}
        button[data-testid="stSidebarCollapseButton"] {
            background-color: #ff00ff !important;
            color: #fff !important;
            border: 2px solid #00ffcc !important;
            box-shadow: 0 0 20px #00ffcc !important;
        }

        /* الخلفية المجرة المتحركة */
        .stApp {
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                        url('https://images.unsplash.com/photo-1464802686167-b939a6910659?auto=format&fit=crop&q=80&w=2000');
            background-size: cover;
            color: #fff;
            font-family: 'Orbitron', 'Cairo', sans-serif;
        }

        /* تصميم السايدبار (نفس الصورة بظبط) */
        [data-testid="stSidebar"] {
            background: rgba(15, 15, 30, 0.95) !important;
            border-right: 2px solid #ff00ff44;
            min-width: 300px !important;
        }
        
        .sidebar-item {
            padding: 15px; margin: 10px 0;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(0, 255, 204, 0.2);
            border-radius: 12px;
            color: #00ffcc; font-weight: bold;
            display: flex; align-items: center; gap: 10px;
            transition: 0.3s;
        }
        .sidebar-item:hover {
            border-color: #ff00ff;
            box-shadow: 0 0 15px rgba(255, 0, 255, 0.4);
            transform: scale(1.02);
        }

        /* العنوان الرئيسي (نفس الصورة) */
        .header-container { text-align: center; margin-top: -60px; }
        .neon-title {
            font-size: 70px; font-weight: 900;
            background: linear-gradient(to right, #00ffcc, #ff00ff);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(0, 255, 204, 0.5);
        }
        .tagline { color: #ccc; letter-spacing: 5px; font-size: 16px; margin-top: -10px; }

        /* صندوق الشات الزجاجي */
        [data-testid="stChatMessage"] {
            background: rgba(0, 0, 0, 0.5) !important;
            border: 1px solid rgba(0, 255, 204, 0.2) !important;
            border-radius: 20px !important; backdrop-filter: blur(10px);
        }
        
        /* تصميم كروت القصص في المنتصف */
        .story-card {
            background: rgba(0,0,0,0.6); border: 1px solid #00ffcc;
            border-radius: 15px; padding: 20px; margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- 4. القائمة الجانبية (The Control Center) ---
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.markdown("<h1 style='color:#ff00ff; text-align:center;'>🔮 GEMLY HUB</h1>", unsafe_allow_html=True)
    
    # قائمة اللغات
    selected_lang = st.selectbox("Select Dimension Language", list(languages_map.keys()))
    lang_cfg = languages_map[selected_lang]

    st.markdown("---")
    # القوائم كما في الصورة
    st.markdown(f'<div class="sidebar-item">📖 Game Lore & Stories</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-item">👤 Character Bios</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-item">🌍 World History</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-item">📰 Global News 2026</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🗑️ Clear Matrix Archive"):
        st.session_state.messages = []
        st.rerun()
    
    # توقيع المطور كما في الصورة
    st.markdown(f"<div style='text-align:center; padding-top:20px;'><img src='https://avatars.githubusercontent.com/u/1?v=4' width='60' style='border-radius:50%; border:2px solid #ff00ff;'><br><b>Ziad Zaza</b><br><small>Dev & Gamer</small></div>", unsafe_allow_html=True)

# --- 5. إعداد الذكاء الاصطناعي ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Matrix Error: API Key Missing!")

# --- 6. الواجهة الرئيسية (التصميم البصري) ---
st.markdown(f"""
    <div class="header-container">
        <h1 class="neon-title">GEMLY AI</h1>
        <p class="tagline">Built by a gamer, for gamers</p>
    </div>
""", unsafe_allow_html=True)

# عرض الشات
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f"<div style='direction:{lang_cfg['dir']}; text-align:{lang_cfg['align']}'>{message['content']}</div>", unsafe_allow_html=True)

# صندوق الإدخال (تصميم الصورة)
if prompt := st.chat_input("Speak to the Legend..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🎮 Processing Matrix Data..."):
            history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            
            # برمجة الشخصية (Lore + News + Gamer slangs)
            system_instruction = f"""
            Identify: You are Gemly AI.
            Expertise: Deep Game Lore, Character Stories, 2026 Gaming News, and Hardware Benchmarks.
            Instruction: Respond ONLY in {selected_lang}. 
            Vibe: Professional Gamer, helpful, and legendary.
            Context: {history}
            """
            
            response = model.generate_content(system_instruction + "\nUser: " + prompt)
            st.markdown(f"<div style='direction:{lang_cfg['dir']}; text-align:{lang_cfg['align']}'>{response.text}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- 7. قسم القصص والأخبار (المربعات التي في الصورة) ---
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
        <div class="story-card">
            <h3 style="color:#00ffcc;">📖 The Ancient Pact Lore</h3>
            <p style="font-size:14px; color:#ddd;">Explore the secrets of the forgotten city and the machines that rule the 2026 wasteland...</p>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class="story-card">
            <h3 style="color:#ff00ff;">📰 Live News Feed</h3>
            <ul style="font-size:13px; color:#00ffcc;">
                <li>GTA VI: New 2026 Roadmap Leaked</li>
                <li>AC Shadows: FPS Patch for Integrated GPUs</li>
                <li>Gemly AI: New Character Lore Module Online</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
