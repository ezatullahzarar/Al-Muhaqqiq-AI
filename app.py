import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="المحقّق AI", layout="wide")
st.title("🔍 المحقّق AI: آپ کا اسمارٹ ریسرچ اسسٹنٹ")
st.write("کسی بھی تصویر، رسید، قانونی کاغذ یا کتاب سے معلومات اور حوالہ جات نکالیں")

with st.sidebar:
    st.header("ترتیبات")
    api_key = st.text_input("Gemini API Key یہاں درج کریں:", type="password")
    st.markdown("---")
    st.info("یہ ایپ ہر زبان اور ہر شعبے کی دستاویزات کا تجزیہ کر سکتی ہے۔")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    uploaded_file = st.file_uploader("اپنی فائل (تصویر یا PDF) یہاں اپ لوڈ کریں", type=['pdf', 'jpg', 'png', 'jpeg'])
    user_query = st.text_input("آپ اس فائل کے بارے میں کیا پوچھنا چاہتے ہیں؟")

    if st.button("تحقیق شروع کریں"):
        if uploaded_file and user_query:
            with st.spinner("اے آئی فائل کا مطالعہ کر رہا ہے..."):
                img = Image.open(uploaded_file)
                prompt = f"""
                آپ ایک ماہر تجزیہ کار ہیں۔ اس دستاویز کو دیکھ کر صارف کے سوال کا جواب دیں:
                سوال: {user_query}
                
                براہ کرم جواب میں یہ چیزیں شامل کریں:
                1. فائل کا عنوان اور موضوع
                2. کوئی بھی اہم حوالہ (تاریخ، جلد، صفحہ نمبر وغیرہ)
                3. اہم نکات کا خلاصہ
                جواب مکمل طور پر اردو میں دیں۔
                """
                response = model.generate_content([prompt, img])
                st.success("تجزیہ مکمل!")
                st.markdown(response.text)
        else:
            st.warning("براہ کرم فائل اپ لوڈ کریں اور سوال لکھیں۔")
else:
    st.info("ایپ شروع کرنے کے لیے سائیڈ بار میں اپنی Gemini API Key ڈالیں۔")
