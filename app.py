import streamlit as st
import google.generativeai as genai

# پیج سیٹنگز
st.set_page_config(page_title="المحقّق AI - عالمی ریسرچ انجن", layout="wide")

# اردو فونٹ اور ڈیزائن
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; font-family: 'Jameel Noori Nastaleeq', 'Noto Sans Arabic', sans-serif; }
    div.stButton > button { width: 100%; border-radius: 10px; background-color: #1e3a8a; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔍 المحقّق AI: جامع علمی و تحقیقی مرکز")

with st.sidebar:
    st.header("⚙️ ریسرچ کنٹرول پینل")
    api_key = st.text_input("Gemini API Key درج کریں:", type="password")
    
    st.markdown("---")
    st.write("### 🚀 خصوصی فیچرز:")
    st.info("""
    1. **ملٹی فائل ریسرچ:** ایک ساتھ کئی کتب میں تلاش۔
    2. **عالمی سرچ:** ویب پر موجود ہر زبان کی کتب تک رسائی۔
    3. **نسخوں کا موازنہ:** مختلف پبلشرز اور ایڈیشنز کی پہچان۔
    """)

if api_key:
    try:
        genai.configure(api_key=api_key)
        # جدید ترین فلیش ماڈل جو بڑی فائلز اور ویب سرچ کے لیے بہترین ہے
        model = genai.GenerativeModel('gemini-1.5-flash')

        # 1. تحقیق کا ذریعہ منتخب کریں
        source = st.radio("تحقیق کا دائرہ منتخب کریں:", 
                          ["میری لائبریری (ملٹی فائل اپ لوڈ)", "عالمی ویب سرچ و ڈیجیٹل کتب"])

        user_files = []
        if source == "میری لائبریری (ملٹی فائل اپ لوڈ)":
            user_files = st.file_uploader("ایک یا زائد کتابیں (PDF) منتخب کریں:", type=['pdf'], accept_multiple_files=True)
            if user_files:
                st.success(f"مجموعی طور پر {len(user_files)} فائلیں منتخب کی گئی ہیں۔")

        # 2. سوال اور مخصوص ہدایات
        query = st.text_area("آپ کا سوال (مثلاً: فلان پبلشر کے نسخے میں یہ مسئلہ کہاں ہے؟)", height=150)
        
        # ایڈوانس آپشنز
        col1, col2 = st.columns(2)
        with col1:
            publisher = st.text_input("مخصوص پبلشر (اختیاری):")
        with col2:
            edition = st.text_input("مخصوص جلد یا سال (اختیاری):")

        if st.button("جامع تحقیق شروع کریں"):
            if not query:
                st.error("براہِ کرم اپنا سوال درج کریں۔")
            else:
                with st.spinner("المحقّق AI ہزاروں صفحات اور ویب لنکس کو کھنگال رہا ہے..."):
                    # اے آئی کے لیے خصوصی ہدایات
                    system_instr = f"""آپ ایک عالمی سطح کے اسلامی محقق اور لائبریرین ہیں۔ 
                    آپ کا کام صارف کو مستند حوالہ فراہم کرنا ہے۔ 
                    جواب میں درج ذیل تفصیل لازمی ہو:
                    - کتاب کا نام، مصنف، پبلشر، جلد اور صفحہ نمبر۔
                    - اگر انٹرنیٹ پر اس کتاب کے مختلف نسخے (طبع) موجود ہیں تو ان کا ذکر کریں اور بتائیں کہ کس نسخے میں کیا فرق ہے۔
                    - اگر صارف نے مخصوص پبلشر ({publisher}) پوچھا ہے تو ترجیحاً اسی کا حوالہ دیں۔
                    - زبان کوئی بھی ہو، جواب اردو میں جامع تحقیقی انداز میں دیں۔"""

                    try:
                        if source == "میری لائبریری (ملٹی فائل اپ لوڈ)" and user_files:
                            # تمام فائلوں کو ایک ساتھ پروسیس کرنا
                            content_list = []
                            for file in user_files:
                                content_list.append({"mime_type": "application/pdf", "data": file.read()})
                            content_list.append(system_instr + "\n" + query)
                            response = model.generate_content(content_list)
                        else:
                            # عالمی ویب سرچ
                            full_prompt = f"{system_instr} \n سوال: {query} \n پبلشر: {publisher} \n ایڈیشن: {edition}"
                            response = model.generate_content(full_prompt)

                        st.markdown("### 📜 تحقیقی رپورٹ:")
                        st.markdown(response.text)
                        
                    except Exception as e:
                        st.error(f"تحقیق کے دوران خرابی: {str(e)}")
                        st.info("مشورہ: اگر '400' ایرر آئے تو اپنی API Key چیک کریں یا فائل کا سائز کم کریں۔")

    except Exception as e:
        st.error(f"سسٹم کنکشن ایرر: {e}")
else:
    st.warning("تحقیق شروع کرنے کے لیے سائیڈ بار میں اپنی 'Gemini API Key' درج کریں۔")
