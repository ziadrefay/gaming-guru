import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="Gaming Guru AI | Vision", page_icon="🎮", layout="centered")

# 2. كود التصميم (الـ CSS بتاعنا مع إضافة ستايل لرفع الصور)
st.markdown("""
    <style>
    .stApp { background: #0a0a0a; color: #ffffff; }
    .main-title {
        font-family: 'Orbitron', sans-serif;
        color: #00ffcc;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        text-shadow: 0 0 10px #00ffcc;
        margin-bottom: 20px;
    }
    .stFileUploader section {
        background-color: #1a1a1a !important;
        border: 2px dashed #00ffcc !important;
        border-radius: 15px !important;
    }
    .stButton>button {
        background: linear-gradient(45deg, #00ffcc, #0099ff) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">GAMING GURU VISION AI</p>', unsafe_allow_html=True)

# 3. إعداد الـ API
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("تأكد من وضع GEMINI_API_KEY في Secrets")

# 4. قسم رفع الصور
st.write("📸 *ارفع صورة من اللعبة (سكرين شوت) ودع الخبير يحللها:*")
uploaded_file = st.file_uploader("اختار صورة...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='الصورة المرفوعة', use_column_width=True)

# 5. قسم السؤال النصي
user_query = st.text_input("ماذا تريد أن تعرف عن هذه الصورة أو اللعبة؟")

if st.button("تحليل بواسطة الذكاء الاصطناعي"):
    if user_query:
        with st.spinner('جاري فحص الصورة والبيانات...'):
            try:
                # استخدام موديل الفلاش لأنه سريع جداً في الصور
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                if uploaded_file:
                    # إذا كانت هناك صورة، نرسلها مع النص
                    response = model.generate_content([user_query, image])
                else:
                    # إذا لم تكن هناك صورة، نرسل النص فقط
                    response = model.generate_content(user_query)
                
                st.markdown("### 📝 تحليل الخبير:")
                st.write(response.text)
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
    else:
        st.warning("اكتب سؤالك عشان الخبير يقدر يساعدك!")

# القائمة الجانبية
with st.sidebar:
    st.title("🚀 مميزات Vision")
    st.write("- حل ألغاز الألعاب بالصور.")
    st.write("- تحليل إعدادات الجرافيك.")
    st.write("- التعرف على الشخصيات والأماكن.")
    st.markdown("---")
    st.write("وضع الكمبيوتر: *HP EliteDesk Optimized* 🖥️")