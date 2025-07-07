
import streamlit as st
import requests
import json

st.title("TED Market Analyzer — API V3")

st.markdown("### Подключение к новому API TED v3. Используется фильтрация по странам и ключевым словам.")

keywords = st.text_input("🔑 Ключевые слова (через запятую):", "air quality, emission, dispersion, monitoring, risk")
countries = st.multiselect("🌍 Страны:", ["DE", "LV", "PL", "FI", "SE", "NO"], default=["DE", "LV", "PL"])

if st.button("🔍 Найти тендеры"):
    st.info("Отправка запроса к TED API...")

    headers = {
        "Content-Type": "application/json"
    }

    query = {
        "q": keywords,
        "placeOfPerformance": {
            "countries": countries
        }
    }

    try:
        response = requests.post("https://ted.europa.eu/api/v3/api/search", headers=headers, data=json.dumps(query))
        st.write("📬 Код ответа:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            if "results" in data:
                st.success(f"🔎 Найдено записей: {len(data['results'])}")
                for item in data["results"][:10]:
                    st.markdown(f"- {item.get('title', 'Без названия')}")
            else:
                st.warning("Нет данных в ответе.")
        else:
            st.error(f"Ошибка: {response.text}")

    except Exception as e:
        st.error(f"Ошибка при выполнении запроса: {str(e)}")
