
import streamlit as st
import pandas as pd
from pytrends.request import TrendReq
import altair as alt

st.set_page_config(page_title="Google Trends – Market Signals", layout="wide")

st.title("📈 Google Trends: Анализ спроса по странам Европы")

keywords = [
    "air pollution modeling",
    "air dispersion modeling",
    "noise mapping",
    "environmental noise modeling",
    "air quality monitoring",
    "industrial risk assessment",
    "chemical accident modeling",
    "risk zone simulation"
]

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

kw_selected = st.sidebar.multiselect("Ключевые слова", keywords, default=keywords[:3])

if st.sidebar.button("🔄 Получить данные"):
    pytrends = TrendReq(hl="en-US", tz=360)
    pytrends.build_payload(kw_selected, cat=0, timeframe="today 5-y", geo=geo)
    data = pytrends.interest_over_time()

    if data.empty:
        st.warning("Нет данных для выбранных параметров.")
    else:
        data = data.reset_index()
        df = pd.melt(data, id_vars=["date"], value_vars=kw_selected, var_name="keyword", value_name="interest")

        st.altair_chart(
            alt.Chart(df).mark_line().encode(
                x="date:T",
                y="interest:Q",
                color="keyword:N",
                tooltip=["date:T", "keyword:N", "interest:Q"]
            ).properties(width=900, height=450),
            use_container_width=True
        )
else:
    st.info("Выберите параметры в боковой панели и нажмите кнопку для запуска анализа.")
