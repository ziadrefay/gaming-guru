import streamlit as st
import google.generativeai as genai

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Gaming Guru AI", page_icon="🎮", layout="wide")

# --- إعداد الـ AI (Gemini) ---
# حط الـ API Key بتاعك هنا
genai.configure(api_key="AIzaSyA9kkI1OWlRQNQ5mfa5Aal7BtgvS1KoFo8")

model = genai.GenerativeModel(
    model_name="gemini-3.1-flash-lite",
    system_instruction="""
    أنت 'Gaming Guru AI'، مساعد ذكي متخصص فقط في عالم الألعاب.
    مهامك:
    1. مساعدة اللاعبين في تخطي المراحل الصعبة (Walkthroughs).
    2. شرح قصص الألعاب المعقدة بشكل مشوق.
    3. ترشيح ألعاب مشابهة بناءً على ذوق المستخدم.
    4. تقديم نصائح تقنية لتحسين الأداء (FPS).
    نبرة صوتك: حماسية، خبيرة، وتستخدم مصطلحات الجيمرز.
    """
)

# --- واجهة المستخدم (Sidebar) ---
st.sidebar.title("🎮 Gaming Guru")
st.sidebar.info("مساعدك الذكي في عالم الألعاب")
option = st.sidebar.selectbox(
    "ماذا تحتاج اليوم؟",
    ("تخطي مرحلة صعبة", "شرح قصة لعبة", "ترشيح ألعاب مشابهة", "معلومات تقنية")
)

# --- الشاشة الرئيسية ---
st.title("🚀 Gaming Guru: الـ AI بتاعك في اللعب")

user_input = st.text_input("اكتب اسم اللعبة أو السؤال اللي شاغل بالك:")

if st.button("اسأل الخبير"):
    if user_input:
        with st.spinner('جاري تحليل البيانات من عالم الألعاب...'):
            try:
                # تخصيص البرومبت بناءً على الاختيار
                full_prompt = f"بناءً على تخصصك كـ {option}، أجب عن الآتي: {user_input}"
                response = model.generate_content(full_prompt)
                
                st.subheader("💡 نصيحة الخبير:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
    else:
        st.warning("من فضلك اكتب سؤالك أولاً!")

# --- قسم إضافي لمعلومات الجهاز ---
with st.expander("💻 تأكد من تشغيل اللعبة على جهازك"):
    specs = st.text_area("اكتب مواصفات جهازك (رام، كرت، معالج):")
    if st.button("فحص الأداء"):
        check_prompt = f"هل المواصفات دي {specs} تشغل لعبة {user_input}؟ وإيه أفضل إعدادات؟"
        res = model.generate_content(check_prompt)
        st.write(res.text)





import streamlit as st
import google.generativeai as genai

# --- 1. إعدادات الصفحة الاحترافية ---
st.set_page_config(
    page_title="Gaming Guru AI | خبير الألعاب العالمي",
    page_icon="🎮",
    layout="wide"
)

# --- 2. إعداد الذكاء الاصطناعي (API Key) ---
# ملاحظة: عند الرفع أونلاين سنستخدم st.secrets للأمان
API_KEY = "AIzaSyADHOCEJN548kXlsbZF1AwYctw4L6d6S_o" 
genai.configure(api_key=API_KEY)

# --- 3. تعليمات النظام (التي تجعله عالمياً ودقيقاً) ---
system_instruction = """
أنت 'Gaming Guru AI'، مساعد ذكي متخصص وعالمي في عالم الألعاب.
مهامك الاحترافية:
1. دعم جميع لغات العالم: رد دائماً بنفس اللغة التي يتحدث بها المستخدم.
2. تقديم حلول تقنية دقيقة: (FPS, تحسين الأداء على الأجهزة الضعيفة مثل Intel HD 4600).
3. شرح قصص الألعاب المعقدة وتقديم Walkthroughs للمراحل الصعبة.
4. ترشيح ألعاب بناءً على ذوق المستخدم وجهازه.
نبرة صوتك: حماسية، خبيرة، ودودة، وتستخدم مصطلحات الجيمرز المحترفين.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# --- 4. تصميم الواجهة الاحترافية (UI) ---
st.title("🚀 Gaming Guru AI")
st.markdown("### محرك الذكاء الاصطناعي الأول للجيمرز المحترفين")

# القائمة الجانبية (Sidebar)
with st.sidebar:
    st.image("https://img.icons8.com/fluent/100/000000/gaming-side-view.png")
    st.title("الإعدادات")
    st.info("هذا المساعد يدعم جميع اللغات ويقدم نصائح مخصصة لجهازك.")
    if st.button("مسح المحادثة"):
        st.session_state.messages = []

# تهيئة ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة إدخال المستخدم
if prompt := st.chat_input("اسأل خبير الألعاب عن أي شيء..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # إرسال المحادثة كاملة للـ AI ليتذكر السياق
            response = model.generate_content(prompt)
            full_response = response.text
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"حدث خطأ فني: {e}")