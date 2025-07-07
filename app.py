
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Eco Market Monitor", layout="wide")
st.title("📊 Мониторинг тендеров в сфере экологии (ЕС)")

DEFAULT_KEYWORDS = [
    "air quality", "dispersion modeling", "emission modeling",
    "environmental impact assessment", "noise modeling",
    "pollution forecast", "air monitoring", "industrial risk assessment"
]

COUNTRY_CODES = {
    "Germany": "DE",
    "Poland": "PL",
    "Netherlands": "NL",
    "Ireland": "IE",
    "Latvia": "LV",
    "Finland": "FI",
    "Sweden": "SE",
    "Norway": "NO",
}

st.sidebar.header("🔍 Настройки поиска")
selected_keywords = st.sidebar.multiselect("Ключевые слова:", DEFAULT_KEYWORDS, default=DEFAULT_KEYWORDS)
selected_countries = st.sidebar.multiselect("Страны:", list(COUNTRY_CODES.keys()), default=list(COUNTRY_CODES.keys()))
start_button = st.sidebar.button("🚀 Начать поиск")

def fetch_tenders(keyword, country_code):
    url = f"https://ted.europa.eu/TED/search/searchResult.html?searchScope=SIMPLE&locale=en&SearchType=AdvancedSearch&text={keyword}&Country={country_code}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tenders = []
    for item in soup.select('.notice-result'):
        title = item.select_one('.notice-title').text.strip() if item.select_one('.notice-title') else 'N/A'
        date = item.select_one('.notice-published').text.strip() if item.select_one('.notice-published') else 'N/A'
        tenders.append({"Title": title, "Date": date, "Country": country_code, "Keyword": keyword})
    return tenders

if start_button:
    st.info("🔄 Идёт сбор данных... Подождите немного.")
    all_tenders = []
    for country in selected_countries:
        code = COUNTRY_CODES[country]
        for kw in selected_keywords:
            tenders = fetch_tenders(kw, code)
            all_tenders.extend(tenders)

    if all_tenders:
        df = pd.DataFrame(all_tenders)
        df['Parsed Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Month'] = df['Parsed Date'].dt.to_period('M')

        st.success(f"✅ Найдено {len(df)} тендеров.")
        st.dataframe(df)

        summary = df.groupby(['Month', 'Country']).size().unstack(fill_value=0)
        st.subheader("📈 Динамика по странам")
        st.bar_chart(summary)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        st.download_button("⬇️ Скачать Excel", data=output.getvalue(), file_name="eco_tenders_monitor.xlsx")
    else:
        st.warning("Ничего не найдено по заданным параметрам.")
