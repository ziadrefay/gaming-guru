import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Gemly AI | World Edition", page_icon="💎", layout="wide")

# --- 2. كود الـ CSS الأسطوري (التأثيرات الجمالية) ---
st.markdown("""
    <style>
        /* إخفاء الهيدر مع الحفاظ على السهم */
        header[data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; }
        button[data-testid="stSidebarCollapseButton"] {
            background-color: #00ffcc !important; color: #000 !important;
            border-radius: 50% !important; box-shadow: 0 0 15px #00ffcc !important;
            z-index: 1000;
        }

        /* الخلفية المتحركة والجرافيك */
        .stApp {
            background: linear-gradient(135deg, #050505 0%, #111 50%, #050505 100%);
            color: #ffffff;
        }

        /* العنوان النيون الأسطوري */
        .neon-title {
            color: #00ffcc;
            text-align: center;
            font-size: 70px;
            font-weight: 900;
            text-shadow: 0 0 20px #00ffcc, 0 0 40px #0099ff;
            margin-top: -50px;
            animation: neon-glow 3s infinite alternate;
        }
        
        @keyframes neon-glow {
            from { text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc; }
            to { text-shadow: 0 0 30px #00ffcc, 0 0 60px #0099ff; }
        }

        /* شعار الجيمرز */
        .tagline {
            color: #00ffcc;
            text-align: center;
            font-size: 18px;
            letter-spacing: 4px;
            margin-top: -20px;
            margin-bottom: 40px;
            opacity: 0.8;
            font-style: italic;
        }

        /* تنسيق فقاعات الشات الزجاجية */
        [data-testid="stChatMessage"] {
            background: rgba(255, 255, 255, 0.05) !important;
            border-left: 5px solid #00ffcc !important;
            border-radius: 15px !important;
            backdrop-filter: blur(15px);
            margin-bottom: 15px !important;
            transition: 0.3s;
        }
        [data-testid="stChatMessage"]:hover {
            transform: translateX(10px);
            background: rgba(255, 255, 255, 0.08) !important;
        }

        /* تعديل السايدبار */
        section[data-testid="stSidebar"] {
            background-color: #050505 !important;
            border-right: 2px solid #00ffcc33;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. نظام جميع لغات العالم ---
all_languages = [
    "Arabic (العربية)", "English", "Spanish (Español)", "French (Français)", 
    "German (Deutsch)", "Japanese (日本語)", "Korean (한국어)", "Russian (Русский)",
    "Portuguese", "Italian", "Turkish", "Chinese", "Hindi", "Urdu"
] # يمكنك إضافة أي لغة هنا، الـ AI سيفهمها تلقائياً

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. القائمة الجانبية (The Control Center) ---
with st.sidebar:
    st.markdown("<h1 style='color:#00ffcc; text-align:center;'>🕹️ GEMLY HUB</h1>", unsafe_allow_html=True)
    selected_lang = st.selectbox("🌐 Choose Language / اختر اللغة", all_languages)
    st.markdown("---")
    
    # رفع الصور لتحليلها
    st.markdown("### 🖼️ Gameplay Scanner")
    uploaded_image = st.file_uploader("Upload screenshot to analyze", type=["jpg", "png", "jpeg"])
    
    st.markdown("---")
    if st.button("🗑️ Clear Matrix Archive"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.write("💎 **V 3.0 Ultra Pro**")
    st.write("👨‍💻 **Dev:** Ziad Zaza")

# --- 5. إعداد الموديل (Gemini 1.5 Flash - الأفضل للصور والشات) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key Missing!")

# --- 6. الواجهة الرئيسية ---
st.markdown('<p class="neon-title">GEMLY AI</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">Built by a gamer, for gamers</p>', unsafe_allow_html=True)

# عرض الشات القديم
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة إدخال الشات
if prompt := st.chat_input("Ask Gemly anything..."):
    # إضافة سؤال المستخدم للذاكرة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # رد الـ AI
    with st.chat_message("assistant"):
        with st.spinner("🎮 Processing Data..."):
            try:
                history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                
                # إعداد المحتوى (نص + صورة لو موجودة)
                content_to_send = [f"You are Gemly AI, a legendary gaming expert. Respond in {selected_lang}. Context: {history}\nUser: {prompt}"]
                
                if uploaded_image:
                    img = Image.open(uploaded_image)
                    content_to_send.append(img)
                
                response = model.generate_content(content_to_send)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("Matrix Glitch! Check Connection.")

# --- 7. أداة تحليل الأداء (Premium Expander) ---
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("🛠️ PERFORMANCE ANALYZER & FPS BOOSTER"):
    col1, col2 = st.columns(2)
    with col1: specs = st.text_input("Your Hardware:", placeholder="e.g. RTX 3060, 16GB RAM")
    with col2: game_name = st.text_input("Game Title:", placeholder="e.g. Cyberpunk 2077")
    
    if st.button("ANALYZE PERFORMANCE 🚀"):
        if specs and game_name:
            res = model.generate_content(f"Analyze performance for {game_name} on {specs}. Best settings for 60FPS in {selected_lang}.")
            st.info(res.text)
