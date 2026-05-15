import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="GEMLY AI | Ultimate Gamer OS", page_icon="🎮", layout="wide")

# --- 2. قاموس اللغات الشامل (لترجمة الموقع بالكامل) ---
lang_db = {
    "English": {
        "dir": "ltr", "align": "left", "font": "Orbitron",
        "title": "GEMLY AI", "tagline": "Built by a gamer, for gamers",
        "news_h": "LIVE NEWS FEED", "lore_h": "GAME LORE", "specs_h": "PC PERFORMANCE",
        "input_p": "Speak to the Legend...", "btn_clear": "Wipe Matrix",
        "side_hub": "GEMLY HUB", "news_prompt": "Give me 3 latest gaming news headlines for May 2026."
    },
    "العربية": {
        "dir": "rtl", "align": "right", "font": "Cairo",
        "title": "جيملي AI", "tagline": "صنع بواسطة جيمر، من أجل الجيمرز",
        "news_h": "آخر الأخبار الحية", "lore_h": "حكاوي الألعاب", "specs_h": "أداء الجهاز",
        "input_p": "تحدث مع الأسطورة جيملي...", "btn_clear": "مسح الأرشيف",
        "side_hub": "مركز التحكم", "news_prompt": "أعطني 3 عناوين لأخبار الألعاب العالمية لشهر مايو 2026 باللغة العربية."
    },
    "日本語": {
        "dir": "ltr", "align": "left", "font": "Sansom",
        "title": "ジェムリー AI", "tagline": "ゲーマーのために",
        "news_h": "ライブニュース", "lore_h": "ゲームの物語", "specs_h": "スペック分析",
        "input_p": "伝説と話す...", "btn_clear": "消去する",
        "side_hub": "ハブ", "news_prompt": "2026年5月の最新ゲームニュースを3つ教えてください。"
    }
}

# --- 3. الـ CSS الخرافي (Ultra Gaming Aesthetics) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Cairo:wght@400;900&display=swap');

        /* الهيدر والزرار النيون */
        header {background: transparent !important;}
        button[data-testid="stSidebarCollapseButton"] {
            background-color: #00ffcc !important; color: #000 !important;
            border: 2px solid #fff !important; box-shadow: 0 0 20px #00ffcc;
        }

        /* الخلفية المجرة المتحركة */
        .stApp {
            background: radial-gradient(circle at top right, #1a1a2e, #020205);
            color: #fff;
        }

        /* العنوان RGB المتحرك */
        .neon-title {
            text-align: center; font-size: clamp(40px, 10vw, 85px); font-weight: 900;
            background: linear-gradient(90deg, #00ffcc, #ff00ff, #00ffcc);
            background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            animation: gradient 3s linear infinite; margin-top: -70px;
        }
        @keyframes gradient { 0% {background-position: 0% 50%;} 100% {background-position: 200% 50%;} }

        .tagline { text-align: center; color: #aaa; letter-spacing: 5px; font-size: 18px; margin-top: -20px; }

        /* السايدبار الزجاجي */
        [data-testid="stSidebar"] { background: rgba(10, 10, 20, 0.9) !important; backdrop-filter: blur(25px); border-right: 1px solid #00ffcc44; }

        /* تصميم صناديق الأخبار والشات */
        .glass-card {
            background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(0, 255, 204, 0.2);
            border-radius: 15px; padding: 15px; margin-bottom: 10px; transition: 0.3s;
        }
        .glass-card:hover { border-color: #ff00ff; box-shadow: 0 0 15px rgba(255, 0, 255, 0.3); }

        [data-testid="stChatMessage"] {
            background: rgba(0, 255, 204, 0.05) !important; border-radius: 20px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 4. إدارة الحالة والذكاء الاصطناعي ---
if "messages" not in st.session_state: st.session_state.messages = []
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except: st.error("Check API Key!")

# --- 5. القائمة الجانبية (The Control Center) ---
with st.sidebar:
    st.markdown("<h1 style='color:#00ffcc; text-align:center;'>🕹️ HUB</h1>", unsafe_allow_html=True)
    sel_lang = st.selectbox("Dimension Language", list(lang_db.keys()))
    ld = lang_db[sel_lang] # تحميل نصوص اللغة المختارة

    st.markdown(f"### 📡 {ld['news_h']}")
    if st.button("🔄 Refresh News"):
        news_res = model.generate_content(ld['news_prompt'])
        st.session_state.current_news = news_res.text
    
    if "current_news" in st.session_state:
        st.markdown(f"<div class='glass-card' style='font-size:12px; direction:{ld['dir']}'>{st.session_state.current_news}</div>", unsafe_allow_html=True)

    st.markdown("---")
    if st.button(ld['btn_clear']):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown(f"<div style='text-align:center;'><br><b>Ziad Zaza</b><br><small>{ld['tagline']}</small></div>", unsafe_allow_html=True)

# --- 6. الواجهة الرئيسية (Dynamic UI) ---
st.markdown(f"<div class='neon-title' style='font-family:{ld['font']}'>{ld['title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='tagline'>{ld['tagline']}</div>", unsafe_allow_html=True)

# عرض الشات بالمحاذاة الصحيحة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(f"<div style='direction:{ld['dir']}; text-align:{ld['align']}'>{msg['content']}</div>", unsafe_allow_html=True)

# إدخال الشات
if prompt := st.chat_input(ld['input_p']):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤖"):
            history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            resp = model.generate_content(f"You are Gemly AI. Respond ONLY in {sel_lang}. Expert in Game Lore, Character Stories, and Specs. Context: {history}\nUser: {prompt}")
            st.markdown(f"<div style='direction:{ld['dir']}; text-align:{ld['align']}'>{resp.text}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": resp.text})

# --- 7. قسم فحص الأداء والقصص (Dynamic Expanders) ---
st.markdown("<br>", unsafe_allow_html=True)
col_a, col_b = st.columns(2)
with col_a:
    with st.expander(f"📖 {ld['lore_h']}"):
        st.write("Ask Gemly about any character lore in the chat above!")
with col_b:
    with st.expander(f"💻 {ld['specs_h']}"):
        hw = st.text_input("GPU/CPU:")
        if st.button("Analyze Performance"):
            res = model.generate_content(f"Can {hw} run modern games? Tips in {sel_lang}.")
            st.info(res.text)
