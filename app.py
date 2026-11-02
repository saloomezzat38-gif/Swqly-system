import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="سيستم وكالة سوقلي", layout="wide")

# --- قاعدة البيانات المصغرة لكل عميل ---
database = {
    "نيو كافيه": {
        "spend": "1,500 EGP", "reach": "45,200", "clicks": "1,250", "cpa": "3.5 EGP",
        "campaigns": [{"اسم الحملة": "عروض المنيو الجديد", "الهدف": "رسائل", "المصروف": "500", "النتائج": "120 رسالة"}],
        "content": [{"نوع المحتوى": "Reel", "الوصف": "فيديو تحضير القهوة", "المشاهدات": "12,000", "التفاعل": "850"}],
        "age": [25, 45, 15, 10, 5], "loc": [35, 25, 20, 10, 10]
    },
    "إبداع للعطور": {
        "spend": "3,200 EGP", "reach": "95,000", "clicks": "3,400", "cpa": "8.2 EGP",
        "campaigns": [{"اسم الحملة": "عروض العطور الشتوية", "الهدف": "مبيعات", "المصروف": "2000", "النتائج": "45 أوردر"}],
        "content": [{"نوع المحتوى": "بوست صور", "الوصف": "تصميم عطر العود", "المشاهدات": "22,000", "التفاعل": "1,200"}],
        "age": [10, 30, 40, 15, 5], "loc": [20, 15, 40, 15, 10]
    },
    "هايبر الفادي": {
        "spend": "5,000 EGP", "reach": "150,000", "clicks": "5,000", "cpa": "2.1 EGP",
        "campaigns": [{"اسم الحملة": "مجلة العروض الأسبوعية", "الهدف": "تفاعل", "المصروف": "1000", "النتائج": "3000 شير"}],
        "content": [{"نوع المحتوى": "ألبوم صور", "الوصف": "عروض السوبر ماركت", "المشاهدات": "50,000", "التفاعل": "4,500"}],
        "age": [5, 25, 45, 20, 5], "loc": [50, 10, 15, 15, 10]
    }
}

default_data = {
    "spend": "0 EGP", "reach": "0", "clicks": "0", "cpa": "0 EGP",
    "campaigns": [{"اسم الحملة": "-", "الهدف": "-", "المصروف": "-", "النتائج": "-"}],
    "content": [{"نوع المحتوى": "-", "الوصف": "-", "المشاهدات": "-", "التفاعل": "-"}],
    "age": [0, 0, 0, 0, 0], "loc": [0, 0, 0, 0, 0]
}

# 1. القائمة الجانبية
try:
    st.sidebar.image("logo.png", use_container_width=True)
except:
    pass
    
st.sidebar.markdown("---")
st.sidebar.header("📅 فلاتر التقرير")

clients = ["نيو كافيه", "إبداع للعطور", "هايبر الفادي", "أسواق التوحيد", "قطونيل قطور", "عميل آخر"]
selected_client = st.sidebar.selectbox("اختر العميل", clients)

data = database.get(selected_client, default_data)

years = [2024, 2025, 2026]
months = list(range(1, 13))
days = list(range(1, 32))

selected_year = st.sidebar.selectbox("اختر السنة", years)
selected_month = st.sidebar.selectbox("اختر الشهر", months)
selected_day = st.sidebar.selectbox("اختر اليوم", days)

# 2. الشاشة الرئيسية
st.title("📊 لوحة تحكم وكالة سوقلي")
st.markdown(f"**العميل:** {selected_client} | **التاريخ:** {selected_year}/{selected_month}/{selected_day}")

tab1, tab2, tab3, tab4 = st.tabs(["📈 نتائج الإعلانات", "📱 أداء المحتوى", "🤖 مولد الخطة الشهرية", "👥 تحليل الجمهور"])

# --- تاب 1: نتائج الإعلانات ---
with tab1:
    st.subheader(f"ملخص حملات ({selected_client})")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("الميزانية المصروفة", data["spend"])
    col2.metric("الوصول (Reach)", data["reach"])
    col3.metric("النقرات (Clicks)", data["clicks"])
    col4.metric("سعر النتيجة", data["cpa"])
    
    st.markdown("---")
    st.table(data["campaigns"])

# --- تاب 2: أداء المحتوى ---
with tab2:
    st.subheader("أفضل المنشورات هذا الشهر")
    st.table(data["content"])

# --- تاب 3: مولد الخطة ---
with tab3:
    st.subheader(f"🤖 خطة محتوى مقترحة لـ ({selected_client})")
    goal = st.text_input("إيه الهدف من الخطة؟ (مثال: مبيعات، تفاعل)")
    if st.button("✨ توليد الخطة"):
        if goal:
            st.success("تم التوليد بنجاح!")
            ai_plan = [
                {"الأسبوع": "الأول", "النوع": "Reel", "الفكرة": f"فيديو لـ {goal}"},
                {"الأسبوع": "الثاني", "النوع": "صور", "الفكرة": "ريفيوهات العملاء"}
            ]
            st.table(ai_plan)

# --- تاب 4: تحليل الجمهور ---
with tab4:
    st.subheader(f"👥 تحليل المتابعين لـ ({selected_client})")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**التوزيع العمري**")
        age_df = pd.DataFrame({"الفئة": ["18-24", "25-34", "35-44", "45-54", "55+"], "النسبة": data["age"]}).set_index("الفئة")
        st.bar_chart(age_df)
    with col2:
        st.markdown("**أكثر الأماكن تفاعلاً**")
        loc_df = pd.DataFrame({"المدينة": ["طنطا", "قطور", "كفر الزيات", "إيتاي البارود", "دمنهور"], "النسبة": data["loc"]}).set_index("المدينة")
        st.bar_chart(loc_df)
