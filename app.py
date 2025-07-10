
import streamlit as st
import pandas as pd
from pytrends.request import TrendReq
import altair as alt

st.set_page_config(page_title="Google Trends – Full Market Analysis", layout="wide")
st.title("📈 Полный анализ спроса на экологические и инженерные услуги в Европе")

keywords = ['air pollution modeling', 'air dispersion modeling', 'noise mapping', 'environmental noise modeling', 'air quality monitoring', 'industrial risk assessment', 'chemical accident modeling', 'risk zone simulation', 'environmental impact assessment', 'geo-environmental consulting', 'air quality simulation', 'dispersion modeling', 'sound propagation model', 'traffic noise simulation', 'consequence modeling software']

geo_options = {
    "Европа (вся)": "",
    "Германия": "DE",
    "Франция": "FR",
    "Нидерланды": "NL",
    "Швеция": "SE",
    "Финляндия": "FI",
    "Норвегия": "NO",
    "Латвия": "LV",
    "Польша": "PL",
    "Великобритания": "GB"
}

st.sidebar.header("🔍 Параметры запроса")
geo_label = st.sidebar.selectbox("Страна", list(geo_options.keys()))
geo = geo_options[geo_label]
kw_selected = st.sidebar.multiselect("Ключевые слова", keywords, default=keywords[:5])

if st.sidebar.button("📊 Запустить анализ"):
    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload(kw_selected, cat=0, timeframe="today 5-y", geo=geo)
    data = pytrends.interest_over_time()

    if data.empty:
        st.warning("Нет данных по выбранным параметрам.")
    else:
        data = data.reset_index()
        df = pd.melt(data, id_vars=["date"], value_vars=kw_selected,
                     var_name="keyword", value_name="interest")

        st.altair_chart(
            alt.Chart(df).mark_line().encode(
                x="date:T",
                y="interest:Q",
                color="keyword:N",
                tooltip=["date:T", "keyword:N", "interest:Q"]
            ).properties(width=900, height=500),
            use_container_width=True
        )

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Скачать CSV", csv, "trends_data.csv", "text/csv")
else:
    st.info("Выберите страну и ключевые слова слева и нажмите кнопку.")
