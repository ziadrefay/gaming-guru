import streamlit as st
import google.generativeai as genai

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="GEMLY HUB", page_icon="💎", layout="wide", initial_sidebar_state="expanded")

# --- 2. محرك اللغات والبيانات ---
# أضفت كل اللغات المطلوبة مع اتجاه النص
languages = {
    "English": {"dir": "ltr", "align": "left", "news": "Latest Gaming News", "check": "Hardware Check", "lore": "Game Lore"},
    "العربية": {"dir": "rtl", "align": "right", "news": "آخر أخبار الألعاب", "check": "فحص الجهاز", "lore": "حكاوي الألعاب"},
    "Deutsch": {"dir": "ltr", "align": "left", "news": "Gaming-News", "check": "Hardware-Check", "lore": "Spiele-Lore"},
    "Français": {"dir": "ltr", "align": "left", "news": "Actualités Gaming", "check": "Vérification PC", "lore": "Histoire du jeu"},
    "日本語": {"dir": "ltr", "align": "left", "news": "ゲームニュース", "check": "スペック確認", "lore": "ゲームの物語"},
    "中文": {"dir": "ltr", "align": "left", "news": "游戏新闻", "check": "硬件检测", "lore": "游戏背景"},
    "Русский": {"dir": "ltr", "align": "left", "news": "Новости игр", "check": "Проверка ПК", "lore": "История игры"},
    "Português": {"dir": "ltr", "align": "left", "news": "Notícias de Jogos", "check": "Verificar Hardware", "lore": "Lore do Jogo"}
}

# --- 3. الـ CSS (نفس الصورة بالضبط بلمسة زجاجية) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Cairo:wght@400;700&display=swap');
    
    .stApp {{
        background: #050510 url('https://www.transparenttextures.com/patterns/stardust.png');
        color: white; font-family: 'Orbitron', 'Cairo', sans-serif;
    }}

    /* السايدبار المزدوج كما في الصورة */
    [data-testid="stSidebar"] {{
        background-color: #0b0b1e !important;
        border-right: 1px solid #1f1f3d;
        min-width: 400px !important;
    }}

    /* الأزرار الجانبية النيون */
    .nav-button {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 255, 204, 0.4);
        border-radius: 12px; padding: 12px 18px; margin-bottom: 12px;
        display: flex; align-items: center; gap: 15px; color: #fff;
        transition: 0.3s; cursor: pointer;
    }}
    .nav-button:hover {{
        background: rgba(0, 255, 204, 0.15);
        border-color: #00ffcc; box-shadow: 0 0 15px #00ffcc88;
    }}

    /* الهيدر الرئيسي */
    .header-box {{ text-align: center; margin-top: -60px; }}
    .title-g {{ font-size: 50px; font-weight: 700; color: #fff; text-shadow: 0 0 10px #00ffcc; }}
    .title-ai {{ font-size: 50px; font-weight: 700; color: #ff00ff; text-shadow: 0 0 10px #ff00ff; }}
    .tagline {{ color: #888; letter-spacing: 4px; font-size: 14px; margin-top: -10px; }}

    /* الصندوق المركزي الكبير */
    .hero-container {{
        border: 2px solid #00ffcc; border-radius: 20px;
        background-image: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('https://img.freepik.com/free-photo/robotic-arm-working-futuristic-factory_23-2151059345.jpg');
        background-size: cover; height: 380px; position: relative; margin: 20px 0;
    }}
    .hero-info {{
        position: absolute; bottom: 20px; left: 20px; right: 20px;
        background: rgba(10, 25, 40, 0.85); backdrop-filter: blur(10px);
        border: 1px solid #00ffcc; border-radius: 15px; padding: 18px;
    }}

    /* صندوق الشات */
    [data-testid="stChatMessage"] {{
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid #1a1a3a !important; border-radius: 15px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. السايدبار (التحكم الكامل) ---
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.markdown("<h2 style='color:#00ffcc; text-align:center;'>🕹️ GEMLY <span style='color:#ff00ff;'>HUB</span></h2>", unsafe_allow_html=True)
    
    # اختيار اللغة (تغيير فوري)
    sel_lang = st.selectbox("🌐 Select Dimension Language", list(languages.keys()))
    l_info = languages[sel_lang]
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # الأزرار كما في الصورة بضبط
    nav_items = [
        ("📖", "Game Lore & Stories"),
        ("👤", "Character Bios"),
        ("🗺️", "World History"),
        ("❓", "Game Trivia"),
        ("📰", "Global News")
    ]
    for icon, text in nav_items:
        st.markdown(f'<div class="nav-button"><span>{icon}</span> {text}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    # ميزة توافق الجهاز (Hardware Check)
    st.markdown(f"### 💻 {l_info['check']}")
    gpu = st.text_input("GPU Name:", placeholder="e.g. Intel HD 4600")
    if st.button("Analyze FPS"):
        st.session_state.hw_check = f"Analyzing {gpu} for 2026 games..."

    if st.button("🗑️ Clear Archive"):
        st.session_state.messages = []
        st.rerun()

    # بروفايل زيزو (نفس الصورة)
    st.markdown(f"""
        <div style='display:flex; align-items:center; gap:12px; margin-top:20px;'>
            <img src='https://avatars.githubusercontent.com/u/1?v=4' width='45' style='border-radius:50%; border:2px solid #ff00ff;'>
            <div><b>Ziad Zaza</b><br><small style='color:#00ffcc;'>Dev & Gamer</small></div>
        </div>
    """, unsafe_allow_html=True)

# --- 5. الواجهة الرئيسية ---
st.markdown(f"""
    <div class="header-box">
        <span class="title-g">GEMLY </span><span class="title-ai">AI</span>
        <p class="tagline">Built by a gamer, for gamers</p>
    </div>
    """, unsafe_allow_html=True)

# الصندوق المركزي الكبير (نفس الصورة)
st.markdown(f"""
    <div class="hero-container">
        <div class="hero-info">
            <h3 style="color:#00ffcc; margin:0;">GEMLY STORIES: THE FORGOTTEN ARCANA</h3>
            <p style="color:#00ffcc; font-size:14px; margin:5px 0;">- Chapter 1: The First Resonance.</p>
            <p style="color:#eee; font-size:12px;">Analyzing the ancient ruins and 2026 tech lore for your journey.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# عرض ميزة الأخبار وتوافق الجهاز
if "hw_check" in st.session_state:
    st.info(st.session_state.hw_check)

# عرض الشات
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(f"<div style='direction:{l_info['dir']}; text-align:{l_info['align']}'>{msg['content']}</div>", unsafe_allow_html=True)

# إدخال الشات مع ربط الميزات
if prompt := st.chat_input("Connect with the Legend..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-flash')
            # برمجة الشخصية لتشمل الأخبار والقصص والتوافق
            sys_prompt = f"""
            Identify: Gemly AI. 
            Role: Gaming Lore Expert & PC Hardware Specialist.
            Current Year: 2026.
            Task: Answer in {sel_lang}. 
            Features: Provide gaming news, story lore, and hardware optimization tips.
            """
            response = model.generate_content(sys_prompt + "\nUser: " + prompt)
            st.markdown(f"<div style='direction:{l_info['dir']}; text-align:{l_info['align']}'>{response.text}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            st.error("Matrix Error: Check API Key!")

# كروت سفلية للميزات
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<div class='nav-button'>📰 {l_info['news']}</div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='nav-button'>📖 {l_info['lore']}</div>", unsafe_allow_html=True)
