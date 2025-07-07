
import streamlit as st
import requests
import json

st.title("🌍 TED Market Analyzer — API Поиск тендеров в экологии")
st.write("### Подключение к TED API. Уточнён формат запроса и добавлена защита от ошибок.")

keywords = st.text_input("🔑 Ключевые слова (через запятую):", "air quality, emission, dispersion, monitoring, risk")

countries = st.multiselect("🌐 Страны:", ["DE", "LV", "PL", "FI", "SE", "NO", "FR", "IT", "ES", "NL", "BE", "DK", "CZ", "EE", "LT", "AT", "SK", "SI", "PT", "HU", "RO", "HR", "BG", "IE", "GR"], default=["DE", "LV", "PL"])

limit = st.slider("📊 Лимит результатов", 1, 100, 10)

if st.button("🔍 Найти тендеры"):
    st.info("Отправка запроса к TED API...")

    # Примерный endpoint TED API v3 (заглушка, заменить на реальный)
    url = "https://ted.europa.eu/api/v3/notices/search"

    # Пример тела запроса (под корректный API TED)
    payload = {
        "keyword": keywords,
        "limit": limit,
        "countryList": countries
    }

    try:
        response = requests.post(url, json=payload)
        st.text(f"Код ответа: {response.status_code}")

        if response.status_code == 200:
            if response.text.strip() == "":
                st.error("❌ Пустой ответ от TED API.")
            else:
                try:
                    data = response.json()
                    st.success("✅ Данные получены!")
                    st.json(data)
                except json.JSONDecodeError:
                    st.error("❌ Ответ не является JSON.")
                    st.code(response.text, language='html')
        else:
            st.error(f"❌ Ошибка: {response.status_code}")
            st.code(response.text, language='html')

    except Exception as e:
        st.error(f"❌ Исключение при выполнении запроса: {e}")
