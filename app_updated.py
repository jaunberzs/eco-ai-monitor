
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt
import io
import time

st.set_page_config(page_title="Eco Market Monitor", layout="wide")
st.title("📊 Мониторинг тендеров в сфере экологии (ЕС)")

DEFAULT_KEYWORDS = ["air quality", "dispersion modeling"]
COUNTRY_CODES = {
    "Germany": "DE",
    "Latvia": "LV",
}

st.sidebar.header("🔍 Настройки поиска")
selected_keywords = st.sidebar.multiselect("Ключевые слова:", DEFAULT_KEYWORDS, default=DEFAULT_KEYWORDS)
selected_countries = st.sidebar.multiselect("Страны:", list(COUNTRY_CODES.keys()), default=list(COUNTRY_CODES.keys()))
start_button = st.sidebar.button("🚀 Начать поиск")

def fetch_tenders(keyword, country_code):
    try:
        url = f"https://ted.europa.eu/TED/search/searchResult.html?searchScope=SIMPLE&locale=en&SearchType=AdvancedSearch&text={keyword}&Country={country_code}"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        tenders = []
        for i, item in enumerate(soup.select('.notice-result')):
            if i >= 10:
                break
            title = item.select_one('.notice-title').text.strip() if item.select_one('.notice-title') else 'N/A'
            date = item.select_one('.notice-published').text.strip() if item.select_one('.notice-published') else 'N/A'
            tenders.append({"Title": title, "Date": date, "Country": country_code, "Keyword": keyword})
        return tenders
    except Exception as e:
        st.warning(f"Ошибка при обработке {keyword} ({country_code}): {e}")
        return []

if start_button:
    st.info("🔄 Сбор данных запущен...")
    all_tenders = []
    progress_bar = st.progress(0)
    total = len(selected_keywords) * len(selected_countries)
    step = 0

    for country in selected_countries:
        code = COUNTRY_CODES[country]
        for kw in selected_keywords:
            st.write(f"🔍 Обработка: {kw} в {country}")
            tenders = fetch_tenders(kw, code)
            all_tenders.extend(tenders)
            step += 1
            progress_bar.progress(step / total)
            time.sleep(1)

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
