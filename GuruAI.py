import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الصفحة (تظهر في المتصفح)
st.set_page_config(
    page_title="Gaming Guru AI | Vision & Chat",
    page_icon="🎮",
    layout="centered"
)

# 2. تصميم الـ CSS الاحترافي (الستايل اللي بتحبه)
st.markdown("""
    <style>
    .stApp { background: #0a0a0a; color: #ffffff; }
    .main-title {
        font-family: 'Orbitron', sans-serif;
        color: #00ffcc;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
        margin-bottom: 20px;
    }
    .stTextInput>div>div>input, .stFileUploader section {
        background-color: #1a1a1a !important;
        border: 2px solid #00ffcc !important;
        border-radius: 15px !important;
        color: #00ffcc !important;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #00ffcc, #0099ff) !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        transition: 0.5s;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4);
    }
    .stButton>button:hover {
        box-shadow: 0 0 30px #00ffcc !important;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إعداد الـ API من الـ Secrets (للأمان)
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        # استخدام الموديل الحديث الذي يدعم الصور والنصوص
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("⚠️ خطأ: لم يتم العثور على GEMINI_API_KEY في Secrets.")
        st.stop()
except Exception as e:
    st.error(f"❌ مشكلة في الاتصال بالـ API: {e}")
    st.stop()

# 4. واجهة المستخدم
st.markdown('<p class="main-title">GAMING GURU VISION AI</p>', unsafe_allow_html=True)
st.write("🤖 مساعدك الذكي لحل المهام، تحليل الصور، وتطوير أداء جهازك.")

# قسم رفع الصور (اختياري)
st.markdown("---")
uploaded_file = st.file_uploader("📸 ارفع سكرين شوت من اللعبة (اختياري):", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='المعطيات البصرية جاهزة للتحليل', use_column_width=True)

# قسم السؤال النصي
user_query = st.text_input("💬 اسأل الخبير عن أي شيء (مهمة صعبة، إعدادات FPS، قصة لعبة):")

if st.button("🚀 تحليل بواسطة الذكاء الاصطناعي"):
    if user_query:
        with st.spinner('جاري استدعاء الخبرات القتالية وفحص البيانات...'):
            try:
                # دمج تعليمات النظام مع سؤال المستخدم
                system_prompt = f"أنت خبير ألعاب محترف. ساعد المستخدم في سؤاله بكل حماس ودقة: {user_query}"
                
                if uploaded_file:
                    # لو فيه صورة بيبعتها للموديل مع النص
                    response = model.generate_content([system_prompt, image])
                else:
                    # لو مفيش صورة بيبعت نص بس
                    response = model.generate_content(system_prompt)
                
                st.markdown("### 💡 نصيحة الخبير:")
                st.info(response.text)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء التوليد: {e}")
    else:
        st.warning("يا بطل، اكتب سؤالك الأول!")

# القائمة الجانبية
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/681/681392.png", width=100)
    st.title("إعدادات Guru")
    st.write("**الحالة:** متصل بالرادار 🟢")
    st.write("**الموديل:** Gemini 1.5 Flash")
    st.markdown("---")
    st.write("🔧 تم التطوير بواسطة زيزو")
    st.write("🖥️ Optimized for: *HP EliteDesk*")
