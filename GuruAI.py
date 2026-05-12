import streamlit as st
import google.generativeai as genai

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Gaming Guru AI", page_icon="🎮", layout="wide")

# --- إعداد الـ AI (Gemini) ---
# حط الـ API Key بتاعك هنا
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

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
    model_name="gemini-3.1-flash-lite",
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

# --- إضافة هذا الجزء داخل قسم القائمة الجانبية (with st.sidebar) ---

st.markdown("---")
st.subheader("📰 مركز أخبار الجيمز")
if st.button("🔥 هات لي آخر الأخبار"):
    with st.spinner('جاري مسح الرادارات بحثاً عن أخبار...'):
        try:
            # هنا بنطلب من الموديل يجيب أخبار حقيقية (Gemini 1.5 عنده وصول لمعلومات حديثة)
            news_prompt = "أعطني ملخصاً لأهم 3 أخبار في عالم الألعاب اليوم (عالمياً وعربياً). رتبها بنقاط، واجعل الأسلوب حماسي وجذاب للجيمرز."
            news_response = model.generate_content(news_prompt)
            
            # عرض الأخبار في نافذة منبثقة أو في الجنب
            st.info(news_response.text)
        except Exception as e:
            st.error(f"عذراً، الرادار معطل حالياً: {e}")

# --- يمكنك أيضاً إضافة "شريط إخباري" صغير في الشاشة الرئيسية ---

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









import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والتصميم (العنوان اللي بيظهر في جوجل والستايل)
st.set_page_config(
    page_title="Gaming Guru AI | خبير الألعاب",
    page_icon="🎮",
    layout="centered"
)

# 2. كود التصميم الاحترافي (CSS)
st.markdown("""
    <style>
    /* خلفية الموقع بالكامل */
    .stApp {
        background: #0a0a0a;
        color: #ffffff;
    }
    
    /* تصميم العنوان الرئيسي مع تأثير توهج */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        color: #00ffcc;
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
        margin-bottom: 30px;
    }

    /* تصميم صناديق الإدخال */
    .stTextInput>div>div>input {
        background-color: #1a1a1a !important;
        color: #00ffcc !important;
        border: 2px solid #00ffcc !important;
        border-radius: 15px !important;
        padding: 10px 20px !important;
    }

    /* تصميم الأزرار (Neon Button) */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #00ffcc, #0099ff) !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 15px !important;
        transition: 0.5s !important;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4);
    }

    .stButton>button:hover {
        box-shadow: 0 0 30px #00ffcc !important;
        transform: translateY(-3px);
    }

    /* تصميم استجابة الذكاء الاصطناعي */
    .stAlert {
        background-color: rgba(0, 255, 204, 0.1) !important;
        border: 1px solid #00ffcc !important;
        color: #ffffff !important;
        border-radius: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. واجهة المستخدم (UI)
st.markdown('<p class="main-title">GAMING GURU AI</p>', unsafe_allow_html=True)
st.subheader("🤖 مساعدك الذكي لتطوير الأداء وحل المهام الصعبة")

# الحصول على الـ API Key من الـ Secrets (الأمان)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("خطأ: لم يتم العثور على API Key في إعدادات Secrets")

# مكان السؤال
user_input = st.text_input("اسأل خبير الألعاب عن أي شيء (مهام، جرافيك، FPS)...")

if st.button("إرسال السؤال"):
    if user_input:
        with st.spinner('جاري استدعاء الخبرات القتالية...'):
            try:
                model = genai.GenerativeModel('gemini-3.1-flash-lite')
                # إضافة "برومبت" سري لجعل الردود جيمينج أكتر
                prompt = f"أنت خبير ألعاب محترف جداً، ساعد المستخدم في سؤاله: {user_input}"
                response = model.generate_content(prompt)
                st.markdown(f"### 💡 نصيحة الخبير:")
                st.write(response.text)
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
    else:
        st.warning("من فضلك اكتب سؤالك أولاً!")

# إضافة Sidebar (القائمة الجانبية)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/681/681392.png", width=100)
    st.title("إعدادات المساعد")
    st.info("هذا المساعد مخصص للاعبين المحترفين على أجهزة PC و Console.")
    st.markdown("---")
    st.write("🔧 تم التطوير بواسطة: *Ziad&Gaming Guru Team*")




import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="Gaming Guru AI", page_icon="🎮", layout="wide")

# 2. قاموس اللغات (تقدر تضيف لغات تانية هنا بسهولة)
languages = {
    "العربية": {
        "title": "🚀 Gaming Guru: مساعدك الذكي",
        "subtitle": "خبير الألعاب الأول لتطوير الأداء وحل المهام",
        "sidebar_title": "⚙️ الإعدادات",
        "lang_label": "اختر اللغة",
        "input_label": "اسأل الجورو عن أي شيء (مهام، جرافيك، FPS)...",
        "button": "إرسال السؤال",
        "news_btn": "📰 هات لي آخر الأخبار",
        "specs_title": "💻 فحص أداء جهازك",
        "specs_label": "اكتب مواصفات جهازك هنا:",
        "specs_btn": "فحص التوافق",
        "chat_placeholder": "جاري استدعاء الخبرات القتالية..."
    },
    "English": {
        "title": "🚀 Gaming Guru: Your AI Ally",
        "subtitle": "The #1 Gaming Expert for Performance & Walkthroughs",
        "sidebar_title": "⚙️ Settings",
        "lang_label": "Select Language",
        "input_label": "Ask the Guru anything (Tasks, Graphics, FPS)...",
        "button": "Send Question",
        "news_btn": "📰 Get Latest News",
        "specs_title": "💻 PC Performance Check",
        "specs_label": "Enter your PC specs here:",
        "specs_btn": "Check Compatibility",
        "chat_placeholder": "Summoning combat expertise..."
    }
}

# 3. القائمة الجانبية واختيار اللغة
with st.sidebar:
    st.title("🎮 Gaming Guru")
    selected_lang = st.selectbox("🌐 Language / اللغة", list(languages.keys()))
    # استدعاء الكلمات بناءً على اللغة المختارة
    t = languages[selected_lang]
    
    st.markdown("---")
    if st.button(t["news_btn"]):
        st.session_state.show_news = True

# 4. إعداد الـ AI (المفتاح والموديل)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # استخدام نسخة الـ Lite اللي أنت شغال بيها
    model = genai.GenerativeModel(
        model_name="gemini-3.1-flash-lite",
        system_instruction=f"You are Gaming Guru AI. Respond in {selected_lang}. Be enthusiastic and use gaming terminology."
    )
except:
    st.error("API Key Missing!")

# 5. الواجهة الرئيسية
st.title(t["title"])
st.subheader(t["subtitle"])

user_input = st.text_input(t["input_label"])

if if st.button(t["button"], key="main_chat_btn"):
    if user_input:
        with st.spinner(t["chat_placeholder"]):
            try:
                # بنجبر الموديل يلتزم باللغة المختارة في الرد
                response = model.generate_content(f"Answer this in {selected_lang}: {user_input}")
                st.markdown("### 💡 " + ("نصيحة الخبير:" if selected_lang == "العربية" else "Guru's Advice:"))
                st.success(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please type something!")

# 6. قسم مواصفات الجهاز
with st.expander(t["specs_title"]):
    specs = st.text_area(t["specs_label"])
    if st.button(t["specs_btn"]):
        res = model.generate_content(f"Based on these specs: {specs}, can I run {user_input}? Answer in {selected_lang}")
        st.write(res.text)
