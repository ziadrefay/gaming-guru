import streamlit as st
import google.generativeai as genai

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="GEMLY HUB", page_icon="💎", layout="wide", initial_sidebar_state="expanded")

# --- 2. محرك اللغات (تغيير الواجهة بالكامل) ---
languages = {
    "English": {"dir": "ltr", "align": "left", "news_title": "Global News"},
    "العربية": {"dir": "rtl", "align": "right", "news_title": "الأخبار العالمية"},
    "Deutsch": {"dir": "ltr", "align": "left", "news_title": "Weltnachrichten"},
    "Français": {"dir": "ltr", "align": "left", "news_title": "Nouvelles Mondiales"},
    "日本語": {"dir": "ltr", "align": "left", "news_title": "ニュース"},
    "中文": {"dir": "ltr", "align": "left", "news_title": "全球新闻"},
    "Русский": {"dir": "ltr", "align": "left", "news_title": "Новости"},
    "Português": {"dir": "ltr", "align": "left", "news_title": "Notícias"}
}

# --- 3. الـ CSS (نحت الصورة برمجياً) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    /* الخلفية الكونية المظلمة */
    .stApp {
        background-color: #050510;
        background-image: radial-gradient(circle at 50% 50%, #0a0a25 0%, #050510 100%);
        color: white;
        font-family: 'Orbitron', 'Cairo', sans-serif;
    }

    /* السايدبار الزجاجي الداكن */
    [data-testid="stSidebar"] {
        background-color: #080815 !important;
        border-right: 1px solid #1f1f3d;
        min-width: 380px !important;
    }

    /* أزرار القائمة (Lore, Bios, etc) - نفس الصورة */
    .menu-item {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(0, 255, 204, 0.3);
        border-radius: 10px;
        padding: 12px 20px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 15px;
        color: #fff;
        transition: 0.3s;
    }
    .menu-item:hover {
        background: rgba(0, 255, 204, 0.1);
        border-color: #00ffcc;
        box-shadow: 0 0 15px #00ffcc44;
    }

    /* شعار الهيدر نيون (GEMLY AI) */
    .header-box { text-align: center; margin-top: -60px; padding-bottom: 20px; }
    .g-text { font-size: 50px; font-weight: 700; color: #fff; text-shadow: 0 0 10px #00ffcc; }
    .ai-text { font-size: 50px; font-weight: 700; color: #ff00ff; text-shadow: 0 0 10px #ff00ff; }
    .sub-tag { color: #888; letter-spacing: 4px; font-size: 14px; margin-top: -10px; }

    /* الكارت الرئيسي (الصورة في النص) */
    .hero-card {
        background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url('https://img.freepik.com/free-photo/view-futuristic-robotic-arm_23-2151059350.jpg');
        background-size: cover;
        border: 2px solid #00ffcc;
        border-radius: 20px;
        height: 400px;
        position: relative;
        margin-bottom: 20px;
    }
    .hero-overlay {
        position: absolute; bottom: 20px; left: 20px; right: 20px;
        background: rgba(10, 30, 45, 0.85);
        backdrop-filter: blur(10px);
        border: 1px solid #00ffcc;
        border-radius: 15px;
        padding: 20px;
    }

    /* صناديق الشات */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid #1a1a3a !important;
        border-radius: 15px !important;
    }
    
    /* شريط الكتابة */
    .stChatInputContainer { background: transparent !important; border: 1px solid #00ffcc33 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. السايدبار (مطابق للصورة) ---
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.markdown("<h2 style='color:#00ffcc;'>🕹️ GEMLY <span style='color:#ff00ff;'>HUB</span></h2>", unsafe_allow_html=True)
    
    # قائمة اللغات
    sel_lang = st.selectbox("Select Language", list(languages.keys()))
    l_info = languages[sel_lang]
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # القوائم كما في الصورة
    menu_list = [
        ("📖", "Game Lore & Stories"),
        ("👤", "Character Bios"),
        ("🗺️", "World History"),
        ("❓", "Game Trivia"),
        ("📰", "Global News")
    ]
    for icon, text in menu_list:
        st.markdown(f'<div class="menu-item"><span>{icon}</span> {text}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🗑️ Clear Matrix Archive"):
        st.session_state.messages = []
        st.rerun()
    
    # بروفايل زيزو
    st.markdown(f"""
        <div style='display:flex; align-items:center; gap:12px; padding-top:20px;'>
            <img src='https://avatars.githubusercontent.com/u/1?v=4' width='45' style='border-radius:50%; border:2px solid #00ffcc;'>
            <div><b>Ziad Zaza</b><br><small style='color:#00ffcc;'>Lead Dev</small></div>
        </div>
    """, unsafe_allow_html=True)

# --- 5. الواجهة الرئيسية (التصميم البصري) ---
st.markdown("""
    <div class="header-box">
        <span class="g-text">GEMLY </span><span class="ai-text">AI</span>
        <p class="sub-tag">Built by a gamer, for gamers</p>
    </div>
    """, unsafe_allow_html=True)

# الكارت الكبير في النص
st.markdown("""
    <div class="hero-card">
        <div class="hero-overlay">
            <h3 style="color:#00ffcc; margin:0;">GEMLY STORIES: THE FORGOTTEN ARCANA</h3>
            <p style="color:#00ffcc; font-size:14px; margin:5px 0;">- Chapter 1: The First Resonance.</p>
            <p style="color:#eee; font-size:12px;">Discover the legend of the ancient Arcana city and the machines that rule the 2026 wasteland.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# عرض الشات
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(f"<div style='direction:{l_info['dir']}; text-align:{l_info['align']}'>{msg['content']}</div>", unsafe_allow_html=True)

# إدخال الشات
if prompt := st.chat_input("Speak to the Legend..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            
            # برمجة الشخصية لتناسب لغات العالم
            response = model.generate_content(f"You are Gemly AI, a gaming expert. Respond ONLY in {sel_lang}. Context: {history}\nUser: {prompt}")
            st.markdown(f"<div style='direction:{l_info['dir']}; text-align:{l_info['align']}'>{response.text}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            st.error("Matrix Glitch! Check API Key in Secrets.")

# كروت سفلية (إضافية)
col1, col2 = st.columns(2)
with col1:
    st.markdown("<div class='menu-item'>📖 The Ancient Pact Lore</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='menu-item'>👤 Character: ELARA Guardian</div>", unsafe_allow_html=True)
