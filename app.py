import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="المحقّق AI - عالمی ریسرچ انجن", layout="wide")

st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; font-family: 'Jameel Noori Nastaleeq', serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔍 المحقّق AI: عالمی ڈیجیٹل لائبریری")

with st.sidebar:
    st.header("⚙️ ایڈوانس کنٹرول پینل")
    api_key = st.text_input("Gemini API Key درج کریں:", type="password")
    st.info("خصوصی فیچرز: عالمی سرچ، پبلشر و جلد کی تفصیل، اور بڑی فائلز کی سپورٹ۔")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # آپ کا بتایا ہوا خودکار ماڈل والا حصہ
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = 'models/gemini-1.5-pro' if 'models/gemini-1.5-pro' in available_models else available_models[0]
        model = genai.GenerativeModel(model_name)
        
        # ذریعہ کا انتخاب
        source = st.radio("تحقیق کا ذریعہ منتخب کریں:", ["لوکل فائل (PDF/Image)", "انٹرنیٹ PDF لنک", "عالمی ویب سرچ"])

        user_input = None
        if source == "لوکل فائل (PDF/Image)":
            user_input = st.file_uploader("کتاب یا دستاویز اپ لوڈ کریں", type=['pdf', 'jpg', 'png', 'jpeg'])
        elif source == "انٹرنیٹ PDF لنک":
            user_input = st.text_input("آن لائن PDF کا لنک یہاں ڈالیں:")

        query = st.text_area("آپ کا سوال (مثلاً: فلان پبلشر کی کتاب، جلد 2، صفحہ 40 پر کیا لکھا ہے؟)")

        if st.button("جامع تحقیق شروع کریں"):
            with st.spinner("المحقّق AI تحقیق کر رہا ہے..."):
                system_instr = "آپ ایک ماہر محقق ہیں۔ کتاب کا نام، پبلشر، جلد اور صفحہ نمبر کا حوالہ لازمی دیں۔"
                
                if source == "لوکل فائل (PDF/Image)" and user_input:
                    response = model.generate_content([{"mime_type": user_input.type, "data": user_input.read()}, system_instr + query])
                else:
                    context = f"ذریعہ: {user_input if user_input else 'Open Web'}"
                    response = model.generate_content(f"{system_instr} \n {context} \n سوال: {query}")
                
                st.markdown("### 📜 تحقیقی رپورٹ:")
                st.write(response.text)
                
    except Exception as e:
        st.error(f"تکنیکی رکاوٹ: {e}")
else:
    st.warning("براہِ کرم سائیڈ بار میں اپنی API Key درج کریں۔")
