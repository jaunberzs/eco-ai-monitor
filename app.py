
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="TED Market Analyzer — Исправленный API", layout="wide")
st.title("🌍 TED Market Analyzer — API V3 (исправлено)")

st.markdown("##### Поиск тендеров через официальное API TED v3 с фильтрацией по странам.")

keywords = st.text_input("Ключевые слова (через запятую):", "air quality, emission, dispersion, monitoring, risk")
selected_countries = st.multiselect(
    "Страны:",
    options=[
        "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "IT",
        "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE", "NO", "IS", "LI", "CH", "UK"
    ],
    default=["DE", "LV", "PL"]
)

if st.button("🔍 Найти тендеры"):
    if not selected_countries:
        st.error("❗ Пожалуйста, выберите хотя бы одну страну.")
    else:
        st.info("⏳ Отправка запроса к TED API...")
        query = " OR ".join(k.strip() for k in keywords.split(","))

        url = "https://api.ted.europa.eu/v3/notices/search"
        headers = {"Content-Type": "application/json"}

        body = {
            "q": query,
            "filters": {
                "country": selected_countries
            },
            "limit": 100
        }

        try:
            response = requests.post(url, json=body, headers=headers)
            st.write("🔧 Код ответа:", response.status_code)

            if response.status_code == 200:
                data = response.json()
                st.success("✅ Ответ получен")

                if "results" in data:
                    df = pd.DataFrame([{
                        "ID": r.get("id"),
                        "Title": r.get("title", {}).get("en", "—"),
                        "Country": r.get("country"),
                        "Publication Date": r.get("publicationDate", "—"),
                        "URL": f'https://ted.europa.eu/en/notice/{r.get("id")}'
                    } for r in data["results"]])
                    st.dataframe(df)
                    st.download_button("💾 Скачать CSV", df.to_csv(index=False), "ted_results.csv")
                else:
                    st.warning("Ответ получен, но нет данных.")
            else:
                st.error("❌ Ошибка при запросе: " + response.text)
        except Exception as e:
            st.exception(f"🚨 Ошибка выполнения: {e}")
