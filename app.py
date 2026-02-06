import streamlit as st
import google.generativeai as genai

# ایپ کی بنیادی سیٹنگ
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
    st.info("""
    **خصوصی فیچرز:**
    1. انٹرنیٹ PDF سپورٹ
    2. پبلشر و جلد کی تفصیل
    3. درست صفحہ نمبر حوالہ
    """)

if api_key:
    genai.configure(api_key=api_key)
    # یہاں ہم نے 'latest' ماڈل کا استعمال کیا ہے تاکہ Error نہ آئے
    model = genai.GenerativeModel('gemini-1.5-pro')

    # آپشنز
    source = st.radio("تحقیق کا ذریعہ منتخب کریں:", ["لوکل فائل (PDF/Image)", "انٹرنیٹ PDF لنک", "عالمی ویب سرچ"])

    user_input = None
    if source == "لوکل فائل (PDF/Image)":
        user_input = st.file_uploader("کتاب اپ لوڈ کریں", type=['pdf', 'jpg', 'png', 'jpeg'])
    elif source == "انٹرنیٹ PDF لنک":
        user_input = st.text_input("آن لائن PDF کا مکمل لنک یہاں ڈالیں:")

    query = st.text_area("آپ کا سوال (مثلاً: فلان پبلشر کی کتاب، جلد 2، صفحہ 40 پر کیا لکھا ہے؟)")

    if st.button("جامع تحقیق شروع کریں"):
        with st.spinner("المحقّق AI ڈیٹا تلاش کر رہا ہے..."):
            system_prompt = "آپ ایک ماہر محقق ہیں۔ اگر صارف پبلشر، جلد یا صفحہ پوچھے تو انٹرنیٹ اور لائبریری ڈیٹا سے درست حوالہ دیں۔ جواب میں کتاب کا نام اور صفحہ نمبر لازمی لکھیں۔"
            
            try:
                if source == "لوکل فائل (PDF/Image)" and user_input:
                    response = model.generate_content([{"mime_type": user_input.type, "data": user_input.read()}, system_prompt + query])
                else:
                    full_query = f"{system_prompt} \n ذریعہ: {user_input if user_input else 'Open Web'} \n سوال: {query}"
                    response = model.generate_content(full_query)
                
                st.markdown("### 📜 تحقیقی رپورٹ:")
                st.write(response.text)
            except Exception as e:
                st.error(f"تحقیق میں رکاوٹ: {e}")
else:
    st.warning("براہِ کرم سائیڈ بار میں API Key درج کریں۔")
