
import streamlit as st
import requests

st.title("TED Market Analyzer — API Поиск тендеров в экологии")

keywords = st.text_input("Ключевые слова (через запятую):", "air quality, emission, dispersion, monitoring, risk")
selected_countries = st.multiselect("Страны:", ["DE", "LV", "PL", "FR", "ES", "IT", "FI", "SE", "NO", "NL", "BE", "AT", "DK", "EE", "LT", "CZ", "SK", "HU", "RO", "BG", "HR", "SI", "GR", "IE", "PT"], default=["DE", "LV", "PL"])
limit = st.slider("Лимит результатов", 1, 100, 10)

if st.button("Найти тендеры"):
    st.info("Отправка запроса к TED API...")
    url = "https://ted.europa.eu/api/v3/search"
    payload = {
        "keywords": [k.strip() for k in keywords.split(",")],
        "countries": selected_countries,
        "limit": limit,
        "sort": "mostRelevant"
    }
    try:
        response = requests.post(url, json=payload)
        st.write("Код ответа:", response.status_code)
        st.json(response.json())
    except Exception as e:
        st.error(f"Ошибка: {str(e)}")
