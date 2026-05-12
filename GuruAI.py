import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. التصميم البسيط (Cyberpunk Style)
st.set_page_config(page_title="Gaming Guru AI", page_icon="🎮")

st.markdown("""
    <style>
    .stApp { background-color: #0a0a0a; color: #00ffcc; }
    input { background-color: #1a1a1a !important; color: #00ffcc !important; border: 1px solid #00ffcc !important; }
    .stButton>button { background: linear-gradient(45deg, #00ffcc, #0099ff); color: black; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎮 GAMING GURU VISION AI")
st.write("ارفع سكرين شوت من اللعبة واسأل الخبير!")

# 2. الربط السهل (بدون تعقيد)
if "GEMINI_API_KEY" in st.secrets:
    # هنا بقى السر الصغير اللي هيشغله
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # بنستخدم gemini-1.5-flash لأنه الأسرع والأخف حالياً
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("حط الـ API Key في الـ Secrets يا بطل!")

# 3. واجهة الرفع والسؤال
uploaded_file = st.file_uploader("📸 ارفع صورة اللعبة هنا:", type=["jpg", "png", "jpeg"])
user_query = st.text_input("💬 عايز تعرف إيه؟")

if st.button("🚀 اسأل الخبير"):
    if user_query:
        with st.spinner('بفحص البيانات...'):
            try:
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    # إرسال الصورة مع النص مباشرة
                    response = model.generate_content([user_query, img])
                else:
                    response = model.generate_content(user_query)
                
                st.markdown("### 💡 رد الجورو:")
                st.success(response.text)
            except Exception as e:
                # لو لسه فيه مشكلة في النسخة، السطر ده هيقولنا فين بالظبط
                st.error(f"حصلت مشكلة صغيرة: {e}")
    else:
        st.warning("اكتب سؤالك الأول!")
