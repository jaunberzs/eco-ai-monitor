
import streamlit as st
import requests
import json

st.set_page_config(page_title="TED Market Analyzer — API v3", layout="wide")

st.title("🌍 TED Market Analyzer — Поиск тендеров (API v3)")
st.markdown("Подключение к **новому API TED v3**. Используется фильтрация по странам и ключевым словам.")

keywords = st.text_input("🔑 Ключевые слова (через запятую)", "air quality, emission, dispersion, monitoring, risk")
countries = st.multiselect("🌐 Страны:", ["DE", "LV", "PL", "SE", "FI", "NO", "EE", "LT", "FR", "IT"], default=["DE", "LV", "PL"])

if st.button("🔍 Найти тендеры"):
    with st.spinner("⏳ Отправка запроса к TED API..."):
        url = "https://api.ted.europa.eu/v3/notices/search"
        headers = {"Content-Type": "application/json"}

        body = {
            "filters": {
                "freeText": keywords.replace(",", " "),
                "countries": countries
            },
            "limit": 100
        }

        response = requests.post(url, headers=headers, data=json.dumps(body))

        st.markdown(f"🔧 **Код ответа:** {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if "items" in data:
                results = data["items"]
                if len(results) > 0:
                    for item in results:
                        st.write(f"📄 {item.get('title', 'Без названия')}")
                        st.write(f"📅 {item.get('publicationDate', '')}")
                        st.write(f"🔗 [Ссылка]({item.get('uri', '#')})")
                        st.markdown("---")
                else:
                    st.info("Нет тендеров по указанным параметрам.")
            else:
                st.error("Нет данных в ответе.")
        else:
            st.error(f"❌ Ошибка при запросе: {response.text}")
