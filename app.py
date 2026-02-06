import streamlit as st
import google.generativeai as genai

# پروفیشنل سیٹ اپ
st.set_page_config(page_title="المحقّق AI - عالمی سرچ انجن", layout="wide")

st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; font-family: 'Jameel Noori Nastaleeq', 'Urdu Typesetting', serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔍 المحقّق AI: عالمی ڈیجیٹل لائبریری و ریسرچ سسٹم")

with st.sidebar:
    st.header("⚙️ ایڈوانس کنٹرول پینل")
    api_key = st.text_input("Gemini API Key درج کریں:", type="password")
    st.info("""
    **شامل فیچرز:**
    1. آن لائن PDF لنک سپورٹ
    2. پبلشر و ایڈیشن کی تفصیص
    3. جلد و صفحہ نمبر کی درست نشاندہی
    4. تقابلی مسلکی مطالعہ
    """)

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # ریسرچ کے ذرائع
    source_type = st.radio("تحقیق کا ذریعہ منتخب کریں:", 
                          ["لوکل فائل اپ لوڈ کریں", "انٹرنیٹ PDF لنک (URL)", "عالمی ویب سرچ (بغیر فائل)"])

    input_data = None
    if source_type == "لوکل فائل اپ لوڈ کریں":
        input_data = st.file_uploader("کتاب یا دستاویز اپ لوڈ کریں", type=['pdf', 'jpg', 'png', 'jpeg'])
    elif source_type == "انٹرنیٹ PDF لنک (URL)":
        input_data = st.text_input("انٹرنیٹ پر موجود PDF کا لنک یہاں پیسٹ کریں:")

    user_query = st.text_area("آپ کا سوال (مثلاً: فلان پبلشر کی کتاب، جلد 2، صفحہ 40 پر کیا لکھا ہے؟)")

    if st.button("جامع تحقیق شروع کریں"):
        if user_query:
            with st.spinner("المحقّق AI عالمی ڈیٹا بیس سے رجوع کر رہا ہے..."):
                system_instruction = """
                آپ ایک 'عالمی محقق' ہیں۔ آپ کے پاس دنیا بھر کے پبلشرز اور لائبریریوں کا علم ہے۔
                1. اگر صارف مخصوص پبلشر، جلد یا صفحہ پوچھے تو انٹرنیٹ کی مدد سے درست ترین معلومات فراہم کریں۔
                2. جواب میں کتاب کا نام، پبلشر، ایڈیشن، جلد اور صفحہ نمبر کی واضح سرخی بنائیں۔
                3. مختلف مسالک (احناف، شوافع، اہل حدیث وغیرہ) کی کتب سے تقابلی حوالہ دیں۔
                4. اگر صارف آن لائن لنک دے، تو اس کا متن نکال کر تجزیہ کریں۔
                """
                
                try:
                    if source_type == "لوکل فائل اپ لوڈ کریں" and input_data:
                        response = model.generate_content([{"mime_type": input_data.type, "data": input_data.read()}, system_instruction + user_query])
                    else:
                        # لنک یا ویب سرچ کے لیے
                        search_prompt = f"{system_instruction} \n ذریعہ: {input_data if input_data else 'Open Web'} \n سوال: {user_query}"
                        response = model.generate_content(search_prompt)
                    
                    st.success("تحقیق مکمل!")
                    st.markdown("### 📜 المحقّق کی رپورٹ:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"تحقیق میں رکاوٹ: {e}")
else:
    st.info("سائیڈ بار میں API Key درج کر کے اپنے ریسرچ سسٹم کو ایکٹیویٹ کریں۔")