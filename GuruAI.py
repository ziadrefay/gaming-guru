import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="Gemly AI Ultra", page_icon="🎮", layout="wide")

# --- 2. كود الـ CSS والـ JavaScript (إظهار الزرار وتحسين الشكل) ---
st.markdown("""
    <style>
        /* إخفاء الهيدر والفوتر تماماً */
        header {visibility: hidden !important; height: 0px !important;}
        .stDeployButton {display:none !important;}
        footer {visibility: hidden !important;}

        /* تصميم زرار القائمة الجانبية المخصص */
        .custom-sidebar-toggle {
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 999999;
            background: #0a0a0a;
            border: 2px solid #00ffcc;
            color: #00ffcc;
            padding: 10px 15px;
            border-radius: 12px;
            cursor: pointer;
            font-weight: bold;
            box-shadow: 0 0 15px #00ffcc;
            transition: 0.3s;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .custom-sidebar-toggle:hover {
            background: #00ffcc;
            color: #000;
            box-shadow: 0 0 25px #00ffcc;
        }

        /* تنسيق خلفية التطبيق */
        .stApp {
            background: radial-gradient(circle at top, #1a1a1a 0%, #0a0a0a 100%);
            color: #ffffff;
        }

        /* تصميم كروت المحادثة */
        .stChatMessage {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(0, 255, 204, 0.2) !important;
            border-radius: 20px !important;
            backdrop-filter: blur(10px);
            margin-bottom: 15px !important;
        }

        /* عنوان النيون الكبير */
        .neon-title {
            color: #00ffcc;
            text-align: center;
            font-size: 55px;
            font-weight: 900;
            text-shadow: 0 0 20px #00ffcc;
            margin-bottom: 5px;
        }
    </style>

    <script>
        // كود لفتح القائمة الجانبية برمجياً عند الضغط على الزرار المخصص
        function toggleSidebar() {
            const sidebarButton = window.parent.document.querySelector('button[data-testid="stSidebarCollapseButton"]');
            if (sidebarButton) {
                sidebarButton.click();
            } else {
                // إذا كان الزرار الأصلي غير موجود، نحاول فتحه بطريقة بديلة
                const openButton = window.parent.document.querySelector('button[aria-label="Open sidebar"]');
                if (openButton) openButton.click();
            }
        }
    </script>
    
    <div class="custom-sidebar-toggle" onclick="toggleSidebar()">
        <span>☰</span> <span>MENU</span>
    </div>
""", unsafe_allow_html=True)

# --- 3. تهيئة الذاكرة واللغات ---
if "messages" not in st.session_state:
    st.session_state.messages = []

languages = {
    "العربية": {
        "title": "GEMLY AI",
        "subtitle": "خبير الألعاب والذكاء الاصطناعي",
        "clear": "🗑️ مسح الشات",
        "placeholder": "اسأل Gemly أي حاجة...",
        "specs": "💻 فحص المواصفات"
    },
    "English": {
        "title": "GEMLY AI",
        "subtitle": "Gaming & Tech Expert AI",
        "clear": "🗑️ Clear Chat",
        "placeholder": "Ask Gemly anything...",
        "specs": "💻 Specs Check"
    }
}

# --- 4. القائمة الجانبية ---
with st.sidebar:
    st.markdown("<h1 style='color:#00ffcc;'>🎮 GEMLY PANEL</h1>", unsafe_allow_html=True)
    lang_choice = st.selectbox("🌐 Language", ["العربية", "English"])
    t = languages[lang_choice]
    
    st.markdown("---")
    if st.button(t["clear"]):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.write("👨‍💻 Dev: Ziad Zaza")

# --- 5. إعداد الموديل ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # استخدمنا 1.5 فلاش لأنه الأفضل في تذكر المحادثات (Chat History)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("API Key Missing!")

# --- 6. الواجهة الرئيسية ---
st.markdown(f'<p class="neon-title">{t["title"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align:center; opacity:0.8;">{t["subtitle"]}</p>', unsafe_allow_html=True)

# عرض تاريخ المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال الشات الجديد
if prompt := st.chat_input(t["placeholder"]):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # تجميع الذاكرة لإرسالها للموديل
                history = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages]
                response = model.generate_content(f"Role: Pro Gaming Assistant. Response Language: {lang_choice}. Context: {history}")
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error("Connection Error!")

# --- 7. قسم فحص المواصفات ---
with st.expander(t["specs"]):
    hw = st.text_input("CPU/GPU:")
    gm = st.text_input("Game:")
    if st.button("Check"):
        res = model.generate_content(f"Can {hw} run {gm}? FPS tips?")
        st.write(res.text)
