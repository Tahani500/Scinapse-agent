import streamlit as st
from google import genai
from pypdf import PdfReader

# إعدادات صفحة الويب
st.set_page_config(
    page_title="Scinapse Agent - مساعد الأبحاث الذكي",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 مساعدك الدحي للأبحاث العلمية (Gemini)")
st.markdown("""
مرحباً بكِ! هذا النظام مصمم لمساعدة الباحثين والطلاب في تحليل الأوراق البحثية واستخراج النتائج بدقة باستخدام **Google Gemini**.
""")

# شريط جانبي لإدخال مفتاح الـ API
st.sidebar.header("إعدادات الوكيل ⚙️")
api_key = st.sidebar.text_input("أدخل مفتاح Gemini API Key:", type="password")

selected_task = st.sidebar.selectbox(
    "اختر مهمة الوكيل:",
    ["تلخيص وتصفية الأبحاث", "استخراج وشرح المعادلات الفيزيائية/الرياضية", "اكتشاف الفجوات البحثية الجديدة"]
)

# خيارات الإدخال
st.subheader("إدخال البيانات البحثية")
input_method = st.radio("اختر طريقة الإدخال:", ["رفع ملف PDF 📄", "كتابة أو لصق النص ✍️"])

research_input = ""

if input_method == "رفع ملف PDF 📄":
    uploaded_file = st.file_uploader("قم برفع ملف الـ PDF الخاص بالبحث:", type=["pdf"])
    if uploaded_file is not None:
        try:
            reader = PdfReader(uploaded_file)
            extracted_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
            
            if extracted_text.strip():
                research_input = extracted_text
                st.success(f"✅ تم قراءة الملف بنجاح! (عدد الصفحات: {len(reader.pages)})")
            else:
                research_input = "بحث في الفيزياء والعلوم."
                st.warning("⚠️ ملاحظة: الملف لا يحتوي على نصوص قابلة للقراءة المباشرة، سنعتمد على العنوان والعوامل العامة.")
        except Exception as e:
            research_input = "بحث في الفيزياء."
            st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
else:
    research_input = st.text_area("الصق محتوى البحث أو ملخصه هنا:", 
                                 placeholder="مثال: دراسة سلوك الإلكترونات...")

# زر التنفيذ
if st.button("تشغيل الوكيل الذكي 🚀"):
    if not api_key:
        st.warning("⚠️ الرجاء إدخال مفتاح الـ API في الشريط الجانبي أولاً.")
    else:
        if not research_input.strip():
            research_input = "تحليل الأوراق البحثية العلمية."

        with st.spinner("جاري التحليل بواسطة Gemini..."):
            
            if selected_task == "تلخيص وتصفية الأبحاث":
                prompt = f"قم بتلخيص وتصفية النص التالي في نقاط رئيسية واضحة مع النتائج والتوصيات:\n\n{research_input}"
            elif selected_task == "استخراج وشرح المعادلات الفيزيائية/الرياضية":
                prompt = f"قم باستخراج المعادلات الموجودة في النص واشرح كل معادلة بالتفصيل:\n\n{research_input}"
            else:
                prompt = f"بناءً على النص المرفق، اكتشف الفجوات البحثية واقترح أفكاراً لأبحاث مستقبلية:\n\n{research_input}"

            try:
                client = genai.Client(api_key=api_key.strip())
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=prompt,
                )
                
                st.success("✨ تم إتمام التحليل بنجاح!")
                st.markdown("### 📊 نتيجة تحليل الوكيل:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالـ API: {e}")

st.markdown("---")
st.caption("مشروع مشارك - مدعوم بـ Google Gemini")
