import streamlit as st
import google.generativeai as genai

# پیج سیٹنگز
st.set_page_config(page_title="المحقّق AI - ریسرچ انجن", layout="wide")

# اردو ڈیزائن
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; font-family: 'Jameel Noori Nastaleeq', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔍 المحقّق AI: جامع تحقیقی مرکز")

with st.sidebar:
    st.header("⚙️ ترتیبات")
    api_key = st.text_input("Gemini API Key درج کریں:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # --- ایرر ختم کرنے والا جادوئی حصہ ---
        @st.cache_resource
        def get_best_model():
            try:
                # دستیاب ماڈلز کی فہرست حاصل کریں
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                # ترجیحی ترتیب: 1.5 Flash -> 1.5 Pro -> Gemini Pro
                if 'models/gemini-1.5-flash' in models: return 'models/gemini-1.5-flash'
                if 'models/gemini-1.5-pro' in models: return 'models/gemini-1.5-pro'
                return models[0] # جو بھی پہلا دستیاب ہو
            except:
                return 'gemini-pro' # آخری حل

        selected_model_name = get_best_model()
        model = genai.GenerativeModel(selected_model_name)
        # ----------------------------------

        source = st.radio("تحقیق کا ذریعہ:", ["میری لائبریری (ملٹی فائلز)", "عالمی ویب سرچ"])

        user_files = []
        if source == "میری لائبریری (ملٹی فائلز)":
            # آپ کی شرط: ہارڈ ڈسک سے ملٹی فائل اپ لوڈ
            user_files = st.file_uploader("کتب (PDF) منتخب کریں:", type=['pdf'], accept_multiple_files=True)

        query = st.text_area("آپ کا سوال:")
        
        col1, col2 = st.columns(2)
        with col1:
            publisher = st.text_input("مخصوص پبلشر:")
        with col2:
            edition = st.text_input("جلد/صفحہ نمبر:")

        if st.button("جامع تحقیق شروع کریں"):
            with st.spinner(f"ماڈل ({selected_model_name}) تحقیق کر رہا ہے..."):
                # آپ کی شرط: عالمی سرچ اور نسخوں کا موازنہ
                sys_prompt = f"""آپ ایک ماہر محقق ہیں۔ 
                - پبلشر: {publisher} اور ایڈیشن: {edition} کی تفصیل لازمی دیں۔
                - اگر ایک سے زیادہ نسخے ہیں تو ان کا حوالہ (جلد، صفحہ) موازنہ کے ساتھ دیں۔
                - جواب مکمل اردو اور علمی ہو۔"""

                try:
                    if source == "میری لائبریری (ملٹی فائلز)" and user_files:
                        payload = []
                        for f in user_files:
                            payload.append({"mime_type": "application/pdf", "data": f.read()})
                        payload.append(sys_prompt + "\n" + query)
                        response = model.generate_content(payload)
                    else:
                        response = model.generate_content(sys_prompt + "\n" + query)
                    
                    st.markdown("### 📜 تحقیقی رپورٹ:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"تحقیق میں خرابی: {e}")
                    st.info("مشورہ: ایک بار ایپ ریبوٹ (Reboot) کر کے دیکھیں۔")

    except Exception as e:
        st.error(f"سسٹم کنکشن میں مسئلہ: {e}")
else:
    st.warning("براہِ کرم سائیڈ بار میں API Key درج کریں۔")
