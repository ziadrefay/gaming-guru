import streamlit as st
import google.generativeai as genai

# --- 1. إعداد الصفحة ---
st.set_page_config(page_title="GEMLY HUB", page_icon="🎮", layout="wide", initial_sidebar_state="expanded")

# --- 2. محرك اللغات الشامل ---
langs = {
    "English": {"dir": "ltr", "align": "left"},
    "العربية": {"dir": "rtl", "align": "right"},
    "Français": {"dir": "ltr", "align": "left"},
    "Deutsch": {"dir": "ltr", "align": "left"},
    "日本語": {"dir": "ltr", "align": "left"},
    "中文": {"dir": "ltr", "align": "left"},
    "Русский": {"dir": "ltr", "align": "left"},
    "Português": {"dir": "ltr", "align": "left"}
}

# --- 3. CSS "نسخة طبق الأصل" من الصورة ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
        
        /* الخلفية الكونية */
        .stApp {
            background: #05050a url('https://www.transparenttextures.com/patterns/stardust.png');
            background-color: #08081a;
            color: white;
            font-family: 'Orbitron', 'Cairo', sans-serif;
        }

        /* تنسيق السايدبار الكامل */
        [data-testid="stSidebar"] {
            background-color: #0b0b18 !important;
            border-right: 1px solid #1f1f3d;
            min-width: 350px !important;
        }

        /* أيقونات العمود الرفيع (اليسار) */
        .side-icons {
            position: fixed; left: 0; top: 0; bottom: 0; width: 60px;
            background: #080812; border-right: 1px solid #1a1a2e;
            display: flex; flex-direction: column; align-items: center; padding-top: 20px; gap: 25px;
        }

        /* أزرار القائمة الجانبية (نفس الصورة) */
        .menu-btn {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(0, 255, 204, 0.3);
            border-radius: 12px; padding: 12px; margin-bottom: 10px;
            display: flex; align-items: center; gap: 15px; color: #fff;
            cursor: pointer; transition: 0.3s;
        }
        .menu-btn:hover { background: rgba(0, 255, 204, 0.1); border-color: #00ffcc; box-shadow: 0 0 10px #00ffcc; }

        /* الهيدر النيون المزدوج */
        .main-header { text-align: center; margin-top: -50px; }
        .title-gemly { font-size: 55px; font-weight: bold; color: #fff; text-shadow: 0 0 10px #00ffcc; display: inline; }
        .title-ai { font-size: 55px; font-weight: bold; color: #ff00ff; text-shadow: 0 0 10px #ff00ff; display: inline; }
        .tagline { color: #aaa; letter-spacing: 3px; font-size: 14px; margin-top: -5px; }

        /* الكارت الكبير في المنتصف */
        .hero-card {
            background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://img.freepik.com/free-photo/view-futuristic-robotic-arm_23-2151059350.jpg');
            background-size: cover; border: 2px solid #00ffcc; border-radius: 20px;
            height: 380px; position: relative; margin: 20px 0;
        }
        .hero-text-box {
            position: absolute; bottom: 20px; left: 20px; right: 20px;
            background: rgba(10, 30, 40, 0.8); backdrop-filter: blur(10px);
            border: 1px solid #00ffcc; padding: 15px; border-radius: 10px;
        }

        /* كروت صغيرة تحت الشات */
        .sub-card {
            background: rgba(20, 20, 40, 0.6); border: 1px solid #333;
            border-radius: 10px; padding: 15px; margin-top: 10px;
        }

        /* الشات */
        [data-testid="stChatMessage"] { background: rgba(0,0,0,0.3) !important; border-radius: 15px !important; border: 1px solid #1f1f3d !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. السايدبار (تصميم طبق الأصل) ---
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    # اللوجو العلوي
    st.markdown("<h2 style='color:#00ffcc; text-align:center;'>🕹️ GEMLY <span style='color:#ff00ff;'>HUB</span></h2>", unsafe_allow_html=True)
    
    # اختيار اللغة
    selected_lang = st.selectbox("🌐 Select Language", list(langs.keys()))
    l_info = langs[selected_lang]
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # أزرار المنيو الجانبي
    menu_items = [
        ("📖", "Game Lore & Stories"),
        ("👤", "Character Bios"),
        ("🗺️", "World History"),
        ("❓", "Game Trivia"),
        ("📰", "Global News")
    ]
    for icon, text in menu_items:
        st.markdown(f'<div class="menu-btn"><span>{icon}</span> {text}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🗑️ Clear Matrix Archive"):
        st.session_state.messages = []
        st.rerun()
    
    # بروفايل زيزو
    st.markdown(f"""
        <div style='display:flex; align-items:center; gap:12px; margin-top:20px;'>
            <img src='https://avatars.githubusercontent.com/u/1?v=4' width='45' style='border-radius:50%; border:2px solid #ff00ff;'>
            <div><b style='font-size:14px;'>Ziad Zaza</b><br><small style='color:#00ffcc;'>Developer</small></div>
        </div>
    """, unsafe_allow_html=True)

# --- 5. الواجهة الرئيسية ---
st.markdown("""
    <div class="main-header">
        <div class="title-gemly">GEMLY </div><div class="title-ai">AI</div>
        <p class="tagline">Built by a gamer, for gamers</p>
    </div>
""", unsafe_allow_html=True)

# الكارت الكبير (Hero Story)
st.markdown("""
    <div class="hero-card">
        <div class="hero-text-box">
            <h4 style="color:#00ffcc; margin:0;">GEMLY STORIES: THE FORGOTTEN ARCANA</h4>
            <p style="font-size:12px; color:#ddd; margin:5px 0;">Chapter 1: The First Resonance. Discover the legend of ancient ruins and machines.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# عرض الشات
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(f"<div style='direction:{l_info['dir']}; text-align:{l_info['align']}'>{m['content']}</div>", unsafe_allow_html=True)

# إدخال الشات
if prompt := st.chat_input("Speak to the Legend..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            response = model.generate_content(f"You are Gemly AI, a gaming legend. Respond ONLY in {selected_lang}. Context: {history}\nUser: {prompt}")
            st.markdown(f"<div style='direction:{l_info['dir']}; text-align:{l_info['align']}'>{response.text}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            st.error("Check your API Key in Secrets!")

# الكروت السفلية
col1, col2 = st.columns(2)
with col1:
    st.markdown("<div class='sub-card'><b>📖 The Ancient Pact Lore</b><br><small>Explore forgotten city secrets.</small></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='sub-card'><b>👤 Character: ELARA</b><br><small>Arcana Guardian Bio.</small></div>", unsafe_allow_html=True)
