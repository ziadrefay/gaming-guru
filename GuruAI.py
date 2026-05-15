import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة (أول سطر دائماً) ---
st.set_page_config(page_title="Gemly AI | The Final Legend", page_icon="🎮", layout="wide")

# --- 2. نظام اللغات الشامل (Dynamic UI) ---
# إضافة لغات أكثر وربطها بكل نصوص الموقع
ui_translations = {
    "العربية": {
        "title": "GEMLY AI", "tagline": "صنع بواسطة جيمر، من أجل الجيمرز",
        "news": "📰 أخبار الجيمز اليومية", "lore": "📖 قصص وحكاوي الألعاب",
        "chars": "👤 موسوعة الشخصيات", "clear": "🗑️ مسح الأرشيف",
        "input": "تحدث مع الأسطورة جيملي...", "sidebar_title": "لوحة التحكم",
        "specs": "💻 فحص المواصفات", "news_list": ["تحديث Assassin's Creed الجديد", "تسريبات GTA VI", "أفضل أجهزة الـ Gaming في 2026"]
    },
    "English": {
        "title": "GEMLY AI", "tagline": "Built by a gamer, for gamers",
        "news": "📰 Global Gaming News", "lore": "📖 Game Lore & Stories",
        "chars": "👤 Character Database", "clear": "🗑️ Clear Matrix Archive",
        "input": "Speak to the Legend Gemly...", "sidebar_title": "GEMLY HUB",
        "specs": "💻 PC Specs Check", "news_list": ["New AC Shadows Update", "GTA VI Rumors Surge", "Top Gaming Hardware 2026"]
    },
    "Español": {
        "title": "GEMLY AI", "tagline": "Creado por un jugador, para jugadores",
        "news": "📰 Noticias de Juegos", "lore": "📖 Historias de Juegos",
        "chars": "👤 Biografías", "clear": "🗑️ Borrar Historial",
        "input": "Habla con la leyenda...", "sidebar_title": "PANEL GEMLY",
        "specs": "💻 Análisis de Specs", "news_list": ["Noticias de PlayStation", "Xbox Game Pass", "E-sports Global"]
    },
    "日本語": {
        "title": "GEMLY AI", "tagline": "ゲーマーによるゲーマーのための",
        "news": "📰 ゲームニュース", "lore": "📖 ゲームの物語",
        "chars": "👤 キャラクター紹介", "clear": "🗑️ アーカイブを消去",
        "input": "伝説のジェムリーと話す...", "sidebar_title": "ハブ",
        "specs": "💻 スペック確認", "news_list": ["新作ゲーム情報", "任天堂の最新ニュース", "PCビルドのヒント"]
    }
}

# --- 3. الـ CSS الاحترافي (نفس شكل الصورة تماماً) ---
st.markdown("""
    <style>
        /* إخفاء الهيدر مع إظهار السهم بلون نيون */
        header {background-color: rgba(0,0,0,0) !important; color: #00ffcc !important;}
        button[data-testid="stSidebarCollapseButton"] {
            background-color: #111 !important; color: #00ffcc !important;
            border: 2px solid #00ffcc !important; box-shadow: 0 0 15px #00ffcc !important;
        }

        /* خلفية الفضاء والمجرة */
        .stApp {
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                        url('https://images.unsplash.com/photo-1462331940025-496dfbfc7564?auto=format&fit=crop&q=80&w=2000');
            background-size: cover; color: white;
        }

        /* تصميم العنوان الرئيسي النيون (نفس الصورة) */
        .neon-title {
            color: #ffffff; text-align: center; font-size: 70px; font-weight: 900;
            text-shadow: 0 0 20px #00ffcc, 0 0 40px #ff00ff; margin-top: -50px;
            font-family: 'Arial Black', sans-serif;
        }
        .tagline {
            color: #ffffff; text-align: center; font-size: 18px; letter-spacing: 3px;
            margin-top: -15px; margin-bottom: 40px; opacity: 0.9;
        }

        /* السايدبار الزجاجي */
        section[data-testid="stSidebar"] {
            background: rgba(10, 10, 20, 0.9) !important;
            border-right: 2px solid #00ffcc44;
        }

        /* أزرار القائمة الجانبية */
        .nav-item {
            padding: 12px; margin: 8px 0; background: rgba(0, 255, 204, 0.05);
            border: 1px solid #00ffcc33; border-radius: 10px; color: #00ffcc;
            font-weight: bold; transition: 0.3s; cursor: pointer;
        }
        .nav-item:hover { background: rgba(0, 255, 204, 0.2); box-shadow: 0 0 10px #00ffcc; }

        /* فقاعات الشات الاحترافية */
        [data-testid="stChatMessage"] {
            background: rgba(0, 0, 0, 0.4) !important;
            border: 1px solid rgba(0, 255, 204, 0.2) !important;
            border-radius: 20px !important; backdrop-filter: blur(15px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }

        /* شريط المدخلات */
        .stChatInputContainer { border-top: 1px solid #00ffcc33 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. القائمة الجانبية (The Control Center) ---
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.markdown(f"<h1 style='color:#00ffcc; text-align:center;'>🕹️ GEMLY HUB</h1>", unsafe_allow_html=True)
    
    # اختيار اللغة
    selected_lang = st.selectbox("🌐 Choose Language / اختر اللغة", list(ui_translations.keys()))
    t = ui_translations[selected_lang]
    
    st.markdown("---")
    # قائمة الأخبار والخدمات
    st.markdown(f"<div class='nav-item'>{t['lore']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='nav-item'>{t['chars']}</div>", unsafe_allow_html=True)
    
    st.markdown(f"### {t['news']}")
    for news in t['news_list']:
        st.markdown(f"<small style='color:#00ffcc;'>• {news}</small>", unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button(t['clear']):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown(f"<br><div style='text-align:center; border-top: 1px solid #333; padding-top: 10px;'><b>Ziad Zaza</b><br><small>Built by a Gamer</small></div>", unsafe_allow_html=True)

# --- 5. إعداد الموديل ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key Missing!")

# --- 6. الواجهة الرئيسية ---
st.markdown(f'<p class="neon-title">{t["title"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="tagline">{t["tagline"]}</p>', unsafe_allow_html=True)

# عرض الشات
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال الشات
if prompt := st.chat_input(t['input']):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🎮 Matrix Data Retrieval..."):
            try:
                history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                # الموديل أصبح الآن "خبير قصص وشخصيات"
                response = model.generate_content(f"You are Gemly AI. Respond in {selected_lang}. Expert in gaming lore, character stories, and PC optimization. Context: {history}\nUser: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error("Connection glitch! Try again.")

# --- 7. قسم فحص المواصفات (أسفل الشاشة) ---
with st.expander(t['specs']):
    c1, c2 = st.columns(2)
    hw = c1.text_input("Hardware:", placeholder="e.g. Intel HD 4600")
    gm = c2.text_input("Game:", placeholder="e.g. AC Unity")
    if st.button("🚀 Analyze"):
        analysis = model.generate_content(f"Can {hw} run {gm}? FPS boost tips in {selected_lang}.")
        st.info(analysis.text)
