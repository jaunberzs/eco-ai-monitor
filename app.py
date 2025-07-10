
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="TED Market Analyzer", layout="wide")

st.title("📊 TED Market Analyzer — Экология и тендеры по Европе (2020–2024)")

df = pd.read_csv("data/tenders_2020_2024.csv")

# Фильтры
years = st.sidebar.multiselect("Годы", options=sorted(df["year"].unique()), default=sorted(df["year"].unique()))
countries = st.sidebar.multiselect("Страны", options=sorted(df["country"].unique()), default=sorted(df["country"].unique()))
products = st.sidebar.multiselect("Продукты/услуги", options=sorted(df["product"].unique()), default=sorted(df["product"].unique()))

df_filtered = df[df["year"].isin(years) & df["country"].isin(countries) & df["product"].isin(products)]

# Метрики
col1, col2, col3 = st.columns(3)
col1.metric("Всего тендеров", df_filtered["tenders"].sum())
col2.metric("Общая сумма (€)", f'{df_filtered["total_value"].sum():,.0f}')
col3.metric("Средний бюджет (€)", f'{df_filtered["total_value"].mean():,.0f}')

# Графики
st.subheader("📈 Динамика по годам")
st.altair_chart(
    alt.Chart(df_filtered).mark_bar().encode(
        x="year:O",
        y="tenders:Q",
        color="product:N",
        tooltip=["year", "country", "product", "tenders", "total_value"]
    ).properties(width=700, height=400),
    use_container_width=True
)

st.subheader("🌍 Объем тендеров по странам")
st.altair_chart(
    alt.Chart(df_filtered).mark_bar().encode(
        x="country:N",
        y="total_value:Q",
        color="product:N",
        tooltip=["country", "total_value"]
    ).properties(width=700, height=400),
    use_container_width=True
)
