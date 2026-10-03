import streamlit as st
import time
import pypdf
import io
from openai import OpenAI

# إعدادات صفحة الويب
st.set_page_config(
    page_title="Scinapse Agent - وكيل الأبحاث العلمية",
    page_icon="🔬",
    layout="wide"
)

# عنوان التطبيق الواجهة
st.title("🔬 Scinapse Agent: مساعدك الذكي للأبحاث العلمية")
st.markdown("""
مرحباً بكِ! هذا النظام مصمم لمساعدة الباحثين والطلاب في تحليل الأوراق البحثية، استخراج المعادلات، واكتشاف الفجوات العلمية باستخدام قوة **NVIDIA & Nebius AI**.
""")

# شريط جانبي لإدخال مفتاح الـ API أو إعدادات الوكيل
st.sidebar.header("إعدادات الوكيل ⚙️")
api_key = st.sidebar.text_input("أدخل مفتاح Nebius / NVIDIA API Key", type="password")

selected_task = st.sidebar.selectbox(
    "اختر مهمة الوكيل:",
    ["تلخيص وتصفية الأبحاث", "استخراج وشرح المعادلات الفيزيائية/رياضية", "اكتشاف الفجوات البحثية الجديدة"]
)

# صندوق ادخال النص أو رفع الملفات
st.subheader("إدخال البيانات البحثية")
research_input = st.text_area("اكتب عنوان البحث، أو الصق ملخص الورقة البحثية هنا:", 
                             placeholder="مثال: دراسة سلوك الإلكترونات في المواد النانوية...")

uploaded_file = st.file_uploader("أو ارفع ملف الورقة البحثية (PDF أو TXT):", type=["pdf", "txt"])

# دالة استخراج النص من ملف PDF أو النص العادي
def extract_file_content(file):
    if file is None:
        return ""
    content = ""
    if file.name.endswith('.pdf'):
        try:
            reader = pypdf.PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    content += text + "\n"
        except Exception as e:
            st.error(f"حدث خطأ أثناء قراءة ملف الـ PDF: {e}")
    elif file.name.endswith('.txt'):
        try:
            content = file.getvalue().decode("utf-8")
        except Exception as e:
            st.error(f"حدث خطأ أثناء قراءة الملف النصي: {e}")
    return content

# زر التنفيذ
if st.button("تشغيل الوكيل الذكي 🚀"):
    if not api_key:
        st.warning("⚠️ الرجاء إدخال مفتاح الـ API في الشريط الجانبي أولاً.")
    elif not research_input and not uploaded_file:
        st.warning("⚠️ الرجاء كتابة نص البحث أو رفع ملف لتتمكن الوكلاء من تحليله.")
    else:
        with st.spinner("جاري قراءة الملف ومعالجة البيانات بواسطة وكلاء الذكاء الاصطناعي..."):
            
            # استخراج محتوى الملف المرفوع إن وجد
            file_content = extract_file_content(uploaded_file)
            
            # دمج مدخلات المستخدم مع محتوى الملف
            full_context = f"معلومات البحث المكتوبة:\n{research_input}\n\nمحتوى الملف المرفوع:\n{file_content}"
            
            # تحديد البرومبت بناءً على المهمة المختارة
            if selected_task == "تلخيص وتصفية الأبحاث":
                prompt = f"قم بتلخيص وتصفية الأبحاث التالية في نقاط رئيسية واضحة، مع ذكر النتائج الأساسية والتوصيات:\n\n{full_context}"
            elif selected_task == "استخراج وشرح المعادلات الفيزيائية/رياضية":
                prompt = f"قم باستخراج المعادلات الفيزيائية أو الرياضية الموجودة في النص واشرح كل معادلة بالتفصيل:\n\n{full_context}"
            else:
                prompt = f"بناءً على النص المرفق، قم باكتشاف الفجوات البحثية واقترح أفكاراً لأبحاث مستقبلية:\n\n{full_context}"

            try:
                # الاتصال بالـ API (متوافق مع Nebius / NVIDIA / OpenAI)
                client = OpenAI(
                    base_url="https://api.studio.nebius.ai/v1/", # يمكنك تعديل الرابط حسب مزود الخدمة لو لزم الأمر
                    api_key=api_key
                )
                
                response = client.chat.completions.create(
                    model="meta-llama/Llama-3-70B-Instruct", # يمكنك تغيير النموذج حسب المتاح لديك
                    messages=[
                        {"role": "system", "content": "أنت مساعد بحثي أكاديمي ذكي متخصص في تحليل الأوراق العلمية والفيزياء."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
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
