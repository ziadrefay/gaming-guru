import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Gemly AI | The Final Legend", page_icon="🎮", layout="wide")

# --- 2. نظام اللغات الشامل (Dynamic UI) ---
ui_lang = {
    "العربية": {
        "title": "GEMLY AI", "tagline": "صنع بواسطة جيمر، من أجل الجيمرز",
        "news": "📰 أخبار الألعاب العالمية", "lore": "📖 حكاوي وقصص الألعاب",
        "chars": "👤 دليل الشخصيات", "clear": "🗑️ مسح الأرشيف",
        "input": "تحدث مع الأسطورة...", "sidebar": "لوحة التحكم",
        "specs": "💻 فحص الأداء", "prompt_role": "أنت خبير ألعاب وقصص شخصيات."
    },
    "English": {
        "title": "GEMLY AI", "tagline": "Built by a gamer, for gamers",
        "news": "📰 Global Game News", "lore": "📖 Game Lore & Stories",
        "chars": "👤 Character Bios", "clear": "🗑️ Clear Matrix Archive",
        "input": "Speak to the Legend...", "sidebar": "GEMLY HUB",
        "specs": "💻 Performance Check", "prompt_role": "You are a pro gaming & lore expert."
    },
    "日本語": {
        "title": "GEMLY AI", "tagline": "ゲーマーによる、ゲーマーのための",
        "news": "📰 ゲームニュース", "lore": "📖 ゲームの伝承",
        "chars": "👤 キャラクター紹介", "clear": "🗑️ アーカイブ消去",
        "input": "伝説と話す...", "sidebar": "コントロール",
        "specs": "💻 スペック確認", "prompt_role": "あなたはゲームの専門家です。"
    }
}

# --- 3. الـ CSS الاحترافي (نفس شكل الصورة) ---
st.markdown("""
    <style>
        header {background-color: rgba(0,0,0,0) !important; color: #00ffcc !important;}
        button[data-testid="stSidebarCollapseButton"] {
            background-color: #111 !important; color: #00ffcc !important;
            border: 1px solid #00ffcc !important; box-shadow: 0 0 15px #00ffcc !important;
        }
        .stApp {
            background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                        url('https://wallpaperaccess.com/full/2454508.jpg');
            background-size: cover; color: white;
        }
        .neon-title {
            color: #00ffcc; text-align: center; font-size: 60px; font-weight: 900;
            text-shadow: 0 0 20px #00ffcc, 0 0 40px #ff00ff; margin-top: -60px;
        }
        .tagline {
            color: #ffffff; text-align: center; font-size: 18px; letter-spacing: 2px;
            margin-top: -15px; margin-bottom: 30px; opacity: 0.9;
        }
        [data-testid="stChatMessage"] {
            background: rgba(0, 255, 204, 0.05) !important;
            border: 1px solid rgba(0, 255, 204, 0.2) !important;
            border-radius: 15px !important; backdrop-filter: blur(10px);
        }
        .sidebar-btn {
            display: block; width: 100%; padding: 10px; margin: 5px 0;
            background: rgba(255,255,255,0.05); border: 1px solid #00ffcc33;
            color: white; border-radius: 10px; text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

# --- 4. القائمة الجانبية (The Control Panel) ---
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.markdown(f"<h1 style='color:#00ffcc; text-align:center;'>🕹️ GEMLY HUB</h1>", unsafe_allow_html=True)
    lang = st.selectbox("🌐 Select Language", list(ui_lang.keys()))
    t = ui_lang[lang]
    
    st.markdown("---")
    # أزرار القائمة الجمالية
    st.markdown(f"<div class='sidebar-btn'>{t['lore']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sidebar-btn'>{t['chars']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sidebar-btn'>{t['news']}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button(t['clear']):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown(f"<br><div style='text-align:center;'><img src='https://cdn-icons-png.flaticon.com/512/8036/8036131.png' width='50'><br><b>Ziad Zaza</b><br>Lead Dev</div>", unsafe_allow_html=True)

# --- 5. إعداد الموديل ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Missing API Key in Secrets!")

# --- 6. الواجهة الرئيسية ---
st.markdown(f'<p class="neon-title">{t["title"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="tagline">{t["tagline"]}</p>', unsafe_allow_html=True)

# عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال الشات
if prompt := st.chat_input(t['input']):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🎮 Matrix Connecting..."):
            history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            # الموديل أصبح الآن مبرمجاً على سرد القصص والمعلومات
            full_prompt = f"{t['prompt_role']} Respond in {lang}. Storytelling mode: ON. Context:\n{history}\nUser: {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- 7. قسم الأخبار وفحص المواصفات ---
with st.expander(t['specs']):
    col1, col2 = st.columns(2)
    with col1: hw = st.text_input("Hardware:")
    with col2: gm = st.text_input("Game:")
    if st.button("Analyze 🚀"):
        res = model.generate_content(f"Analyze {gm} on {hw} and give gaming news about it in {lang}.")
        st.info(res.text)
