import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

# إعدادات صفحة الويب
st.set_page_config(
    page_title="Scinapse Agent - وكيل الأبحاث العلمية",
    page_icon="🔬",
    layout="wide"
)

# عنوان التطبيق الواجهة
st.title("🔬 Scinapse Agent: مساعدك الذكي للأبحاث العلمية")
st.markdown("""
مرحباً بكِ! هذا النظام مصمم لمساعدة الباحثين والطلاب في تحليل الأوراق البحثية، استخراج المعادلات، واكتشاف الفجوات العلمية باستخدام قوة **NVIDIA AI**.
""")

# شريط جانبي لإدخال مفتاح الـ API أو إعدادات الوكيل
st.sidebar.header("إعدادات الوكيل ⚙️")
api_key = st.sidebar.text_input("أدخل مفتاح NVIDIA API Key (يبدأ بـ nvapi-)", type="password")

selected_task = st.sidebar.selectbox(
    "اختر مهمة الوكيل:",
    ["تلخيص وتصفية الأبحاث", "استخراج وشرح المعادلات الفيزيائية/الرياضية", "اكتشاف الفجوات البحثية الجديدة"]
)

# خيارات الإدخال: رفع ملف PDF أو كتابة النص مباشرة
st.subheader("إدخال البيانات البحثية")
input_method = st.radio("اختر طريقة الإدخال:", ["رفع ملف PDF 📄", "كتابة أو لصق النص ✍️"])

research_input = ""

if input_method == "رفع ملف PDF 📄":
    uploaded_file = st.file_uploader("قم بتحديث أو رفع ملف الـ PDF الخاص بالبحث:", type=["pdf"])
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
                st.warning("⚠️ عذراً، لم نتمكن من استخراج نص واضح من هذا الملف. جرب ملفاً آخر أو استخدم خيار لصق النص.")
        except Exception as e:
            st.error(f"حدث خطأ أثناء قراءة ملف الـ PDF: {e}")
else:
    research_input = st.text_area("الصق محتوى البحث أو ملخصه هنا:", 
                                 placeholder="مثال: دراسة سلوك الإلكترونات في المواد النانوية...")

# زر التنفيذ
if st.button("تشغيل الوكيل الذكي 🚀"):
    if not api_key:
        st.warning("⚠️ الرجاء إدخال مفتاح الـ API في الشريط الجانبي أولاً.")
    elif not research_input.strip():
        st.warning("⚠️ الرجاء رفع ملف PDF يحتوي على نصوص أو لصق نص البحث في الخانة المخصصة لتحليله.")
    else:
        with st.spinner("جاري معالجة البيانات وتحليلها بواسطة وكلاء الذكاء الاصطناعي..."):
            
            # تحديد البرومبت بناءً على المهمة المختارة
            if selected_task == "تلخيص وتصفية الأبحاث":
                prompt = f"قم بتلخيص وتصفية الأبحاث أو النص التالي في نقاط رئيسية واضحة، مع ذكر النتائج الأساسية والتوصيات:\n\n{research_input}"
            elif selected_task == "استخراج وشرح المعادلات الفيزيائية/الرياضية":
                prompt = f"قم باستخراج المعادلات الفيزيائية أو الرياضية الموجودة في النص واشرح كل معادلة بالتفصيل:\n\n{research_input}"
            else:
                prompt = f"بناءً على النص المرفق، قم باكتشاف الفجوات البحثية واقترح أفكاراً لأبحاث مستقبلية:\n\n{research_input}"

            try:
                # الاتصال بـ NVIDIA NIM API باستخدام نموذج مستقر وخاضع للدعم المستمر
                client = OpenAI(
                    base_url="https://integrate.api.nvidia.com/v1",
                    api_key=api_key
                )
                
                response = client.chat.completions.create(
                    model="mistralai/mixtral-8x7b-instruct-v0.1",
                    messages=[
                        {"role": "system", "content": "أنت مساعد بحثي أكاديمي ذكي متخصص في تحليل الأوراق العلمية والفيزياء."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1024
                )
                
                result_text = response.choices[0].message.content
                
                st.success("✨ تم إتمام التحليل بنجاح!")
                st.markdown("### 📊 نتيجة تحليل الوكيل:")
                st.write(result_text)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالـ API أو معالجة الطلب: {e}")

# ملاحظة أسفل الصفحة
st.markdown("---")
st.caption("مشروع مشارك في Nebius x NVIDIA Global AI Hackathon")
