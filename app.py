
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="TED Market Analyzer — Поиск через API", layout="wide")

st.title("🌍 TED Market Analyzer — API Поиск тендеров в экологии")
st.markdown("#### Используется прямое подключение к Search API TED")

keywords = st.text_input("🔑 Ключевые слова (через запятую):", "air quality, emission, dispersion, monitoring, risk")
selected_countries = st.multiselect(
    "🌐 Страны:",
    options=[
        "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "IT",
        "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE", "NO", "IS", "LI", "CH", "UK"
    ],
    default=["DE", "LV", "PL"]
)

if st.button("🚀 Найти тендеры"):
    st.info("⏳ Поиск тендеров через TED API...")
    query = " OR ".join(k.strip() for k in keywords.split(","))
    body = {
        "query": query,
        "country": selected_countries,
        "limit": 500
    }

    response = requests.post("https://api.ted.europa.eu/v3/notices/search", json=body)
    if response.status_code == 200:
        data = response.json()
        if "results" in data:
            results = data["results"]
            df = pd.DataFrame([{
                "ID": r.get("id"),
                "Title": r.get("title", {}).get("en", "—"),
                "Country": r.get("country"),
                "Publication Date": r.get("publicationDate", "—"),
                "URL": f'https://ted.europa.eu/en/notice/{r.get("id")}'
            } for r in results])

            st.success(f"🔍 Найдено: {len(df)} тендеров")
            st.dataframe(df, use_container_width=True)
            st.download_button("💾 Скачать CSV", data=df.to_csv(index=False), file_name="ted_results.csv", mime="text/csv")
        else:
            st.warning("❗ Тендеры не найдены.")
    else:
        st.error("🚫 Ошибка при запросе к API TED.")
