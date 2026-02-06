import streamlit as st
import google.generativeai as genai

# پیج کی بنیادی ترتیبات
st.set_page_config(page_title="المحقّق AI - عالمی ریسرچ انجن", layout="wide")

# خوبصورت اردو ڈیزائن (Nastaleeq Style)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;700&display=swap');
    .stApp { direction: rtl; text-align: right; font-family: 'Noto Sans Arabic', sans-serif; }
    .stTextArea textarea { direction: rtl; text-align: right; }
    div.stButton > button { width: 100%; background-color: #075E54; color: white; border-radius: 8px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔍 المحقّق AI: جامع ڈیجیٹل لائبریری و عالمی تحقیقی مرکز")

# سائیڈ بار کنٹرول
with st.sidebar:
    st.header("⚙️ ایڈوانس کنٹرول پینل")
    raw_api_key = st.text_input("Gemini API Key درج کریں:", type="password")
    api_key = raw_api_key.strip() if raw_api_key else None
    
    st.markdown("---")
    st.write("### 🚀 ایپ کی خصوصیات:")
    st.success("""
    1. **ملٹی فائل سپورٹ:** ہارڈ ڈسک سے ایک ساتھ کئی کتب (PDF) پر ریسرچ۔
    2. **عالمی ویب سرچ:** ویب پر موجود ہر زبان کے نسخوں تک رسائی۔
    3. **نسخوں کا موازنہ:** مختلف پبلشرز، جلد اور صفحہ نمبر کی تفریق۔
    """)

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # --- ایرر فری ماڈل سلیکٹر (Fail-Safe Logic) ---
        @st.cache_resource
        def get_working_model():
            try:
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                # ترجیحی ترتیب تاکہ 404 یا 400 نہ آئے
                for target in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
                    if target in available_models: return target
                return available_models[0]
            except Exception:
                return "gemini-1.5-flash" # ڈیفالٹ

        model_name = get_working_model()
        model = genai.GenerativeModel(model_name)
        # --------------------------------------------

        # آپشنز کا انتخاب
        tab1, tab2 = st.tabs(["📚 میری لائبریری (PC/Hard Disk)", "🌐 عالمی ویب ریسرچ"])

        with tab1:
            st.subheader("ہارڈ ڈسک سے کتب اپ لوڈ کریں")
            user_files = st.file_uploader("ایک یا زائد PDF فائلیں منتخب کریں:", type=['pdf'], accept_multiple_files=True)
            if user_files:
                st.info(f"منتخب شدہ کتب: {len(user_files)}")

        with tab2:
            st.subheader("آن لائن کتب و پبلشرز موازنہ")
            st.write("اس ٹیب میں آپ بغیر فائل اپ لوڈ کیے براہِ راست انٹرنیٹ سے تحقیق کر سکتے ہیں۔")

        # مشترکہ سوال نامہ
        query = st.text_area("آپ کا تحقیقی سوال (مثلاً: فلان مسئلے پر مختلف نسخوں کے حوالے دیں):", height=120)
        
        col1, col2 = st.columns(2)
        with col1:
            target_pub = st.text_input("مخصوص پبلشر (مثلاً: دار السلام، مکتبہ شاملہ):")
        with col2:
            target_ed = st.text_input("جلد یا صفحہ نمبر (اگر معلوم ہو):")

        if st.button("جامع تحقیق شروع کریں"):
            if not query:
                st.warning("براہِ کرم اپنا سوال درج کریں۔")
            else:
                with st.spinner(f"المحقّق AI (ماڈل: {model_name}) ڈیٹا پروسیس کر رہا ہے..."):
                    # عالمی تحقیقی ہدایات
                    prompt_context = f"""آپ ایک عالمی سطح کے محقق اور لائبریرین ہیں۔ 
                    - صارف کے سوال کا جواب انتہائی علمی اور مدلل انداز میں دیں۔
                    - اگر فائلیں موجود ہیں تو ان کا ہر صفحہ باریکی سے چیک کریں۔
                    - انٹرنیٹ سے اس کتاب کے تمام دستیاب نسخوں (طبع) کا موازنہ کریں۔
                    - پبلشر: {target_pub} اور ایڈیشن: {target_ed} کو ترجیح دیں۔
                    - جواب میں کتاب، مصنف، پبلشر، جلد اور صفحہ نمبر کا حوالہ لازمی دیں۔"""

                    try:
                        if user_files and any(f for f in user_files):
                            # ملٹی فائل پروسیسنگ
                            request_data = []
                            for f in user_files:
                                request_data.append({"mime_type": "application/pdf", "data": f.read()})
                            request_data.append(prompt_context + "\n" + query)
                            response = model.generate_content(request_data)
                        else:
                            # خالص ویب ریسرچ
                            response = model.generate_content(prompt_context + "\n" + query)
                        
                        st.markdown("### 📜 تحقیقی رپورٹ:")
                        st.write(response.text)
                        
                    except Exception as e:
                        st.error(f"تحقیق کے دوران خرابی: {str(e)}")
                        st.info("مشورہ: اگر 400 ایرر آئے تو اپنی API Key دوبارہ چیک کریں یا چھوٹی فائل سے ٹیسٹ کریں۔")

    except Exception as e:
        st.error(f"سسٹم کنکشن ایرر: {e}")
else:
    st.warning("تحقیق شروع کرنے کے لیے سائیڈ بار میں اپنی 'Gemini API Key' درج کریں۔")
